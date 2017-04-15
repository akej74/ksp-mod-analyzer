"""
    spacedock.py
    -----------
    Implements functions for parsing SpaceDock using the SpaceDock API.
    For details on the API see https://github.com/KSP-SpaceDock/SpaceDock/blob/dev/api.md
"""

import sys

import requests
from PyQt5 import QtCore

import helpers

# How many mods to get on each page from SpaceDock API (30-500)
MODS_PER_PAGE = 100

class SpacedockThread(QtCore.QThread):
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

    def __del__(self):
        self.wait()

    def stop(self):
        """Stops the running thread gracefully."""

        print("Stopping SpaceDock thread...")
        self.keep_running = False

        # Wait for the thread to stop
        self.wait()
        self.cancelled_signal.emit("spacedock")
        print("SpaceDock thread stopped")

    def run(self):
        """Main thread processing loop."""

        self.keep_running = True

        try:
            print("Starting SpaceDock thread...")
            # Get data from SpaceDock and update database
            self.update_spacedock()

            # Update database table 'Total'
            helpers.update_total_mods(self.db_file)

            # Only emit finished signal if job was not cancelled (i.e. 'keep_running' is still True)
            if self.keep_running:
                self.finished_signal.emit("spacedock")

        # Exception handling:
        # Emits a signal if an exception occurs in the running thread
        # The main application will then show an error message about the problem
        # This is needed because a new message box widget cannot be created/displayed in the thread
        except Exception as e:
            # Stop the thread
            self.stop()
            print("SpaceDock thread stopped at exception")
            print()

            # Get info about the exception
            (type, value, traceback) = sys.exc_info()

            # Generate a detailed error message
            msg = helpers.exception_message_qthread(type, value, traceback)

            # Emit a signal with the error message to be displayed in a message box in the main UI
            self.exception_signal.emit(msg)

    def update_spacedock(self):
        """Updates the database with data from SpaceDock."""

        # Get the SpaceDock data
        # "spacedock_data" is a dictionary containing all sub-pages with mods in JSON format

        # Check if cached data on disk should be used (for testing purposes)
        if self.use_cache:
            spacedock_data = helpers.read_from_disk("spacedock.data")
        else:
            spacedock_data = self.parse_spacedock()
            helpers.write_to_disk("spacedock.data", spacedock_data)

        if self.keep_running:
            # Empty list to hold all mods
            #mod_list = []
            # Empty dict to hold all mod data
            mods = {}

            # Get all mods from each sub-page and store them in the dict
            for key, value in spacedock_data.items():
                page = value.json()
                for mod in page['result']:
                    mod_name = helpers.clean_item(mod['name'])
                    ksp_version = mod['versions'][0]['game_version']
                    last_updated = 'N/A'  # Not available from SpaceDock API
                    source = mod['source_code']
                    #if not source:
                    #    source = 'N/A'

                    # Update dict
                    mods[mod_name] = [ksp_version, last_updated, source]

            # Update the database
            helpers.update_db('SpaceDock', mods, self.db_file)

    def parse_spacedock(self):
        """Requests SpaceDock for all mods using the API and returns a dictionary with the data in JSON format."""

        # Set initial value (3%) for progress bar to indicate processing has started
        self.notify_progress_signal.emit(3)

        # Initial request to SpaceDock API
        req = "https://spacedock.info/api/browse?count=" + str(MODS_PER_PAGE)

        # Empty dictionary to store the mod data
        mod_data = {}

        try:
            if self.keep_running:
                # Get the first page of mods
                print("Getting first page with request", req)
                response = requests.get(req)

                # Store the first page of mod data in the dictionary
                mod_data[1] = response

                # Another check is needed in case the thread was stopped while the HTTP request was running
                if self.keep_running:
                    # Update progress bar to indicate first page received, number of pages are still unknown
                    self.notify_progress_signal.emit(10)

                # Decode JSON data that will be used to check how many sub pages there are
                spacedock_data = response.json()

                # Number of pages as returned from SpaceDock API
                pages = spacedock_data["pages"]
                print("Pages to get:", pages)

                # Calculate the progress bar interval based on number of pages
                progress_bar_interval = 100 / int(pages)

                # Request SpaceDock for each page available and store the result in the dictionary
                # Start from page 2 as the first page has already been retrieved
                for page in range(2, pages + 1):
                    if self.keep_running:
                        # Create the URL to fetch each page
                        req = "https://spacedock.info/api/browse?page=" + str(page) + "&count=" + str(MODS_PER_PAGE)

                        # Fetch page
                        mod_data[page] = requests.get(req)

                        # Another check is needed in case the thread was stopped while the HTTP request was running
                        if self.keep_running:
                            # Update progress bar
                            self.notify_progress_signal.emit(progress_bar_interval * page)
                    else:
                        break
        except:
            # Raise any exception to be handled by the QThread
            raise

        return mod_data


