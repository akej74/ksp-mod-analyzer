"""
    curse.py
    -----------
    Implements functions for parsing the Curse website.
"""

import re
import sys

import requests
from PyQt5 import QtCore
from bs4 import BeautifulSoup

import helpers


class CurseThread(QtCore.QThread):
    """QThread for processing."""

    # Signal for handling exceptions that may occur in the running thread
    exception_signal = QtCore.pyqtSignal(str)

    # Finished signal, emitted at the end of the run
    finished_signal = QtCore.pyqtSignal(str)

    # Cancelled signal, emitted when the thread is stopped
    cancelled_signal = QtCore.pyqtSignal(str)

    # Signal for updating the progress bar
    notify_progress_signal = QtCore.pyqtSignal(int)

    def __init__(self, db_file, use_cache):
        super().__init__()
        self.db_file = db_file
        self.use_cache = use_cache
        self.keep_running = False
        self.session = requests.session()  # Keep the session, improves performance

    def __del__(self):
        self.wait()

    def stop(self):
        """Stops the running thread gracefully."""

        print('Stopping Curse thread...')
        self.keep_running = False

        # Wait for the thread to stop
        self.wait()
        self.cancelled_signal.emit('curse')
        print('Curse thread stopped')

    def run(self):
        """Main thread processing loop."""

        self.keep_running = True

        try:
            print('Starting Curse thread...')
            # Get data from Curse and update database
            self.update_curse()

            # Update database table 'Total'
            helpers.update_total_mods(self.db_file)

            # Only emit finished signal if job was not cancelled (i.e. 'keep_running' is still True)
            if self.keep_running:
                self.finished_signal.emit('curse')

        # Exception handling:
        # Emits a signal if an exception occurs in the running thread
        # The main application will then show an error message about the problem
        # This is needed because a new message box widget cannot be created/displayed in the thread
        except Exception as e:
            # Stop the thread
            self.stop()
            print('Curse thread stopped at exception')

            # Get info about the exception
            (type, value, traceback) = sys.exc_info()

            # Generate a detailed error message
            msg = helpers.exception_message_qthread(type, value, traceback)

            # Emit a signal with the error message to be displayed in a message box in the main UI
            self.exception_signal.emit(msg)

    def update_curse(self):
        """Updates the database with data from Curse."""

        # Check if cached data on disk should be used
        if self.use_cache:
            # Read mod list from disk
            mods = helpers.read_from_disk('data/curse.data')

            # Update database
            helpers.update_db('Curse', mods, self.db_file)
        else:
            # Empty dict to hold all mod data
            mods = {}

            # Set initial value (3%) for progress bar to indicate processing has started
            self.notify_progress_signal.emit(3)

            # Define the initial URL for getting the mods from the first page
            curse_init_url = 'https://mods.curse.com/ksp-mods/kerbal'

            # Get the first Curse page and prepare for HTML parsing (BeautifulSoup object)
            soup_first_page = self.get_page(curse_init_url)

            # Get the mods from the first page and update the dict
            mods_first_page = get_curse_mods(soup_first_page)
            mods.update(mods_first_page)

            # Find how many sub-pages there are
            pages = find_max_page(soup_first_page)

            # Calculate the progress bar interval based on number of pages
            progress_bar_interval = 100 / int(pages)

            # Verify parsing of number of pages on Curse
            if pages:
                print('Total sub-pages on Curse', pages)
            else:
                raise Exception('Error parsing Curse, no pages found.')

            # Define the URL for the next page (starting from page 2) and get the remaining mods
            for page in range(2, int(pages) + 1):
                if self.keep_running:
                    # Create a new URL to fetch data from the next page
                    # E.g. "https://mods.curse.com/ksp-mods/kerbal?page=2"
                    new_curse_url = curse_init_url + "?page=" + str(page)

                    # Get data from the page
                    new_soup = self.get_page(new_curse_url)

                    # Another check is needed in case the thread was stopped while the HTTP request was running
                    if self.keep_running:
                        # Update progress bar
                        self.notify_progress_signal.emit(progress_bar_interval * page)

                    # Get the mods from the current page
                    mods_new_page = get_curse_mods(new_soup)

                    # Update dict with mods from the current page
                    mods.update(mods_new_page)

            # Write data to file
            helpers.write_to_disk('data/curse.data', mods)

            # Update database
            helpers.update_db('Curse', mods, self.db_file)

    def get_page(self, url):
        """Gets a web page using the session object and return a soup object."""

        try:
            response = self.session.get(url)
        except:
            # Raise any exception to be handled by the QThread
            raise

        # Create a BeautifulSoup object from the HTML page
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup


def find_max_page(soup):
    """Finds the number of sub-pages in the HTML code, it's a two digit number... E.g. "1 2 3 4 5 ... 37"""

    # Using a regexp, find HREF's with two digits, e.g. <a href="/ksp-mods/kerbal?page=37" class="b-pagination-item">
    tags = soup.find_all('a', href=re.compile('^/ksp-mods/kerbal\?page\=[0-9][0-9]'))

    # Regexp to search for a two digit number (e.g. "37")
    p = re.compile('[0-9][0-9]')

    # If a match on a two digit number is found, return the number, else 'False' will be returned
    pages = False
    for item in tags:
        match = p.search(str(item))
        if match:
            pages = match.group()
    return pages

def get_curse_mods(soup):
    """Parses the BeautifulSoup object and returns a dict of mods."""

    # Empty dict to hold the mod data
    mods = {}

    # One UL tag per mod
    for ultag in soup.find_all('ul', 'group'):
        # Eight LI tags with data for each mod
        for litag in ultag.find_all('li'):
            mod_tag = litag.find('h4')
            if mod_tag:
                mod_name = helpers.clean_item(mod_tag.get_text())
                mod_url = 'https://mods.curse.com' + mod_tag.a.get('href')

            ksp_version_tag = litag.find_all(text=re.compile(r'Supports'))
            if ksp_version_tag:
                ksp_version = ksp_version_tag[0][10:]

        # Channge "prerelase" to "pre" to save space
        ksp_version = re.sub(r'prerelease', 'pre', ksp_version)

        # Update values after all LI tags have been analyzed

        mod_link = '<a href="' + mod_url + '">' + ksp_version + '</a>'
        mods[mod_name] = [ksp_version, mod_link]


    return mods

