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


def init_database(db_file):
    """Initializes the SQLite database and creates tables if they don't exist."""

    with contextlib.closing(sqlite3.connect(db_file, timeout=1)) as con:
        print("Initializing database...")
        print()
        with con as cur:
            # Create tables
            cur.execute('CREATE TABLE IF NOT EXISTS SpaceDock (Id INTEGER PRIMARY KEY, Mod TEXT, KSP_version TEXT, Last_updated TEXT, Source TEXT)')
            cur.execute('CREATE TABLE IF NOT EXISTS Curse (Id INTEGER PRIMARY KEY, Mod TEXT, KSP_version TEXT, Last_updated TEXT, Source TEXT)')
            cur.execute('CREATE TABLE IF NOT EXISTS CKAN (Id INTEGER PRIMARY KEY, Mod TEXT, KSP_version TEXT, Last_updated TEXT, Source TEXT)')
            cur.execute('CREATE TABLE IF NOT EXISTS Total (Id INTEGER PRIMARY KEY, Mod TEXT, SpaceDock TEXT, Curse TEXT, CKAN TEXT)')

def update_total_mods(db_file):
    """Updates the 'Total' table with data from 'SpaceDock', 'Curse' and 'CKAN' tables."""

    con = sqlite3.connect(db_file, timeout=1)
    with con:
        cur = con.cursor()
        cur.execute('DELETE FROM Total')

        # Get a list of all SpaceDock mods
        cur.execute('SELECT Mod FROM SpaceDock')
        spacedock_list = [i[0] for i in cur.fetchall()]

        # Get a list of all Curse mods
        cur.execute('SELECT Mod FROM Curse')
        curse_list = [i[0] for i in cur.fetchall()]

        # Get a list of all CKAN mods
        #cur.execute('SELECT Mod FROM CKAN')
        #ckan_list = [i[0] for i in cur.fetchall()]

        # Get a sorted list of all unique mods (duplicates removed by the set)
        total_mods = sorted(set(spacedock_list + curse_list), key=str.lower)
        print("Total mods", len(total_mods))

        # Update 'Total' table with all available mods
        for mod in total_mods:
            cur.execute('INSERT INTO Total (Mod, SpaceDock, Curse, CKAN) VALUES (:mod, "Not available", "Not available", "Not available")', {'mod': mod})

        # Update 'Total' table with status of mod availability in SpaceDock, Curse and CKAN repositories
        for mod in total_mods:
            if mod in spacedock_list:
                cur.execute('UPDATE Total SET Spacedock = "OK" WHERE Mod =:mod', {'mod': mod})
            if mod in curse_list:
                cur.execute('UPDATE Total SET Curse = "OK" WHERE Mod =:mod', {'mod': mod})
            #if mod in ckan_list:
            #    cur.execute('UPDATE Total SET CKAN = "OK" WHERE Mod =:mod', {'mod': mod})

# def drop_data(table, db_file):
#     con = sqlite3.connect(db_file, timeout=1)
#     with con:
#         cur = con.cursor()
#         sql = 'DELETE FROM ' + table
#         cur.execute(sql)

def update_db(table, mods, db_file):
    """Updates the database with mod data for SpaceDock, Curse or CKAN."""

    # with contextlib.closing(sqlite3.connect(db_file, timeout=1)) as con:
    #     with con as cur:
    #         if table == "SpaceDock":
    #             print("Updating SpaceDock database...")
    #             cur.execute('DELETE FROM SpaceDock')
    #             for mod in mod_list:
    #                 cur.execute('INSERT INTO SpaceDock (Mod) VALUES (:mod)', {'mod': mod})
    #             print("SpaceDock database update complete,", len(mod_list), "mods inserted.")
    #
    #         if table == "Curse":
    #             print("Updating Curse database...")
    #             cur.execute('DELETE FROM Curse')
    #             for mod in mod_list:
    #                 cur.execute('INSERT INTO Curse (Mod) VALUES (:mod)', {'mod': mod})
    #             print("Curse database update complete,", len(mod_list), "mods inserted.")
    #
    #         if table == "CKAN":
    #             print("Updating CKAN database...")
    #             cur.execute('DELETE FROM CKAN')
    #             for mod in mod_list:
    #                 cur.execute('INSERT INTO CKAN (Mod) VALUES (:mod)', {'mod': mod})
    #             print("CKAN database update complete,", len(mod_list), "mods inserted.")

    with contextlib.closing(sqlite3.connect(db_file, timeout=1)) as con:
         with con as cur:
            if table == 'Curse':
                print("Updating Curse database...")
                cur.execute('DELETE FROM Curse')
                for mod_name in sorted(mods.keys()):
                    cur.execute('INSERT INTO Curse (Mod, KSP_version, Last_updated) VALUES (:mod, :version, :last_updated)',
                                {'mod': mod_name, 'version': mods[mod_name][0], 'last_updated': mods[mod_name][1]})





def get_records(table, db_file):
    """Gets the number of rows in a table."""

    # TODO: Rewrite this code to make it more efficient

    con = sqlite3.connect(db_file, timeout=1)
    with con:
        cur = con.cursor()
        if table == 'SpaceDock':
            cur.execute('SELECT COUNT(Mod) FROM Total WHERE SpaceDock = "OK"')
            rows = cur.fetchone()[0]

        elif table == 'Curse':
            cur.execute('SELECT COUNT(Mod) FROM Total WHERE Curse = "OK"')
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

    # Get the date in a human readable for from the timestamp
    last_modified_date = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
    return last_modified_date

def clean_list(list):
    """Cleans a list of items:
       - Remove leading and trailing whitespace
       - Remove leading version info, e.g. [x.y.z], [1.2], (0.90)
       - Sort the list non case sensitive
    """

    cleaned_list = []

    for item in list:
        # Strip leading and trailing whitespace
        clean_item = item.strip()

        # Regexp for removing all info enclosed in [] at the start of the string, e.g. [1.0.5], [1.x] etc
        regexp = re.compile(r'^\[.*?\]')
        clean_item = re.sub(regexp, '', clean_item)

        # Regexp for removing all info enclosed in () at the start of the string, e.g. (0.90) etc
        regexp = re.compile(r'^\(.*?\)')
        clean_item = re.sub(regexp, '', clean_item)

        # Strip leading and trailing whitespace again (after regexp cleaning)
        cleaned_list.append(clean_item.strip())

        # Sort the list non case sensitive
        cleaned_list.sort(key=str.lower)

    return cleaned_list

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
        pickle.dump(data, f)

def read_from_disk(filename):
    """Reads data from disk and un-serializes with pickle."""

    with open(filename, "rb") as f:
        print("Reading from file", filename)
        data = pickle.load(f)
    return data