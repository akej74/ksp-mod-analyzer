"""
    helpers.py
    ---------
    Implements various helper functions, e.g:
        - Display messages and errors using a QT Message box
        - Database management
"""

import contextlib
import io
import os
import pickle
import re
import sqlite3
import sys
import traceback
from datetime import datetime

from PyQt5 import QtCore, QtWidgets, QtGui
from natsort import natsorted


def get_highest_version(mod_versions):
    """Get the highest mod version in the mod_versions list."""

    # Epoch number
    re_epoch = re.compile(r'(^\d):')

    # Everything after epoch
    re_rest = re.compile(r'(^\d:)?(.*)')

    clean_mod_versions = []
    epochs = []

    # Get all epoch numbers if available
    for mod_version in mod_versions:
        m1 = re.match(re_epoch, mod_version)
        epoch = m1.group(1) if m1 else ''
        if epoch:
            epochs.append(epoch)

    # Get the highest epoch number
    if epochs:
        highest_epoch = sorted(epochs)[-1]
    else:
        highest_epoch = 0

    # Find all mod versions, using only the highest epoch number
    for mod_version in mod_versions:
        m1 = re.match(re_epoch, mod_version)
        m2 = re.match(re_rest, mod_version)

        epoch = m1.group(1) if m1 else ''
        rest = m2.group(2) if m2 else ''

        # Only append mod versions with highest epoch
        if epoch == highest_epoch:
            clean_mod_versions.append(rest)

        # If no epochs, just add the mod version
        if not epochs:
            clean_mod_versions.append(rest)

    highest_mod_version = natsorted(clean_mod_versions)[-1]

    if epochs:
        return highest_epoch + ':' + highest_mod_version
    else:
        return highest_mod_version

def init_database(db_file):
    """Initializes the SQLite database and creates tables if they don't exist."""

    with contextlib.closing(sqlite3.connect(db_file, timeout=1)) as con:
        print("Initializing database...")
        print()
        with con as cur:
            # Create tables
            cur.execute('CREATE TABLE IF NOT EXISTS SpaceDock '
                        '(Id INTEGER PRIMARY KEY, Mod TEXT, KSP_version TEXT, Source TEXT, Forum TEXT, Mod_Id TEXT, URL TEXT)')

            cur.execute('CREATE TABLE IF NOT EXISTS Curse '
                        '(Id INTEGER PRIMARY KEY, Mod TEXT, KSP_version TEXT, Source TEXT, Forum TEXT, URL TEXT)')

            cur.execute('CREATE TABLE IF NOT EXISTS CKAN '
                        '(Id INTEGER PRIMARY KEY, Mod TEXT, KSP_version TEXT, Source TEXT, Forum TEXT, Kerbalstuff TEXT, Spacedock TEXT)')

            cur.execute('CREATE TABLE IF NOT EXISTS Total '
                        '(Id INTEGER PRIMARY KEY, Mod TEXT, SpaceDock TEXT, Curse TEXT, CKAN TEXT, Source TEXT, Forum TEXT)')

def update_total_mods(db_file):
    """Updates the 'Total' table with data from 'SpaceDock', 'Curse' and 'CKAN' tables."""

    con = sqlite3.connect(db_file, timeout=1)
    with con:
        cur = con.cursor()
        cur.execute('DELETE FROM Total')

        # Get a list of all SpaceDock mods
        cur.execute('SELECT Mod, KSP_version, Source, Forum, URL FROM SpaceDock')
        spacedock = {i[0]: [i[1], i[2], i[3], i[4]] for i in cur.fetchall()}

        # Get a list of all Curse mods
        cur.execute('SELECT Mod, KSP_version, Source, Forum, URL FROM Curse')
        curse = {i[0]: [i[1], i[2], i[3], i[4]] for i in cur.fetchall()}

        # TODO: Add CKAN

        # Get a sorted list of all unique mods (duplicates removed by the set)
        total_mods = sorted(set(list(spacedock.keys()) + list(curse.keys())), key=str.lower)
        print("Total mods", len(total_mods))

        # Initlialize 'Total' table with all available mods
        for mod in total_mods:
            cur.execute('INSERT INTO Total (Mod) '
                        'VALUES (:mod)',
                        {'mod': mod})

        # Update 'Total' table with status of mod availability in SpaceDock, Curse and CKAN repositories
        for mod in total_mods:
            if mod in spacedock.keys():
                cur.execute('UPDATE Total '
                            'SET Spacedock =:version_link, Source =:source, Forum =:forum '
                            'WHERE Mod =:mod',
                            {'mod': mod,
                             'version_link': spacedock[mod][3],
                             'source': spacedock[mod][1],
                             'forum': spacedock[mod][2]})
            if mod in curse.keys():
                cur.execute('UPDATE Total '
                            'SET Curse =:version_link '
                            'WHERE Mod =:mod',
                            {'mod': mod,
                             'version_link': curse[mod][3]})

def update_db(table, mods, db_file):
    """Updates the database with mod data for SpaceDock, Curse or CKAN."""

    with contextlib.closing(sqlite3.connect(db_file, timeout=1)) as con:
         with con as cur:
            if table == 'Curse':
                print("Updating Curse database...")
                cur.execute('DELETE FROM Curse')
                for mod_name in sorted(mods.keys(), key=str.lower):
                    cur.execute('INSERT INTO Curse (Mod, KSP_version, URL) '
                                'VALUES (:mod, :version, :url)',
                                {'mod': mod_name,
                                 'version': mods[mod_name][0],
                                 'url':mods[mod_name][1]})

            if table == 'SpaceDock':
                print("Updating SpaceDock database...")
                cur.execute('DELETE FROM SpaceDock')
                for mod_name in sorted(mods.keys(), key=str.lower):
                    cur.execute('INSERT INTO SpaceDock (Mod, KSP_version, Source, Forum, Mod_Id, URL) '
                                'VALUES (:mod, :version, :source, :forum, :mod_id, :url)',
                                {'mod': mod_name,
                                 'version': mods[mod_name][0],
                                 'source': mods[mod_name][1],
                                 'forum': mods[mod_name][2],
                                 'mod_id': mods[mod_name][3],
                                 'url': mods[mod_name][4]})

            if table == 'CKAN':
                # raw_mods[identifier][mod_version] = [ksp_version, mod_name, source, forum, kerbalstuff, spacedock]
                print("Updating CKAN database...")
                cur.execute('DELETE FROM CKAN')
                for mod_name in sorted(mods.keys(), key=str.lower):
                    cur.execute('INSERT INTO Curse (Mod, KSP_version, Source, Forum) '
                                'VALUES (:mod, :version, :source, :forum)',
                                {'mod': mod_name,
                                 'version': mods[mod_name][0],
                                 'source': mods[mod_name][1],
                                 'forum': mods[mod_name][2]})

def get_records(table, db_file):
    """Gets the number of rows in a table."""

    con = sqlite3.connect(db_file, timeout=1)
    with con:
        cur = con.cursor()
        if table == 'SpaceDock':
            cur.execute('SELECT COUNT(Mod) FROM Total WHERE SpaceDock IS NOT NULL')
            rows = cur.fetchone()[0]
        elif table == 'Curse':
            cur.execute('SELECT COUNT(Mod) FROM Total WHERE Curse IS NOT NULL')
            rows = cur.fetchone()[0]
        elif table == 'CKAN':
            cur.execute('SELECT COUNT(Mod) FROM Total WHERE CKAN IS NOT NULL')
            rows = cur.fetchone()[0]
        else:
            return 0

        return rows

def get_file_modification_time(file_name):
    """Gets the 'last modification' date and time for a file."""

    try:
        mtime = os.path.getmtime(file_name)
    except OSError:
        return False

    # Get the date in a human readable form from the timestamp
    last_modified_date = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
    return last_modified_date

def clean_item(item):
    """Cleans an item (string):
       - Remove leading and trailing whitespace
       - Remove leading version info, e.g. [x.y.z], [1.2], (0.90)
    """

    # Strip leading and trailing whitespace
    cleaned_item = item.strip()

    # Regexp for removing all info enclosed in [] at the start of the string, e.g. [1.0.5], [1.x] etc
    regexp = re.compile(r'^\[.*?\]')
    cleaned_item = re.sub(regexp, '', cleaned_item)

    # Regexp for removing all info enclosed in () at the start of the string, e.g. (0.90) etc
    regexp = re.compile(r'^\(.*?\)')
    cleaned_item = re.sub(regexp, '', cleaned_item)

    # Strip leading and trailing whitespace again (after regexp cleaning)
    cleaned_item = cleaned_item.strip()

    return cleaned_item

def excepthook(excType, excValue, tracebackobj):
    """Rewritten "excepthook", to display a message box with details about the unhandled exception.

    @param excType exception type
    @param excValue exception value
    @param tracebackobj traceback object
    """
    separator = '-' * 40
    notice = "An unhandled exception has occurred\n"

    tbinfofile = io.StringIO()
    traceback.print_tb(tracebackobj, None, tbinfofile)
    tbinfofile.seek(0)
    tbinfo = tbinfofile.read()
    errmsg = '%s: \n%s' % (str(excType), str(excValue))
    sections = [separator, errmsg, separator, tbinfo]
    msg = '\n'.join(sections)

    # Create a QMessagebox
    error_box = QtWidgets.QMessageBox()

    error_box.setText(str(notice)+str(msg))
    error_box.setWindowTitle("KSP Mod Analyzer - unhandled exception")
    error_box.setIcon(QtWidgets.QMessageBox.Critical)
    error_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
    error_box.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

    # Show the window
    error_box.exec_()

    # Exit the application
    sys.exit(1)

def exception_message_qthread(excType, excValue, tracebackobj):
    """Get exception details, called when an exception occurs in a QThread."""

    separator = '-' * 40
    notice = "An exception occurred in the running thread!\n"

    tbinfofile = io.StringIO()
    traceback.print_tb(tracebackobj, None, tbinfofile)
    tbinfofile.seek(0)
    tbinfo = tbinfofile.read()
    errmsg = '%s: \n%s' % (str(excType), str(excValue))
    sections = [notice, separator, errmsg, separator, tbinfo]
    msg = '\n'.join(sections)

    return msg

def show_error(message):
    """Displays "message" in a "Critical error" message box with 'OK' button."""

    # Create a QMessagebox
    message_box = QtWidgets.QMessageBox()

    message_box.setText(str(message))
    message_box.setWindowTitle("Error")
    message_box.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(":/icons/flying.png")))
    message_box.setIcon(QtWidgets.QMessageBox.Critical)
    message_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
    message_box.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

    #Show the window
    message_box.exec_()

def show_notification(message):
    """Displays "message" in a "Information" message box with 'OK' button."""

    # Create a QMessagebox
    message_box = QtWidgets.QMessageBox()

    message_box.setText(message)
    message_box.setWindowTitle("Note")
    message_box.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(":/icons/grid.png")))
    message_box.setIcon(QtWidgets.QMessageBox.Information)
    message_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
    message_box.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

    #Show the window
    message_box.exec_()

def write_to_disk(filename, data):
    """Serializes data with pickle and writes to disk."""

    with open(filename, "wb") as f:
        print("Writing file", filename)
        print()
        pickle.dump(data, f)

def read_from_disk(filename):
    """Reads data from disk and un-serializes with pickle."""

    with open(filename, "rb") as f:
        print("Reading from file", filename)
        print()
        data = pickle.load(f)
    return data

def dump(obj):
    """Print details about an object."""

    for attr in dir(obj):
        if hasattr(obj, attr):
            print('##### Object details #####')
            print(obj)
            print('--------------------------')
            print("obj.%s = %s" % (attr, getattr(obj, attr)))
            print()