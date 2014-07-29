from visualizer import GPIOVisualizer
import sys
from PyQt4 import QtGui

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    v = GPIOVisualizer()
    v.show()
    v.start('example.py')
    sys.exit(app.exec_())
