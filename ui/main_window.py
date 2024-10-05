import sys
from PyQt6.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QToolBar, QStatusBar,QHBoxLayout,QWidget,QVBoxLayout,QFileDialog
)
from PyQt6.QtGui import QAction, QIcon, QPalette, QColor
from pathlib import Path
import json

from constants.icons import icons
from globals.options import GlobalOptions
from ui.toolbar_action import ToolbarAction
from logic.actions import Actions
from ui.canvas import Canvas
from ui.right_side_panel import RightSidePanel

class MainWindow(QMainWindow):
    def __init__(self):
        self.color = "blue"
        self.data = {
            "directed": False,
            "multigraph": False,
            "graph": {},
            "nodes": [],
            "links": []
        }
        self.global_options = GlobalOptions()

        super(MainWindow, self).__init__()
        self.setWindowTitle("Gráf kezelő app")
        self.setMinimumSize(1000, 700)
        toolbar = QToolBar("Toolbar")

        self.addToolBar(toolbar)
        toolbar.setFloatable(False)
        toolbar.setMovable(False)

        ########
        # Toolbar
        new_document = ToolbarAction(QIcon(icons["new_document"]), "&New document", Actions.newDocumentAction, self)
        zoom_in = ToolbarAction(QIcon(icons["zoom_in"]), "&Zooom in", Actions.zoomInAction, self)
        zoom_out = ToolbarAction(QIcon(icons["zoom_out"]), "&Zooom out", Actions.zoomOutAction, self)

        ## Adding actons to toolbar
        toolbar.addAction(new_document)
        toolbar.addAction(zoom_in)
        toolbar.addAction(zoom_out)

        self.setStatusBar(QStatusBar(self))

        menu = self.menuBar()

        #########
        # File menu elements
        file_menu = menu.addMenu("&File")
        new_file=QAction("&New file...", self)
        open_file=QAction("&Open file...", self)
        open_file.triggered.connect(self.open_file_dialog)
        save=QAction("&Save", self)
        close=QAction("&Close", self)
        close.triggered.connect(self.closeApp)
        file_menu.addAction(new_file)
        file_menu.addSeparator()
        file_menu.addAction(open_file)
        file_menu.addSeparator()
        file_menu.addAction(save)
        file_menu.addSeparator()
        file_menu.addAction(close)

        ########
        # Edit menu elements
        edit_menu = menu.addMenu("&Edit")
        undo=QAction("&Undo", self)
        edit_menu.addAction(undo)

        ###########
        # UI
        self.widget = QWidget()

        layout = QHBoxLayout()
        
        right_side_panel = QVBoxLayout()
        canvas_layout = QVBoxLayout()
        
        right_side_panel.addWidget(RightSidePanel(self.global_options))
        self.canvas = Canvas(self, width=5, height=4, dpi=100, data=self.data,optionsObject=self.global_options)
        canvas_layout.addWidget(self.canvas)
        self.show()
        layout.addLayout(canvas_layout)
        layout.addLayout(right_side_panel)

        layout.setStretchFactor(canvas_layout, 6)
        layout.setStretchFactor(right_side_panel, 1)
        self.widget.setLayout(layout)
        self.setCentralWidget(self.widget)

    def closeApp(self):
        self.close()
    def open_file_dialog(self):
        filename, ok = QFileDialog.getOpenFileName(
            self,
            "Select a File", 
            "${HOME}",
            "JSON (*.json)"
        )
        if filename:
            path = Path(filename)
            with open(filename, 'r') as f:
                self.data = json.load(f)

            self.update_view_with_data()

    def update_view_with_data(self):
        self.canvas.update_graph(self.data)

class Color(QWidget):
    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)