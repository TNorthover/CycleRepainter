from PySide.QtGui import QGraphicsItem

class CentralSurfaceRenderer(QGraphicsItem):
    def __init__(self, surface):
        super(CentralSurfaceRenderer, self).__init__()
        self.surface = surface

