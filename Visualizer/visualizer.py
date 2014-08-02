# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import subprocess
import sys
import os
import sip


if sys.platform.startswith("darwin"):
    import Foundation


class Watcher(QtCore.QThread):
    """execute subprocess and recieve stdout then send it to visualizer"""

    def __init__(self, visualizer, parent=None):
        super(Watcher, self).__init__(parent)
        self.visualizer = visualizer

    def setup(self, proc):
        """ setup python running on subprocess

        @param py python to run
        """
        self.stoped = False
        self.proc = proc

    def stop(self):
        self.stoped = True

    def run(self):
        """recieve stdout from child process"""
        # for memory leak problem
        if sys.platform.startswith("darwin"):
            Foundation.NSAutoreleasePool.alloc().init()
        for line in iter(self.proc.stdout.readline, ''):
            if self.stoped:
                return
            line = line.rstrip()
            splited = line.split(' ')
            if splited:
                prefix = splited[0]
                if prefix == "__GPIO__":
                    channel = int(splited[1])
                    state = True if splited[2] == "1" else False
                    self.visualizer.output(channel, state)
                else:
                    print line
                    self.visualizer.stdout(line)
                    continue
        self.visualizer.subprocessStoped()


class ErrWatcher(QtCore.QThread):
    """execute subprocess and recieve stderr then send it to visualizer"""

    def __init__(self, visualizer, parent=None):
        super(ErrWatcher, self).__init__(parent)
        self.visualizer = visualizer

    def setup(self, proc):
        """ setup python running on subprocess

        @param py python to run
        """
        self.stoped = False
        self.proc = proc

    def stop(self):
        self.stoped = True

    def run(self):
        """recieve stderr from child process"""
        # for memory leak problem on Mac
        if sys.platform.startswith("darwin"):
            Foundation.NSAutoreleasePool.alloc().init()
        for line in iter(self.proc.stderr.readline, ''):
            if self.stoped:
                return
            line = line.rstrip()
            self.visualizer.stderr(line)
        self.visualizer.subprocessStoped()


class GPIOVisualizer(object):

    PINS = [('3V3',     -1), ('5V0',     -1),
            ('GPIO_2',   2), ('5V0',     -1),
            ('GPIO_3',   3), ('GND',     -1),
            ('GPIO_4',   4), ('GPIO_14', 14),
            ('GND',     -1), ('GPIO_15', 15),
            ('GPIO_17', 17), ('GPIO_18', 18),
            ('GPIO_27', 27), ('GND',     -1),
            ('GPIO_22', 22), ('GPIO_23', 23),
            ('3V3',     -1), ('GPIO_24', 24),
            ('GPIO_10', 10), ('GND',     -1),
            ('GPIO_9',   9), ('GPIO_25', 25),
            ('GPIO_11', 11), ('GPIO_8',   8),
            ('GND',     -1), ('GPIO_7',   7),
            ]

    def __init__(self,  ui):
        super(GPIOVisualizer, self).__init__()
        self.ui = ui
        self.mainwindow = QtGui.QMainWindow()
        self.ui.setupUi(self.mainwindow)
        self.wathcer = Watcher(self)
        self.err_watcher = ErrWatcher(self)

        self.createGPIO(ui.gridLayoutWidget, ui.gridLayout)
        self.setButtonOpen()
        self.setButtonKill()
        self.setTextEdit(ui.textEdit)

        # @see setButtonOpen
        self.lastOpenPath = os.path.expanduser('~')

    def show(self):
        self.mainwindow.show()

    def start(self):
        """start subprocess

        @param py python to run
        """
        if self.py:
            print "start", self.py, "!!!!!"
            self.ui.stateLabel.setText("running")
            self.proc = subprocess.Popen(['python', self.py],
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE)
            self.wathcer.setup(self.proc)
            self.err_watcher.setup(self.proc)
            self.wathcer.start()
            self.err_watcher.start()

    def createGPIO(self, widget, grid):
        """place pins in grid"""
        self.pinWidgets = [None] * 30

        index = 0
        # place pins in the grid
        for pin in self.PINS:
            name = pin[0]
            gpio = pin[1]

            label_pin = self.createLabel(name)
            label_boardpin = self.createLabel(str(index+1))
            label_boardpin.setMargin(2)
            pinWidget = PinWidget(widget, gpio)
            self.pinWidgets[gpio] = pinWidget

            row = index/2
            if index % 2 == 0:
                grid.addWidget(label_pin, row, 0, 1, 1)
                grid.addWidget(label_boardpin, row, 1, 1, 1)
                grid.addWidget(pinWidget, row, 2, 1, 2)
            else:
                grid.addWidget(label_pin, row, 5, 1, 1)
                grid.addWidget(label_boardpin, row, 4, 1, 1)
                grid.addWidget(pinWidget, row, 3, 1, 2)
            index += 1

    def setButtonOpen(self):
        self.mainwindow.connect(self.ui.pushButton, QtCore.SIGNAL("clicked()"),
                                self.openFile)

    def setButtonKill(self):
        self.mainwindow.connect(self.ui.killButton, QtCore.SIGNAL("clicked()"),
                                self.killSubprocess)

    def setTextEdit(self, qtextedit):
        self.textEdit = qtextedit

    def stdout(self, line):
        self.textEdit.append(line)

    def stderr(self, line):
        """append line to textedit in red
        """
        self.textEdit.setTextColor(QtGui.QColor(0xff, 0, 0))
        self.textEdit.append(line)
        self.textEdit.setTextColor(QtGui.QColor(0, 0, 0))

    def openFile(self):
        """select a file to run as subprocess"""
        filename = QtGui.QFileDialog.getOpenFileName(self.mainwindow,
                                                     'Open file',
                                                     self.lastOpenPath)
        # convert to normal string
        filename = str(filename)
        self.py = filename
        # self.labelFileName.setText(os.path.basename(filename))
        self.lastOpenPath = os.path.dirname(filename)
        self.start()

    def killSubprocess(self):
        """" kill subprocess if it is running """
        self.proc.kill()

    def createLabel(self, name):
        """create label pin's description"""
        label = QtGui.QLabel(name)
        label.setAlignment(QtCore.Qt.AlignCenter)
        return label

    def output(self, channel, state):
        """change pin's state and repaint"""
        if self.pinWidgets is not None:
            self.pinWidgets[channel].state = state
            self.pinWidgets[channel].repaint()

    def subprocessStoped(self):
        self.ui.stateLabel.setText("waiting")


class PinWidget(QtGui.QWidget):

    is_gpio = False
    state = False

    WIDTH = 30
    HEIGHT = 30

    def __init__(self, gui, gpio):
        super(PinWidget, self).__init__(gui)
        self.setFixedWidth(self.WIDTH)
        self.setFixedHeight(self.HEIGHT)
        self.is_gpio = True if gpio >= 0 else False

    def paintEvent(self, e):
        painter = QtGui.QPainter()
        painter.begin(self)
        self.drawRectangle(painter)
        painter.end()

    def drawRectangle(self, painter):
        color = QtGui.QColor(255, 255, 255)
        painter.setPen(color)

        # draw frame
        painter.setBrush(QtGui.QColor(100, 100, 100))
        painter.drawRect(0, 0, self.WIDTH, self.HEIGHT)

        # fill inside white
        painter.setBrush(QtGui.QColor(255, 255, 255))
        painter.drawRect(2, 2, self.WIDTH-4, self.HEIGHT-4)

        # gpio
        if self.is_gpio:
            if self.state:
                painter.setBrush(QtGui.QColor(200, 0, 0))
            else:
                painter.setBrush(QtGui.QColor(120, 120, 120))
        else:
            painter.setBrush(QtGui.QColor(230, 230, 230))
        painter.drawRect(6, 6, self.WIDTH-12, self.HEIGHT-12)
