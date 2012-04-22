from PySide.QtGui import QGraphicsItemGroup

from PySide.QtGui import QPen, QBrush, QGraphicsEllipseItem, QGraphicsLineItem
from PySide.QtCore import QRectF
from PySide.QtCore import Qt

class CentralSurfaceRenderer(QGraphicsItemGroup):
    def __init__(self, surface):
        super(CentralSurfaceRenderer, self).__init__()
        self.surface = surface

    def surfaceOrProjectionChanged(self, surface):
        self.surface = surface

        assert(self.scene())
        map(self.scene().removeItem, self.childItems())

        cutPen = QPen(Qt.gray)
        cutPen.setWidthF(0.02)

        dotBrush = QBrush(Qt.red)
        radius = 0.1

        for branch in self.surface.finiteBranchPoints():            
            # FIXME: Arbitrary centre
            l = QGraphicsLineItem(0, 0, branch.real, branch.imag, self)
            l.setPen(cutPen)


            dot = QGraphicsEllipseItem(branch.real - radius, branch.imag - radius, 
                                       2*radius, 2*radius, self)
            dot.setBrush(dotBrush)
            dot.setPen(QPen(QBrush(), 0))
