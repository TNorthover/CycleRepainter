#! /usr/bin/python2
import sys
from PySide import QtGui, QtCore
from PySide import QtUiTools

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

    app.exec_()

if __name__ == '__main__':
    main()
