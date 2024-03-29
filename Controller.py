from sympy.parsing.sympy_parser import parse_expr
from PySide import QtCore, QtGui
from PySide.QtCore import QRectF, Qt

from RiemannSurface import RiemannSurface
from SurfaceRenderers import CentralSurfaceRenderer
from PathManager import PathManager

class Controller(QtCore.QObject):
    def __init__(self, ui):
        super(Controller, self).__init__()
        self.ui = ui

        self.scene_model = QtGui.QGraphicsScene()
        self.ui.display.setScene(self.scene_model)

        # FIXME: Should be dynamic, scrolling should be limited,
        # perhaps. Zoomable.
        # N.b. reflection in Y.
        self.ui.display.scale(100, -100)

        self.surface = RiemannSurface()
        self.indets = None

        csr = CentralSurfaceRenderer(self.scene_model, self.surface)
        self.surface_renderer = csr

        self.paths = PathManager(self.ui.paths)
        self.ui.paths.setModel(self.paths)

        self.scroll_locked = False

        self._connectSlots()
        self._setStandardIcons()

        self.surfaceChanged()
        
        # QGraphicsView::fitInView(QRectF&, Qt::AspectRatioMode) to set zoom.
        # Scroll wheel for zoom too.
        # May want to lock scroll-bars on or off

    def _connectSlots(self):
        self.ui.equation.editingFinished.connect(self.surfaceChanged)
        self.ui.projection_variable.currentIndexChanged.connect(self.setProjection)
        self.ui.primary_mode.currentChanged.connect(self.setPrimaryMode)
        self.surface_renderer.centralPointDragged.connect(self.centralPointDragged)
        self.ui.central_point.editingFinished.connect(self.centralPointSetTextually)

        self.ui.add_path.clicked.connect(self.paths.newPath)
        self.ui.delete_path.clicked.connect(self.paths.removeSelectedPaths)

    def _setStandardIcons(self):
        # Unfortunately Qt Designer doesn't have a way to set the
        # standard icons yet so we have to do it manually here.
        self.ui.add_path.setIcon(QtGui.QIcon.fromTheme('list-add'))
        self.ui.delete_path.setIcon(QtGui.QIcon.fromTheme('list-remove'))
        self.ui.zoom_in.setIcon(QtGui.QIcon.fromTheme('zoom-in'))
        self.ui.zoom_out.setIcon(QtGui.QIcon.fromTheme('zoom-out'))
        self._setScrollLockIcon()

    def _setScrollLockIcon(self):
        if self.scroll_locked:
            self.ui.scroll_lock.setIcon(QtGui.QIcon.fromTheme('object-locked'))
        else:
          self.ui.scroll_lock.setIcon(QtGui.QIcon.fromTheme('object-unlocked'))

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
        
    def setPrimaryMode(self, index):
        '''Currently there are two modes: editing the surface itself, and
        editing paths defined on that surface. The mode in use should be
        determined by the active tab at the bottom.'''
        if index == 0:
            self.surface_renderer.setEditMode(True)
        else:
            self.surface_renderer.setEditMode(False)


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

    def centralPointSet(self, new_text):
        pass

    def centralPointDragged(self, new_point):
        text = '%f+%f*I' % (new_point.x(), new_point.y())
        self.ui.central_point.setText(text)

    def centralPointSetTextually(self):
        new_point = self.ui.central_point.text()
        try:
            new_point = complex(parse_expr(new_point))
            self.surface_renderer.setCentralPoint(new_point)
        except ValueError:
            return


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
