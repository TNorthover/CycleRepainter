
class Controller:
    def __init__(self):
        self.scene_model = QtGui.QGraphicsScene()

        self.surface = RiemannSurface()
        self.surface_renderer = CentralSurfaceRenderer(self.surface)
        self.scene_model.addItem(self.surface_renderer)

        self.paths = []
        self.paths_model = None # For the listview

    def connect_slots(self):

    # Signals/slots we might care about:
        # scene_model.selectionChanged

    # Signals:

    # Slots:

    def surfaceChanged(self, new_text):
        self.surface.changeTo(new_text)
        # FIXME: highlight incorrect syntax


    # modeChanged (editing surface, editing paths)

    # centralPointChanged
    # analyticPointChanged (should these two be aspects of the renderer?)
    # changesCommitted (make sure we snap paths and confirm).
    # changesReverted

    # pathAdded
    # pathRemoved
    # pathVisibilityChanged

    # pathNodeMoved
    # pathNodeAdded
    # pathNodeRemoved
    # pathSheetChanged

    # zoomChanged
