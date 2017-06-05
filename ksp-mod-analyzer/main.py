"""
    main.py
    --------------
    This is the main module of KSP Mod Analyzer. Implements the UI and business logic.
"""

import os
import sys

from PyQt5 import QtCore, QtWidgets, QtSql

import ckan
import curse
import helpers
import settings
import spacedock
from ui.mainwindow import Ui_MainWindow

PROGRAM_VERSION = '1.1.0'
DATA_DIR = 'data'

# DISK_CACHE = True disables web parsing and reads data from a previous run from disk (for debugging)
DISK_CACHE = False

class KspModAnalyzer(QtWidgets.QMainWindow):
    """Creates the UI, based on PyQt5.

    The UI elements are defined in "mainwindow.py" and resource file "resources_rc.py", both created in QT Designer.

    To update "mainwindow.py":
        Run "pyuic5.exe --from-imports mainwindow.ui -o mainwindow.py"

    To update "resources_rc.py":
        Run "pyrcc5.exe resources.qrc -o resource_rc.py"

    Note: Never modify "mainwindow.py" or "resource_rc.py" manually.
    """

    def __init__(self):
        super().__init__()

        # Create the main window
        self.ui = Ui_MainWindow()

        # Set upp the UI
        self.ui.setupUi(self)

        # Create data directory
        os.makedirs(DATA_DIR, exist_ok=True)

        # SQLite database file
        self.db_file = 'data/database.db'

        # Define QSqlDatabase
        self.qt_db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.qt_db.setDatabaseName(self.db_file)

        # QSettings object for storing the UI configuration in the OS native repository (Registry for Windows, ini-file for Linux)
        # In Windows, parameters will be stored at HKEY_CURRENT_USER/SOFTWARE/KSP_Mod_Analyzer/App
        self.config = QtCore.QSettings('KSP_Mod_Analyzer', 'App')

        # Read saved UI configuration
        settings.read_settings(self.config, self.ui)

        # Initialize database
        helpers.init_database(self.db_file)

        # QThreads for fetching data from SpaceDock, Curse and CKAN
        self.spacedock_thread = spacedock.SpacedockThread(db_file=self.db_file, use_cache=DISK_CACHE)
        self.curse_thread = curse.CurseThread(db_file=self.db_file, use_cache=DISK_CACHE)
        self.ckan_thread = ckan.CKANThread(db_file=self.db_file, use_cache=DISK_CACHE)

        # Connect signals and slots and initialize UI values
        self.setup_ui_logic()

        # Update 'Status' group box
        self.update_status()


    def setup_ui_logic(self):
        """Defines QT signal and slot connections and initializes UI values."""

        # Connect push button events
        self.ui.pushButtonSpacedock.clicked.connect(self.update_spacedock)
        self.ui.pushButtonCurse.clicked.connect(self.update_curse)
        self.ui.pushButtonCKAN.clicked.connect(self.update_ckan)

        # Connect combo box event and update database model with current selected value in the combo box
        self.ui.comboBoxSelectData.currentIndexChanged.connect(
            lambda: self.update_db_model(self.ui.comboBoxSelectData.currentText()))

        # Connect exception signals to show an exception message from running threads,
        # This is needed as it's not possible to show a message box widget from the QThread directly
        self.spacedock_thread.exception_signal.connect(self.thread_exception_handling)
        self.curse_thread.exception_signal.connect(self.thread_exception_handling)
        self.ckan_thread.exception_signal.connect(self.thread_exception_handling)

        # Connect finished signals
        self.spacedock_thread.finished_signal.connect(self.finished_processing)
        self.curse_thread.finished_signal.connect(self.finished_processing)
        self.ckan_thread.finished_signal.connect(self.finished_processing)

        # Connect cancelled signals
        self.spacedock_thread.cancelled_signal.connect(self.cancelled_processing)
        self.curse_thread.cancelled_signal.connect(self.cancelled_processing)
        self.ckan_thread.cancelled_signal.connect(self.cancelled_processing)

        # Connect progress bar signals
        self.spacedock_thread.notify_progress_signal.connect(lambda i: self.ui.progressBarSpacedock.setValue(i))
        self.curse_thread.notify_progress_signal.connect(lambda i: self.ui.progressBarCurse.setValue(i))
        self.ckan_thread.notify_progress_signal.connect(lambda i: self.ui.progressBarCKAN.setValue(i))

        # Update data model for the QTableView
        self.update_db_model(self.ui.comboBoxSelectData.currentText())

    def update_spacedock(self):
        """Updates the UI and starts SpaceDock processing thread."""

        # Change functionality of "Update SpaceDock" button to "Cancel"
        self.ui.pushButtonSpacedock.disconnect()
        self.ui.pushButtonSpacedock.clicked.connect(self.spacedock_thread.stop)
        self.ui.pushButtonSpacedock.setText('Cancel')

        self.spacedock_thread.start()

    def update_curse(self):
        """Updates the UI and starts SpaceDock processing thread."""

        # Change functionality of "Update Curse" button to "Cancel"
        self.ui.pushButtonCurse.disconnect()
        self.ui.pushButtonCurse.clicked.connect(self.curse_thread.stop)
        self.ui.pushButtonCurse.setText('Cancel')

        self.curse_thread.start()

    def update_ckan(self):
        """Updates the UI and starts CKAN processing thread."""

        # Change functionality of "Update CKAN" button to "Cancel"
        self.ui.pushButtonCKAN.disconnect()
        self.ui.pushButtonCKAN.clicked.connect(self.ckan_thread.stop)
        self.ui.pushButtonCKAN.setText('Cancel')

        self.ckan_thread.start()

    def finished_processing(self, sender):
        """Updates the UI and database model after threads have completed the run."""

        # Update the data view
        self.update_db_model(self.ui.comboBoxSelectData.currentText())

        # Update button functionality
        if sender == 'spacedock':
            self.ui.pushButtonSpacedock.disconnect()
            self.ui.pushButtonSpacedock.clicked.connect(self.update_spacedock)
            self.ui.pushButtonSpacedock.setText('Update SpaceDock')

        if sender == 'curse':
            self.ui.pushButtonCurse.disconnect()
            self.ui.pushButtonCurse.clicked.connect(self.update_curse)
            self.ui.pushButtonCurse.setText('Update Curse')

        if sender == 'ckan':
            self.ui.pushButtonCKAN.disconnect()
            self.ui.pushButtonCKAN.clicked.connect(self.update_ckan)
            self.ui.pushButtonCKAN.setText('Update CKAN')

        # Update 'Status' group box
        self.update_status()

    def cancelled_processing(self, sender):
        """Updates the UI after a cancellation."""

        if sender == 'spacedock':
            self.ui.progressBarSpacedock.setValue(0)
            self.ui.pushButtonSpacedock.disconnect()
            self.ui.pushButtonSpacedock.clicked.connect(self.update_spacedock)
            self.ui.pushButtonSpacedock.setText('Update SpaceDock')

        if sender == 'curse':
            self.ui.progressBarCurse.setValue(0)
            self.ui.pushButtonCurse.disconnect()
            self.ui.pushButtonCurse.clicked.connect(self.update_curse)
            self.ui.pushButtonCurse.setText('Update Curse')

        if sender == 'ckan':
            self.ui.progressBarCKAN.setValue(0)
            self.ui.pushButtonCKAN.disconnect()
            self.ui.pushButtonCKAN.clicked.connect(self.update_ckan)
            self.ui.pushButtonCKAN.setText('Update CKAN')

        # Update 'Status' group box
        self.update_status()

        # Reset combo box in 'Data' view
        self.ui.comboBoxSelectData.setCurrentIndex(0)

    def update_db_model(self, query_type):
        """Defines a model view for the database, used by the QTableView.

        Called in the following situations:
            - At application start
            - The drop down box in the 'Data' field is changed
            - After data collection from SpaceDock and/or Curse
        """

        # Open the database
        # TODO: Investigate if a context manager can be used for QtSQL databases
        if not self.qt_db.open():
            raise Exception('Could not open QT database.')

        # Use the simple read-only model provided by QT
        db_model = QtSql.QSqlQueryModel()

        # Define SQL queries
        if query_type == 'All mods':
            sql = 'SELECT Mod, Spacedock, Curse, CKAN, Source, Forum FROM Total'
        elif query_type == 'All mods on SpaceDock':
            sql = 'SELECT Mod, SpaceDock, Source, Forum FROM Total WHERE SpaceDock IS NOT NULL'
        elif query_type == 'All mods on Curse':
            sql = 'SELECT Mod, Curse FROM Total WHERE Curse IS NOT NULL'
        elif query_type == 'All mods on CKAN':
            sql = 'SELECT Mod, CKAN FROM Total WHERE CKAN IS NOT NULL'
        elif query_type == 'Mods only on SpaceDock':
            sql = 'SELECT Mod, SpaceDock FROM Total WHERE Spacedock IS NOT NULL AND Curse IS NULL'
        elif query_type == 'Mods only on Curse':
            sql = 'SELECT Mod, Curse FROM Total WHERE Spacedock IS NULL AND Curse IS NOT NULL'
        else:
            self.qt_db.close()
            raise Exception('Invalid query type: "' + query_type + '" for QTableView')

        # Update the model with SQL query
        db_model.setQuery(sql, self.qt_db)

        # Configure the QTableView to use the model
        self.ui.tableView.setModel(db_model)

        # Set headers to be left aligned
        #self.ui.tableView.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)

        # Set all columns to stretch to available width
        self.ui.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # Set first column to auto resize to contents
        #self.ui.tableView.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)

        self.ui.tableView.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Interactive)
        self.ui.tableView.horizontalHeader().resizeSection(0, 350)

        self.ui.tableView.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Interactive)
        self.ui.tableView.horizontalHeader().resizeSection(1, 100)

        self.ui.tableView.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Interactive)
        self.ui.tableView.horizontalHeader().resizeSection(2, 100)

        self.ui.tableView.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Interactive)
        self.ui.tableView.horizontalHeader().resizeSection(3, 100)

        if query_type == 'All mods on SpaceDock':
            self.ui.tableView.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Interactive)
            self.ui.tableView.horizontalHeader().resizeSection(2, 300)

            self.ui.tableView.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Interactive)
            self.ui.tableView.horizontalHeader().resizeSection(3, 300)

        # Fetch all available records
        while db_model.canFetchMore():
            db_model.fetchMore()

        # Update number of mods displayed
        rows = db_model.rowCount()
        self.ui.labelNumberOfRecords.setText('<font color="Blue">' + str(rows))

        # Close database
        self.qt_db.close()

    def update_status(self):
        """Updates the data in 'Status' group box."""

        # Check if SpaceDock data file exists and update UI accordingly
        if os.path.isfile('data/spacedock.data'):
            spacedock_records = helpers.get_records('SpaceDock', self.db_file)
            spacedock_last_date = helpers.get_file_modification_time('data/spacedock.data')
            self.ui.labelSpacedockMods.setText('<font color="Blue">' + str(spacedock_records))
            self.ui.labelLastUpdateSpacedock.setText('<font color="Blue">' + str(spacedock_last_date))
        else:
            self.ui.labelSpacedockMods.setText('<font color="Red">---')
            self.ui.labelLastUpdateSpacedock.setText('<font color="Red">---')

        # Check if Curse data file exists and update UI accordingly
        if os.path.isfile('data/curse.data'):
            curse_records = helpers.get_records('Curse', self.db_file)
            curse_last_date = helpers.get_file_modification_time('data/curse.data')
            self.ui.labelCurseMods.setText('<font color="Blue">' + str(curse_records))
            self.ui.labelLastUpdateCurse.setText('<font color="Blue">' + str(curse_last_date))
        else:
            self.ui.labelCurseMods.setText('<font color="Red">---')
            self.ui.labelLastUpdateCurse.setText('<font color="Red">---')

        # Check if CKAN data file exists and update UI accordingly
        if os.path.isfile('data/master.tar.gz'):
            ckan_records = helpers.get_records('CKAN', self.db_file)
            ckan_last_date = helpers.get_file_modification_time('data/master.tar.gz')
            self.ui.labelCKANMods.setText('<font color="Blue">' + str(ckan_records))
            self.ui.labelLastUpdateCKAN.setText('<font color="Blue">' + str(ckan_last_date))
        else:
            self.ui.labelCKANMods.setText('<font color="Red">---')
            self.ui.labelLastUpdateCKAN.setText('<font color="Red">---')


    def closeEvent(self, event):
        """Saves UI settings, then exit the application.
        Called when closing the application window.
        """

        # Stop the running threads
        if self.spacedock_thread.isRunning():
            print("Stopping SpaceDock thread...")
            self.spacedock_thread.stop()

        if self.curse_thread.isRunning():
            print("Stopping Curse thread...")
            self.curse_thread.stop()

        if self.ckan_thread.isRunning():
            print("Stopping CKAN thread...")
            self.ckan_thread.stop()

        # Save UI settings
        settings.save_settings(self.config, self.ui)

        # Accept the closing event and close application
        event.accept()

    def thread_exception_handling(self, msg):
        """Displays an error message with details about the exception.
        Called when an exception occurs in a thread.
        """

        # Show error message
        helpers.show_error(msg)

if __name__ == "__main__":
    # Use a rewritten excepthook for displaying unhandled exceptions as a QMessageBox
    sys.excepthook = helpers.excepthook

    # Create the QT application
    app = QtWidgets.QApplication(sys.argv)

    # Create the main window
    win = KspModAnalyzer()

    # Set program version
    win.setWindowTitle("KSP Mod Analyzer " + PROGRAM_VERSION)

    # Show window
    win.show()

    # Start QT application
    sys.exit(app.exec_())