import visualizer
import sys
from PyQt4 import QtGui
import ui_mainwindow

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainwindow = QtGui.QMainWindow()
    ui = ui_mainwindow.Ui_MainWindow()
    ui.setupUi(mainwindow)

    visualizer = visualizer.GPIOVisualizer(mainwindow)

    visualizer.createGPIO(ui.gridLayoutWidget,
                          ui.gridLayout)

    visualizer.setButton(ui.pushButton, ui.label)
    visualizer.setTextEdit(ui.textEdit)

    mainwindow.show()

    sys.exit(app.exec_())
