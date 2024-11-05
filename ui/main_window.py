import sys
from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import (
    QMainWindow, QApplication,
    QLabel,QSplitter, QToolBar, QStatusBar,QHBoxLayout,QWidget,QVBoxLayout,QFileDialog,QTableWidget,QTableWidgetItem,QPushButton,QInputDialog,QMessageBox,QDialog
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
from ui.node_option_widget import NodeOptionsPanel
from ui.new_file_window import UniquePropertyDialog  # Import the UniquePropertyDialog class
import networkx as nx

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
        new_document.triggered.connect(self.new_file)

        toolbar.addAction(zoom_in)
        toolbar.addAction(zoom_out)

        self.setStatusBar(QStatusBar(self))

        menu = self.menuBar()

        #########
        # File menu elements
        file_menu = menu.addMenu("File")
        new_file = QAction("New file...", self)
        new_file.triggered.connect(self.new_file)
        open_file = QAction("Open file...", self)
        open_file.triggered.connect(self.open_file_dialog)
        save = QAction("Save", self)
        save_as = QAction("Save As...", self)

        close = QAction("Close", self)
        close.triggered.connect(self.closeApp)
        file_menu.addAction(new_file)
        file_menu.addSeparator()
        file_menu.addAction(open_file)
        file_menu.addSeparator()
        file_menu.addAction(save)
        save_as.triggered.connect(self.graph.save_as_file_dialog)
        save_as.setShortcut("Ctrl+S")
        file_menu.addAction(save)
        file_menu.addAction(save_as)
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

        splitterVertical = QSplitter(Qt.Orientation.Vertical)
        splitterHorizontal = QSplitter(Qt.Orientation.Horizontal)
        splitterRightVertical = QSplitter(Qt.Orientation.Vertical)  # New vertical splitter for the right side

        # Set handle width and style for visibility
        splitterVertical.setHandleWidth(1)
        splitterHorizontal.setHandleWidth(1)
        splitterRightVertical.setHandleWidth(1)

        # Optionally, you can set a style sheet to make the handles more visible
        splitter_style = """
            QSplitter::handle {
            background-color: gray;
            }
        """
        splitterVertical.setStyleSheet(splitter_style)
        splitterHorizontal.setStyleSheet(splitter_style)
        splitterRightVertical.setStyleSheet(splitter_style)

        self.right_side_panel = RightSidePanel(self.global_options)
        self.canvas = Canvas(self, width=5, height=4, dpi=100, graph=self.graph.graph, optionsObject=self.global_options)
        self.graphWidget = GraphWidget(self.graph, self)

        # New widget for additional options
        self.node_options_panel = NodeOptionsPanel(self.global_options, self.canvas)

        splitterVertical.addWidget(self.canvas)
        splitterVertical.addWidget(self.graphWidget)

        splitterRightVertical.addWidget(self.right_side_panel)
        splitterRightVertical.addWidget(self.node_options_panel)

        splitterHorizontal.addWidget(splitterVertical)
        splitterHorizontal.addWidget(splitterRightVertical)

        self.show()
        layout.addWidget(splitterHorizontal)

        layout.setStretchFactor(splitterVertical, 6)
        layout.setStretchFactor(splitterHorizontal, 1)
        self.widget.setLayout(layout)
        self.setCentralWidget(self.widget)

        self.canvas.node_selected.connect(self.node_options_panel.update_selected_node)
    
    def new_file(self):
        dialog = UniquePropertyDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            attributes = dialog.get_attributes()
            self.graph = nx.Graph()  # Create a new graph
            for node, attr in attributes.items():
                self.graph.add_node(node, **attr)
            self.canvas.update_graph(self.graph)
            self.update_view_with_data()

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

        self.setLayout(self.layout)

    def addNode(self):
        node, ok = QInputDialog.getText(self, 'Add Node', 'Enter node name:')
        if ok and node:
            attributes, ok = QInputDialog.getText(self, 'Add Node Attributes', 'Enter node attributes (key1=value1,key2=value2,...):')
            attr_dict = {}
            if ok and attributes:
                try:
                    attr_dict = dict(item.split("=") for item in attributes.split(","))
                except ValueError:
                    QMessageBox.warning(self, 'Error', 'Invalid attributes format!')
                    return
            self.graph.add_node(node, **attr_dict)
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

    def update_view_with_data(self):
        self.main_window.update_view_with_data()
