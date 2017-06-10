"""
    curse.py
    -----------
    Implements functions for parsing the CKAN repo.
"""

import json
import sys
import tarfile
from collections import defaultdict

import helpers
import requests
from PyQt5 import QtCore

CKAN_REPO = 'https://github.com/KSP-CKAN/CKAN-meta/archive/master.tar.gz'


class CKANThread(QtCore.QThread):
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

        print('Stopping CKAN thread...')
        self.keep_running = False

        # Wait for the thread to stop
        self.wait()
        self.notify_progress_signal.emit(0)
        self.cancelled_signal.emit('ckan')
        print('CKAN thread stopped')

    def run(self):
        """Main thread processing loop."""

        self.keep_running = True

        try:
            print('Starting CKAN thread...')
            # Get data from CKAN repo and update database
            self.update_ckan()

            # Update database table 'Total'
            helpers.update_total_mods(self.db_file)

            # Only emit signals if job was not cancelled (i.e. 'keep_running' is still True)
            if self.keep_running:
                self.notify_progress_signal.emit(100)
                self.finished_signal.emit('ckan')

        # Exception handling:
        # Emits a signal if an exception occurs in the running thread
        # The main application will then show an error message about the problem
        # This is needed because a new message box widget cannot be created/displayed in the thread
        except Exception as e:
            # Stop the thread
            self.stop()
            print('CKAN thread stopped at exception')

            # Get info about the exception
            (type, value, traceback) = sys.exc_info()

            # Generate a detailed error message
            msg = helpers.exception_message_qthread(type, value, traceback)

            # Emit a signal with the error message to be displayed in a message box in the main UI
            self.exception_signal.emit(msg)

    def update_ckan(self):
        """Updates the database with data from CKAN repo."""

        # Check if cached data on disk should be used
        if self.use_cache:
            # Read raw mod list from disk
            raw_mods = helpers.read_from_disk('data/ckan.data')

        else:
            # Download the CKAN repo (tar file)
            self.download_ckan(CKAN_REPO)

            raw_mods = process_ckan('data/master.tar.gz')

            # Write raw mods data to file
            helpers.write_to_disk('data/ckan.data', raw_mods)

        # TODO: Process and sort raw mods
        #print_raw_mod(raw_mods, 'ShuttleLiftingBodyCormorantAeronology')

        raw_mods_filtered = filter_raw_mods(raw_mods)

        # Iterate over each mod id
        for id in sorted(raw_mods_filtered.keys(), key=str.lower):
            #print('##### ID "{}" #####'.format(id))

            mod_versions = sorted(raw_mods_filtered[id].keys())
            highest_mod_version = helpers.get_highest_version(mod_versions)

    def download_ckan(self, url):
        """Downloads the CKAN repo."""

        print('Downloading CKAN repo...')

        progress_value = 3
        self.notify_progress_signal.emit(progress_value)

        r = requests.get(url, stream=True)
        with open('data/master.tar.gz', 'wb') as f:
            for chunk in r.iter_content(chunk_size=20000):
                progress_value += 1
                # Prevent signal from beeing emitted if the run was cancelled
                if self.keep_running:
                    self.notify_progress_signal.emit(progress_value)
                f.write(chunk)
            print('CKAN repo downloaded')
            print()

def process_ckan(file_name):
    """Processes the CKAN repo file and returns a dict of raw mods data."""

    raw_mods = defaultdict(dict)

    # Open the GZ compressed tar file for reading
    with tarfile.open(file_name, 'r:gz') as tar:
        for tarinfo in tar:
            # Check if it's a regular file
            if tarinfo.isfile():
                # Only process CKAN data files
                if tarinfo.name.endswith('.ckan') or tarinfo.name.endswith('.kerbalstuff'):
                    try:
                        jsondata = json.loads(str(tar.extractfile(tarinfo).read(), 'utf-8'))

                        if 'identifier' in jsondata:
                            identifier = jsondata['identifier']
                        else:
                            print('Identifier missing for file', tarinfo.name)
                            continue
                        if 'version' in jsondata:
                            mod_version = jsondata['version']
                        else:
                            print('Mod version missing for file', tarinfo.name)
                            continue
                        if 'name' in jsondata:
                            mod_name = helpers.clean_item(jsondata['name'])
                        else:
                            print('Mod name missing for file', tarinfo.name)
                            continue

                        # Get supported KSP version
                        if 'ksp_version' in jsondata:
                            ksp_version = jsondata['ksp_version']
                        elif 'ksp_version_max' in jsondata:
                            ksp_version = jsondata['ksp_version_max']
                        elif 'ksp_version_min' in jsondata and not 'ksp_version_max' in jsondata:
                            ksp_version = jsondata['ksp_version_min'] + '+'
                        else:
                            ksp_version = 'any'

                        # Get link to KSP forum and/or source code repositories (e.g. GitHub) if available
                        forum = ''
                        source = ''
                        kerbalstuff = ''
                        spacedock = ''
                        if 'resources' in jsondata:
                            if 'homepage' in jsondata['resources']:
                                forum = jsondata['resources']['homepage']
                            if 'repository' in jsondata['resources']:
                                source = jsondata['resources']['repository']
                            if 'kerbalstuff' in jsondata['resources']:
                                kerbalstuff = jsondata['resources']['kerbalstuff']
                            if 'spacedock' in jsondata['resources']:
                                spacedock = jsondata['resources']['spacedock']

                        # Each mod, identified by 'identifier' may have one or more mod versions
                        # Data for each mod version is stored in the nested dict 'raw_mods'
                        raw_mods[identifier][mod_version] = [ksp_version, mod_name, source, forum, kerbalstuff, spacedock]

                    except ValueError as e:
                        print('Error reading JSON data', e, 'file', tarinfo.name)
                else:
                    pass
                    #print('Not a .ckan or .kerbalstuff file', tarinfo.name)
    return raw_mods

def filter_raw_mods(raw_mods):
    """For each mod, filter out the mod versions that have the highest KSP version for that mod, simplifying 
    sorting of mod versions later on.
    
    E.g. 
        Mod version "0.5pre" with KSP version 0.90
        Mod version "1.0" with KSP version 1.1.3
        Mod version "1.1" with KSP version 1.2.2
        Mod version "1.2" with KSP version 1.2.2
        
        -> Filtered mod versions: 1.1 and 1.2
    
    Data structure for "raw_mods":
    raw_mods[identifier][mod_version] = [ksp_version, mod_name, source, forum]
    """

    raw_mods_filtered = defaultdict(dict)
    all_ksp_versions = []
    all_mod_versions = []

    for id in sorted(raw_mods.keys()):
        ksp_versions = []

        # Iterate over all mod versions and store the corresponding KSP version
        for mod_version in raw_mods[id].keys():
            ksp_versions.append(raw_mods[id][mod_version][0])
            all_mod_versions.append(mod_version)

        # Highest KSP version is the last element in the sorted list
        highest_ksp_version = sorted(ksp_versions)[-1]

        # Iterate over all mod versions again and store the mod versions that have the highest KSP version
        for mod_version in raw_mods[id].keys():
            if raw_mods[id][mod_version][0] == highest_ksp_version:
                all_ksp_versions.append((raw_mods[id][mod_version][0]))
                raw_mods_filtered[id][mod_version] = raw_mods[id][mod_version]

    return raw_mods_filtered







