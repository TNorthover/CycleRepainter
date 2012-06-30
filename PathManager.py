from PySide import QtCore, QtGui
from PySide.QtCore import Qt, QModelIndex

from Path import Path

class PathManager(QtCore.QAbstractTableModel):
    COLUMN_TITLES = ['Name', 'Initial Sheet', 'Visible']

    def __init__(self, path_table):
        super(PathManager, self).__init__()

        self.path_table = path_table
        self.paths = []
        self.visibilities = []
        self.names = []

    ##################################################################
    # Slots
    ##################################################################        

    def removeSelectedPaths(self):
        for index in self.path_table.selectedIndexes():
            self.removeRow(index.row())

    def newPath(self):
        self.insertRow(len(self.paths))

    ##################################################################
    # QAbstractItemModel methods
    ##################################################################        

    def insertRow(self, row, parent=QModelIndex()):
        # Simple tabular view: should be no parental ambiguity
        assert parent == QModelIndex()

        self.beginInsertRows(parent, row, row)

        self.paths.insert(row, Path())
        self.visibilities.insert(row)
        self.names.insert(row, 'Temporary name')

        self.endInsertRows()

        return True

    def removeRow(self, row, parent=QModelIndex()):
        # Simple tabular view: should be no parental ambiguity
        assert parent == QModelIndex()

        self.beginRemoveRows(parent, row, row)

        del self.paths[row:row+1]
        del self.visibilities[row:row+1]
        del self.names[row:row+1]

        self.endRemoveRows()

    def rowCount(self, parent):
        return len(self.paths)

    def columnCount(self, index):
        return len(PathManager.COLUMN_TITLES)

    def data(self, index, role):
        if not index.isValid() or role != Qt.DisplayRole:
            return None

        path = self.paths[index.row()]
        if index.column() == 0:
            return self.names[index.row()]
        elif index.column() == 1:
            return self.paths[index.row()].getInitialSheet()
        elif index.column() == 2:
            return self.visibilities[index.row()]
        else:
            return None

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole or orientation == Qt.Vertical:
            return None
        
        return PathManager.COLUMN_TITLES[section]
    # setData for editability
