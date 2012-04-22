from PySide.QtGui import QGraphicsItemGroup

from PySide.QtGui import QPen, QBrush, QGraphicsEllipseItem
from PySide.QtCore import QRectF
from PySide.QtCore import Qt

class CentralSurfaceRenderer(QGraphicsItemGroup):
    def __init__(self, surface):
        super(CentralSurfaceRenderer, self).__init__()
        self.surface = surface

    def surfaceChanged(self, surface):
        self.surface = surface
        # FIXME: remove existing items
        el = QGraphicsEllipseItem(QRectF(-1, -1, 5, 5), self)
        el.setBrush(QBrush(Qt.blue))
        p = QPen()
        p.setWidthF(0.1)
        el.setPen(p)
