from PySide.QtGui import QGraphicsItem, QGraphicsEllipseItem, QGraphicsLineItem

from PySide.QtGui import QPen, QBrush
from PySide.QtCore import QRectF, QPointF, QLineF
from PySide.QtCore import Qt, QObject
from PySide import QtCore

class CentralSurfaceRenderer(QObject):
    centralPointMoved = QtCore.Signal(QPointF)

    def __init__(self, scene, surface):
        super(CentralSurfaceRenderer, self).__init__()
        self.scene = scene
        self.surface = surface
        self.items = []
        self.lines = []
        self.centre = QPointF()

        self.edit_mode = True

    def surfaceOrProjectionChanged(self, surface):
        self.surface = surface
        self.branches = self.surface.finiteBranchPoints()

        # First remove all existing data
        map(self.scene.removeItem, self.items)
        self.items = []

        self._addItems()

    def setEditMode(self, editing):
        self.edit_mode = editing

        map(self.scene.removeItem, self.items)
        self.items = []
        self._addItems()

    def _addItems(self):
        cutPen = self._cutPen()

        dotBrush = QBrush(Qt.black)
        radius = self._branchRadius()

        e = CentralPoint(self, self.centre, edit_mode=self.edit_mode)
        self.scene.addItem(e)
        self.items.append(e)

        for branch in self.branches:
            # FIXME: Arbitrary centre
            l = self.scene.addLine(QLineF(self.centre, 
                                          QPointF(branch.real, branch.imag)))
            l.setPen(cutPen)
            self.items.append(l)
            self.lines.append(l)

            dot = self.scene.addEllipse(branch.real - radius,
                                        branch.imag - radius, 
                                        2*radius, 2*radius)
            dot.setBrush(dotBrush)
            dot.setPen(QPen(QBrush(), 0))
            self.items.append(dot)

    def _cutPen(self):
        if self.edit_mode:
            pen = QPen()
            pen.setWidthF(0.03)
            return pen
        else:
            pen = QPen(Qt.gray)
            pen.setWidthF(0.02)
            return pen

    def _branchRadius(self):
        if self.edit_mode:
            return 0.1
        else:
            return 0.05


class CentralPoint(QGraphicsEllipseItem):
    def __init__(self, renderer, centre, edit_mode):
        super(CentralPoint, self).__init__()

        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setZValue(1)
       
        self.renderer = renderer
        self.setPos(self.renderer.centre)

        self.setEditMode(edit_mode)

    def setEditMode(self, editing):
        if editing:
            self._setRadius(0.15)
            self.setBrush(QBrush(Qt.darkGreen))
            self.setFlag(QGraphicsItem.ItemIsMovable)
        else:
            self._setRadius(0.075)
            self.setBrush(QBrush(Qt.gray))
            self.setFlag(QGraphicsItem.ItemIsMovable, False)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            self.renderer.centre = self.pos()
            self.renderer.centralPointMoved.emit(self.pos())
            for line_item in self.renderer.lines:
                l = line_item.line()
                l.setP1(self.renderer.centre)
                line_item.setLine(l)

        return super(CentralPoint, self).itemChange(change, value)

    def _setRadius(self, radius):
        self.setRect(-radius, -radius, 2*radius, 2*radius)
