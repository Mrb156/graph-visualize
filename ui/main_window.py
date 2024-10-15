import sys
from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QToolBar, QStatusBar,QHBoxLayout,QWidget,QVBoxLayout,QFileDialog,QTableWidget,QTableWidgetItem,QPushButton,QInputDialog,QMessageBox
)
from PyQt6.QtGui import QAction, QIcon, QPalette, QColor
from pathlib import Path
import json

from constants.icons import icons
from globals.graph import Graph
from globals.options import GlobalOptions
from ui.toolbar_action import ToolbarAction
from logic.actions import Actions
from ui.canvas import Canvas
from ui.right_side_panel import RightSidePanel

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.color = "blue"
        self.data = {
            "directed": False,
            "multigraph": False,
            "graph": {},
            "nodes": [],
            "links": []
        }
        self.global_options = GlobalOptions()
        self.graph = Graph()

        self.setWindowTitle("Gráf kezelő app")
        self.setMinimumSize(1000, 700)
        toolbar = QToolBar("Toolbar")

        self.addToolBar(toolbar)
        toolbar.setFloatable(False)
        toolbar.setMovable(False)

        ########
        # Toolbar
        new_document = ToolbarAction(QIcon(icons["new_document"]), "New document", Actions.newDocumentAction, self)
        zoom_in = ToolbarAction(QIcon(icons["zoom_in"]), "Zooom in", Actions.zoomInAction, self)
        zoom_out = ToolbarAction(QIcon(icons["zoom_out"]), "Zooom out", Actions.zoomOutAction, self)

        ## Adding actions to toolbar
        toolbar.addAction(new_document)
        toolbar.addAction(zoom_in)
        toolbar.addAction(zoom_out)

        self.setStatusBar(QStatusBar(self))

        menu = self.menuBar()

        #########
        # File menu elements
        file_menu = menu.addMenu("File")
        new_file = QAction("New file...", self)
        open_file = QAction("Open file...", self)
        open_file.triggered.connect(self.open_file_dialog)
        save = QAction("Save", self)
        close = QAction("Close", self)
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
        edit_menu = menu.addMenu("Edit")
        undo = QAction("Undo", self)
        edit_menu.addAction(undo)
        rnd_graph = QAction("Random graph", self)
        edit_menu.addAction(rnd_graph)
        edit_menu.addSeparator()
        # edit_menu.triggered.connect()

        ###########
        # UI
        self.widget = QWidget()

        layout = QHBoxLayout()
        
        right_side_panel = QVBoxLayout()
        canvas_layout = QVBoxLayout()
        # bottom_layout = QVBoxLayout()
        
        right_side_panel.addWidget(RightSidePanel(self.global_options))
        self.canvas = Canvas(self, width=5, height=4, dpi=100, graph=self.graph.graph, optionsObject=self.global_options)
        self.graphWidget = GraphWidget(self.graph, self)
        canvas_layout.addWidget(self.canvas)
        canvas_layout.addWidget(self.graphWidget)
        self.show()
        layout.addLayout(canvas_layout)
        layout.addLayout(right_side_panel)
        canvas_layout.setStretchFactor(self.canvas, 6)
        canvas_layout.setStretchFactor(self.graphWidget, 3)

        layout.setStretchFactor(canvas_layout, 6)
        layout.setStretchFactor(right_side_panel, 1)
        self.widget.setLayout(layout)
        self.setCentralWidget(self.widget)

    def closeApp(self):
        self.close()

    def open_file_dialog(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select a File", 
            "${HOME}",
            "JSON (*.json)"
        )
        if filename:
            path = Path(filename)
            with open(filename, 'r') as f:
                self.data = json.load(f)
                self.graph.from_json(json.dumps(self.data))

            self.update_view_with_data()

    def update_view_with_data(self):
        self.canvas.update_graph(self.graph.graph)


class GraphWidget(QWidget):
    def __init__(self, graph, main_window, parent=None):
        super().__init__(parent)
        self.graph = graph
        self.main_window = main_window  # Store the reference to MainWindow

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.table = QTableWidget(0, 0)
        self.table.itemChanged.connect(self.handleItemChanged)
        self.layout.addWidget(self.table)

        self.addNodeButton = QPushButton('Add Node')
        self.addNodeButton.clicked.connect(self.addNode)
        self.layout.addWidget(self.addNodeButton)

        self.deleteNodeButton = QPushButton('Delete Node')
        self.deleteNodeButton.clicked.connect(self.deleteNode)
        self.layout.addWidget(self.deleteNodeButton)

        self.saveButton = QPushButton('Save Graph')
        self.saveButton.clicked.connect(self.saveGraph)
        self.layout.addWidget(self.saveButton)

        self.setLayout(self.layout)

    def addNode(self):
        node, ok = QInputDialog.getText(self, 'Add Node', 'Enter node name:')
        if ok and node:
            self.graph.add_node(node)
            self.updateTable()
            self.update_view_with_data()

    def deleteNode(self):
        node, ok = QInputDialog.getText(self, 'Delete Node', 'Enter node name:')
        if ok and node:
            if node in self.graph.nodes:
                self.graph.delete_node(node)
                self.updateTable()
                self.update_view_with_data()
            else:
                QMessageBox.warning(self, 'Error', 'Node not found!')

    def updateTable(self):
        nodes = list(self.graph.nodes)
        size = len(nodes)
        self.table.setRowCount(size)
        self.table.setColumnCount(size)
        self.table.setHorizontalHeaderLabels(nodes)
        self.table.setVerticalHeaderLabels(nodes)

        for i in range(size):
            for j in range(size):
                item = QTableWidgetItem()
                if i == j:
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                else:
                    node1 = nodes[i]
                    node2 = nodes[j]
                    if self.graph.has_edge(node1, node2):
                        weight = self.graph.get_edge_weight(node1, node2)
                        item.setText(str(weight))
                self.table.setItem(i, j, item)

    def handleItemChanged(self, item):
        row = item.row()
        col = item.column()
        text = item.text()

        if not text.isdigit():
            item.setText('')
            return

        if row != col:
            corresponding_item = self.table.item(col, row)
            if corresponding_item is None:
                corresponding_item = QTableWidgetItem()
                self.table.setItem(col, row, corresponding_item)
            corresponding_item.setText(text)
        nodes = list(self.graph.nodes)
        for i in range(self.table.rowCount()):
            for j in range(self.table.columnCount()):
                if i != j:
                    weight_item = self.table.item(i, j)
                    if weight_item and weight_item.text():
                        weight = float(weight_item.text())
                        node1 = nodes[i]
                        node2 = nodes[j]
                        self.graph.add_edge(node1, node2, weight=weight)
            self.update_view_with_data()

    def saveGraph(self):
        nodes = list(self.graph.nodes)
        for i in range(self.table.rowCount()):
            for j in range(self.table.columnCount()):
                if i != j:
                    weight_item = self.table.item(i, j)
                    if weight_item and weight_item.text():
                        weight = float(weight_item.text())
                        node1 = nodes[i]
                        node2 = nodes[j]
                        self.graph.add_edge(node1, node2, weight=weight)
        self.graph.save_to_json_file('graph.json')
        self.update_view_with_data()

    def update_view_with_data(self):
        self.main_window.update_view_with_data()

