# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import subprocess
import sys
import os
import sip


if sys.platform.startswith("darwin"):
    import Foundation


class Watcher(QtCore.QThread):
    """execute subprocess and recieve stdout then send signal

    RPi.GPIOでoutputの箇所で親プロセスに向かってシグナル？を発信する
    """

    def __init__(self, visualizer, parent=None):
        super(Watcher, self).__init__(parent)
        self.visualizer = visualizer

    def setup(self, py):
        """ setup python running on subprocess

        @param py python to run
        """
        self.stoped = False
        self.py = py

    def stop(self):
        self.stoped = True

    def run(self):
        """recieve stdout from child process"""
        proc = subprocess.Popen(['python', self.py],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # for memory leak problem
        if sys.platform.startswith("darwin"):
            Foundation.NSAutoreleasePool.alloc().init()

        for line in iter(proc.stdout.readline, ''):
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

    def __init__(self, mainwindow):
        super(GPIOVisualizer, self).__init__()
        self.mainwindow = mainwindow
        self.wathcer = Watcher(self)

    def start(self):
        """start subprocess

        @param py python to run
        """
        if self.py:
            print "start", self.py, "!!!!!"
            self.wathcer.setup(self.py)
            self.wathcer.start()

    def createGPIO(self, widget, grid):

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

    def setButton(self, qbutton, qlabel):
        self.mainwindow.connect(qbutton, QtCore.SIGNAL("clicked()"),
                                self.openFile)
        self.labelFileName = qlabel

    def setTextEdit(self, qtextedit):
        self.textEdit = qtextedit

    def stdout(self, line):
        self.textEdit.append(line)

    def openFile(self):
        """select a file to run as subprocess"""
        filename = QtGui.QFileDialog.getOpenFileName(
                self.mainwindow, 'Open file', os.path.expanduser('~'))
        # self.labelFileName.setText(filename)
        filename = str(filename)        #convert to normal string
        self.py = filename              #start subprocess!!
        self.labelFileName.setText(os.path.basename(filename))
        self.start()

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