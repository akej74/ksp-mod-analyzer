# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1018, 714)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/flying.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("QGroupBox {\n"
"        background-color:qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(235, 235, 235, 255), stop:1 rgba(255, 255, 255, 255));\n"
"        border: 1px solid gray;\n"
"        border-radius: 6px;\n"
"        border-width: 1px;\n"
"        margin-top: 0.5em;\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    left: 10px;\n"
"    padding: 0 3px 0 3px;\n"
"}\n"
"\n"
"QHeaderView::section \n"
"{\n"
"    background-color: rgb(220,255,220);\n"
"    font: 10pt \"MS Shell Dlg 2\";\n"
"    font-weight: bold;\n"
"    margin-bottom:4px;\n"
"    margin-top:2px;\n"
"}")
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout_3.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_3.setSpacing(6)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBox = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButtonUpdateSpacedock = QtWidgets.QPushButton(self.groupBox)
        self.pushButtonUpdateSpacedock.setMinimumSize(QtCore.QSize(110, 0))
        self.pushButtonUpdateSpacedock.setObjectName("pushButtonUpdateSpacedock")
        self.gridLayout.addWidget(self.pushButtonUpdateSpacedock, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.progressBarSpacedock = QtWidgets.QProgressBar(self.groupBox)
        self.progressBarSpacedock.setEnabled(True)
        self.progressBarSpacedock.setProperty("value", 0)
        self.progressBarSpacedock.setObjectName("progressBarSpacedock")
        self.gridLayout.addWidget(self.progressBarSpacedock, 0, 2, 1, 1)
        self.pushButtonCancelSpacedock = QtWidgets.QPushButton(self.groupBox)
        self.pushButtonCancelSpacedock.setMinimumSize(QtCore.QSize(110, 0))
        self.pushButtonCancelSpacedock.setObjectName("pushButtonCancelSpacedock")
        self.gridLayout.addWidget(self.pushButtonCancelSpacedock, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(344, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 1, 1, 2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem2, 2, 0, 1, 1)
        self.pushButtonUpdateCurse = QtWidgets.QPushButton(self.groupBox)
        self.pushButtonUpdateCurse.setMinimumSize(QtCore.QSize(110, 0))
        self.pushButtonUpdateCurse.setObjectName("pushButtonUpdateCurse")
        self.gridLayout.addWidget(self.pushButtonUpdateCurse, 3, 0, 1, 1)
        self.progressBarCurse = QtWidgets.QProgressBar(self.groupBox)
        self.progressBarCurse.setProperty("value", 0)
        self.progressBarCurse.setObjectName("progressBarCurse")
        self.gridLayout.addWidget(self.progressBarCurse, 3, 2, 1, 1)
        self.pushButtonCancelCurse = QtWidgets.QPushButton(self.groupBox)
        self.pushButtonCancelCurse.setMinimumSize(QtCore.QSize(110, 0))
        self.pushButtonCancelCurse.setObjectName("pushButtonCancelCurse")
        self.gridLayout.addWidget(self.pushButtonCancelCurse, 4, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(344, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 4, 1, 1, 2)
        self.gridLayout_3.addWidget(self.groupBox, 1, 0, 1, 2)
        self.groupBoxData = QtWidgets.QGroupBox(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxData.sizePolicy().hasHeightForWidth())
        self.groupBoxData.setSizePolicy(sizePolicy)
        self.groupBoxData.setObjectName("groupBoxData")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBoxData)
        self.gridLayout_4.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_4.setSpacing(6)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBoxSelectData = QtWidgets.QComboBox(self.groupBoxData)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.comboBoxSelectData.setFont(font)
        self.comboBoxSelectData.setObjectName("comboBoxSelectData")
        self.comboBoxSelectData.addItem("")
        self.comboBoxSelectData.addItem("")
        self.comboBoxSelectData.addItem("")
        self.comboBoxSelectData.addItem("")
        self.comboBoxSelectData.addItem("")
        self.horizontalLayout.addWidget(self.comboBoxSelectData)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.label_5 = QtWidgets.QLabel(self.groupBoxData)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout.addWidget(self.label_5)
        self.labelNumberOfRecords = QtWidgets.QLabel(self.groupBoxData)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.labelNumberOfRecords.setFont(font)
        self.labelNumberOfRecords.setObjectName("labelNumberOfRecords")
        self.horizontalLayout.addWidget(self.labelNumberOfRecords)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
        self.gridLayout_4.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.tableView = QtWidgets.QTableView(self.groupBoxData)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableView.sizePolicy().hasHeightForWidth())
        self.tableView.setSizePolicy(sizePolicy)
        self.tableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setObjectName("tableView")
        self.tableView.horizontalHeader().setDefaultSectionSize(180)
        self.tableView.horizontalHeader().setMinimumSectionSize(50)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.verticalHeader().setCascadingSectionResizes(False)
        self.gridLayout_4.addWidget(self.tableView, 1, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBoxData, 2, 0, 1, 4)
        spacerItem6 = QtWidgets.QSpacerItem(347, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem6, 0, 1, 1, 2)
        self.labelKSPModAnalyzer = QtWidgets.QLabel(self.centralWidget)
        self.labelKSPModAnalyzer.setMaximumSize(QtCore.QSize(300, 50))
        self.labelKSPModAnalyzer.setText("")
        self.labelKSPModAnalyzer.setPixmap(QtGui.QPixmap(":/icons/ksp_mod_analyzer.png"))
        self.labelKSPModAnalyzer.setScaledContents(True)
        self.labelKSPModAnalyzer.setObjectName("labelKSPModAnalyzer")
        self.gridLayout_3.addWidget(self.labelKSPModAnalyzer, 0, 0, 1, 1)
        self.labelFlyingKerbal = QtWidgets.QLabel(self.centralWidget)
        self.labelFlyingKerbal.setMaximumSize(QtCore.QSize(50, 60))
        self.labelFlyingKerbal.setText("")
        self.labelFlyingKerbal.setPixmap(QtGui.QPixmap(":/icons/flying.png"))
        self.labelFlyingKerbal.setScaledContents(True)
        self.labelFlyingKerbal.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelFlyingKerbal.setObjectName("labelFlyingKerbal")
        self.gridLayout_3.addWidget(self.labelFlyingKerbal, 0, 3, 1, 1)
        self.groupBoxStatus = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBoxStatus.setObjectName("groupBoxStatus")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBoxStatus)
        self.gridLayout_2.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.groupBoxStatus)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.labelLastUpdateSpacedock = QtWidgets.QLabel(self.groupBoxStatus)
        self.labelLastUpdateSpacedock.setObjectName("labelLastUpdateSpacedock")
        self.gridLayout_2.addWidget(self.labelLastUpdateSpacedock, 1, 1, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem7, 2, 0, 1, 1)
        self.labelSpacedockMods = QtWidgets.QLabel(self.groupBoxStatus)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.labelSpacedockMods.setFont(font)
        self.labelSpacedockMods.setObjectName("labelSpacedockMods")
        self.gridLayout_2.addWidget(self.labelSpacedockMods, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBoxStatus)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBoxStatus)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 4, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBoxStatus)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 3, 0, 1, 1)
        self.labelCurseMods = QtWidgets.QLabel(self.groupBoxStatus)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.labelCurseMods.setFont(font)
        self.labelCurseMods.setObjectName("labelCurseMods")
        self.gridLayout_2.addWidget(self.labelCurseMods, 3, 1, 1, 1)
        self.labelLastUpdateCurse = QtWidgets.QLabel(self.groupBoxStatus)
        self.labelLastUpdateCurse.setObjectName("labelLastUpdateCurse")
        self.gridLayout_2.addWidget(self.labelLastUpdateCurse, 4, 1, 1, 1)
        self.gridLayout_3.addWidget(self.groupBoxStatus, 1, 2, 1, 2)
        self.groupBoxData.raise_()
        self.groupBox.raise_()
        self.groupBoxStatus.raise_()
        self.labelKSPModAnalyzer.raise_()
        self.labelFlyingKerbal.raise_()
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Update"))
        self.pushButtonUpdateSpacedock.setText(_translate("MainWindow", "Update Spacedock"))
        self.pushButtonCancelSpacedock.setText(_translate("MainWindow", "Cancel"))
        self.pushButtonUpdateCurse.setText(_translate("MainWindow", "Update Curse"))
        self.pushButtonCancelCurse.setText(_translate("MainWindow", "Cancel"))
        self.groupBoxData.setTitle(_translate("MainWindow", "Data"))
        self.comboBoxSelectData.setItemText(0, _translate("MainWindow", "All mods"))
        self.comboBoxSelectData.setItemText(1, _translate("MainWindow", "All mods on SpaceDock"))
        self.comboBoxSelectData.setItemText(2, _translate("MainWindow", "All mods on Curse"))
        self.comboBoxSelectData.setItemText(3, _translate("MainWindow", "Mods only on SpaceDock"))
        self.comboBoxSelectData.setItemText(4, _translate("MainWindow", "Mods only on Curse"))
        self.label_5.setText(_translate("MainWindow", "Mods currently displayed"))
        self.labelNumberOfRecords.setText(_translate("MainWindow", "---"))
        self.groupBoxStatus.setTitle(_translate("MainWindow", "Status"))
        self.label.setText(_translate("MainWindow", "SpaceDock mods"))
        self.labelLastUpdateSpacedock.setText(_translate("MainWindow", "<N/A>"))
        self.labelSpacedockMods.setText(_translate("MainWindow", "<N/A>"))
        self.label_2.setText(_translate("MainWindow", "Last updated"))
        self.label_3.setText(_translate("MainWindow", "Last updated"))
        self.label_4.setText(_translate("MainWindow", "Curse mods"))
        self.labelCurseMods.setText(_translate("MainWindow", "<N/A>"))
        self.labelLastUpdateCurse.setText(_translate("MainWindow", "<N/A>"))

from . import resources_rc
