# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'visualizer.ui'
#
# Created: Sun Aug  3 03:09:25 2014
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 20, 361, 531))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(400, 10, 76, 32))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.textEdit = QtGui.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(400, 80, 391, 471))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.subprocLabel = QtGui.QLabel(self.centralwidget)
        self.subprocLabel.setGeometry(QtCore.QRect(470, 50, 321, 21))
        self.subprocLabel.setText(_fromUtf8(""))
        self.subprocLabel.setObjectName(_fromUtf8("subprocLabel"))
        self.argvTextEdit = QtGui.QPlainTextEdit(self.centralwidget)
        self.argvTextEdit.setGeometry(QtCore.QRect(580, 15, 211, 21))
        self.argvTextEdit.setObjectName(_fromUtf8("argvTextEdit"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(550, 15, 31, 20))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.stateLabel = QtGui.QLabel(self.centralwidget)
        self.stateLabel.setGeometry(QtCore.QRect(400, 50, 61, 21))
        self.stateLabel.setObjectName(_fromUtf8("stateLabel"))
        self.killButton = QtGui.QPushButton(self.centralwidget)
        self.killButton.setGeometry(QtCore.QRect(470, 10, 76, 32))
        self.killButton.setObjectName(_fromUtf8("killButton"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "GPIOVisualizer", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "argv", None, QtGui.QApplication.UnicodeUTF8))
        self.stateLabel.setText(QtGui.QApplication.translate("MainWindow", "waiting", None, QtGui.QApplication.UnicodeUTF8))
        self.killButton.setText(QtGui.QApplication.translate("MainWindow", "Kill", None, QtGui.QApplication.UnicodeUTF8))

