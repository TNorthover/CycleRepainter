#! /usr/bin/python2
import sys
from PySide import QtGui, QtCore
from PySide import QtUiTools

from Controller import Controller

def load_ui():
    file = QtCore.QFile('outline.ui')
    file.open(QtCore.QFile.ReadOnly)

    loader = QtUiTools.QUiLoader()
    ui = loader.load(file)
    file.close()

    return ui

def main():
    app = QtGui.QApplication(sys.argv)

    ui = load_ui()
    c = Controller(ui)
    ui.show()

    app.lastWindowClosed.connect(app.quit)

    app.exec_()

if __name__ == '__main__':
    main()
