import sys
from PyQt6.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QToolBar, QStatusBar,QHBoxLayout,QWidget,QVBoxLayout
)
from PyQt6.QtGui import QAction, QIcon, QPalette, QColor

from constants.icons import icons
from ui.toolbar_action import ToolbarAction
from logic.actions import Actions

class MainWindow(QMainWindow):

    def __init__(self):
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
        widget = QWidget()

        layout = QHBoxLayout()
        
        right_side_panel = QVBoxLayout()
        canvas_layout = QVBoxLayout()
        
        right_side_panel.setStretch(0,1000)
        right_side_panel.addWidget(Color("blue"))
        right_side_panel.addWidget(Color("green"))
        canvas_layout.addWidget(Color("red"))

        layout.addLayout(canvas_layout)
        layout.addLayout(right_side_panel)

        layout.setStretchFactor(canvas_layout, 6)
        layout.setStretchFactor(right_side_panel, 1)
        widget.setLayout(layout)
        self.setCentralWidget(widget)


    def onMyToolBarButtonClick(self, s):
        print("click", s)
    def closeApp(self):
        self.close()

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
