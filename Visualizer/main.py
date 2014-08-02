import visualizer
import sys
from PyQt4 import QtGui
import ui_mainwindow

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ui = ui_mainwindow.Ui_MainWindow()

    visualizer = visualizer.GPIOVisualizer(ui)
    #
    # visualizer.createGPIO(ui.gridLayoutWidget,
    #                       ui.gridLayout)
    #
    # visualizer.setButton(ui.pushButton, ui.label)
    # visualizer.setTextEdit(ui.textEdit)

    visualizer.show()

    sys.exit(app.exec_())
