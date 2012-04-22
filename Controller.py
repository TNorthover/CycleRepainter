from PySide import QtCore, QtGui
from PySide.QtCore import QRectF

from RiemannSurface import RiemannSurface
from SurfaceRenderers import CentralSurfaceRenderer

class Controller(QtCore.QObject):
    def __init__(self, ui):
        super(Controller, self).__init__()
        self.ui = ui

        self.scene_model = QtGui.QGraphicsScene()
        self.ui.display.setScene(self.scene_model)

        # FIXME: Should be dynamic
        self.ui.display.scale(50, 50)

        self.surface = RiemannSurface()
        self.indets = None

        self.surface_renderer = CentralSurfaceRenderer(self.surface)
        self.scene_model.addItem(self.surface_renderer)

        self.paths = []
        self.paths_model = None # For the listview

        self.connectSlots()
        self.surfaceChanged()

    def connectSlots(self):
        self.ui.equation.editingFinished.connect(self.surfaceChanged)
        
        self.ui.projection_variable.currentIndexChanged.connect(self.setProjection)

    def updatePermittedProjections(self):
        '''Called when the equation defining the Riemann surface is
        changed, this function harvests the indeterminates in the
        polynomial and updates the '''
        combo = self.ui.projection_variable

        if self.surface.indeterminates() == self.indets:
            return

        self.indets = self.surface.indeterminates()
        combo.clear()
        for indet in self.indets:
            combo.addItem(str(indet) + ' plane')

        combo.setCurrentIndex(0) # A reasonably sane default


    # Signals/slots we might care about:
        # scene_model.selectionChanged

    # Signals:

    # Slots:

    def surfaceChanged(self):
        '''Deals with the defining-equation of the Riemann surface being changed'''
        new_text = self.ui.equation.text()
        self.surface.setEquation(new_text)
        self.surface_renderer.surfaceOrProjectionChanged(self.surface)
        self.updatePermittedProjections()
        # FIXME: highlight incorrect syntax

    def setProjection(self, idx):
        self.surface.setProjectsOnto(self.indets[idx])
        self.surface_renderer.surfaceOrProjectionChanged(self.surface)


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
