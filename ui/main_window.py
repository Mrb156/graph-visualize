import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QLabel, QSplitter, QToolBar, QStatusBar,
    QHBoxLayout, QWidget, QVBoxLayout, QFileDialog, QTableWidget,
    QTableWidgetItem, QPushButton, QInputDialog, QMessageBox, QDialog,QMenu, QStyledItemDelegate, QLineEdit, QCheckBox
)
from PyQt6.QtGui import QAction, QIcon, QPalette, QColor, QIntValidator, QDoubleValidator
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
from ui.unique_property_dialog import UniquePropertyDialog
from ui.edge_option_widget import EdgeOptionWidget
import networkx as nx

class PanelContainer(QWidget):
    def __init__(self, content_widget, title, parent=None):
        super().__init__(parent)
        self.content_widget = content_widget
        self.title = title
        self.is_visible = True
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header with title and toggle button
        header = QWidget()
        header.setFixedHeight(30)  # Fixed height for header
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(5, 2, 5, 2)
        
        title_label = QLabel(title)
        self.toggle_button = QPushButton("×")
        self.toggle_button.setFixedSize(20, 20)
        self.toggle_button.clicked.connect(self.toggle_visibility)
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(self.toggle_button)
        
        layout.addWidget(header)
        layout.addWidget(content_widget)
        
        # Style
        header.setStyleSheet("border-bottom: 1px solid #ddd;")
        self.toggle_button.setStyleSheet("""
            QPushButton {
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
            }
        """)

    def toggle_visibility(self):
        self.is_visible = not self.is_visible
        self.content_widget.setVisible(self.is_visible)
        self.toggle_button.setText("+" if not self.is_visible else "×")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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
        
        # Initialize UI
        self.setup_toolbar()
        self.setup_menu()
        self.setup_main_layout()

    def setup_toolbar(self):
        toolbar = QToolBar("Toolbar")
        self.addToolBar(toolbar)
        toolbar.setFloatable(False)
        toolbar.setMovable(False)

        new_document = ToolbarAction(QIcon(icons["new_document"]), "New document", Actions.newDocumentAction, self)
        zoom_in = ToolbarAction(QIcon(icons["zoom_in"]), "Zoom in", Actions.zoomInAction, self)
        zoom_out = ToolbarAction(QIcon(icons["zoom_out"]), "Zoom out", Actions.zoomOutAction, self)

        toolbar.addAction(new_document)
        new_document.triggered.connect(self.new_file)
        toolbar.addAction(zoom_in)
        toolbar.addAction(zoom_out)

        self.setStatusBar(QStatusBar(self))

    def setup_menu(self):
        menu = self.menuBar()
        
        # File menu
        file_menu = menu.addMenu("File")
        new_file = QAction("New file...", self)
        new_file.triggered.connect(self.new_file)
        open_file = QAction("Open file...", self)
        open_file.triggered.connect(self.open_file_dialog)
        save = QAction("Save", self)
        save_as = QAction("Save As...", self)
        save_as.triggered.connect(self.graph.save_as_file_dialog)
        save_as.setShortcut("Ctrl+S")
        close = QAction("Close", self)
        close.triggered.connect(self.closeApp)

        file_menu.addAction(new_file)
        file_menu.addSeparator()
        file_menu.addAction(open_file)
        file_menu.addSeparator()
        file_menu.addAction(save)
        file_menu.addAction(save_as)
        file_menu.addSeparator()
        file_menu.addAction(close)

        # Edit menu
        edit_menu = menu.addMenu("Edit")
        undo = QAction("Undo", self)
        rnd_graph = QAction("Random graph", self)
        edit_menu.addAction(undo)
        edit_menu.addAction(rnd_graph)
        edit_menu.addSeparator()

        # View menu (new)
        view_menu = menu.addMenu("View")
        self.view_actions = {}
        
    def setup_main_layout(self):
        self.widget = QWidget()
        layout = QHBoxLayout()

        # Create splitters
        self.splitter_vertical = QSplitter(Qt.Orientation.Vertical)
        self.splitter_horizontal = QSplitter(Qt.Orientation.Horizontal)
        self.splitter_right_vertical = QSplitter(Qt.Orientation.Vertical)

        # Set splitter styles
        splitter_style = "QSplitter::handle { background-color: gray; }"
        for splitter in [self.splitter_vertical, self.splitter_horizontal, self.splitter_right_vertical]:
            splitter.setHandleWidth(1)
            splitter.setStyleSheet(splitter_style)

        # Create main components
        self.canvas = Canvas(self, width=5, height=4, dpi=100, graph=self.graph, optionsObject=self.global_options)
        self.graph_widget = GraphWidget(self.graph, self)
        self.right_side_panel = RightSidePanel(self.global_options)
        self.node_options_panel = NodeOptionsPanel(self.graph, self.canvas)

        # Wrap components in containers
        self.canvas_container = PanelContainer(self.canvas, "Canvas")
        self.graph_widget_container = PanelContainer(self.graph_widget, "Graph Data")
        self.right_panel_container = PanelContainer(self.right_side_panel, "Options")
        self.node_options_container = PanelContainer(self.node_options_panel, "Node Options")

        # Add containers to splitters
        self.splitter_vertical.addWidget(self.canvas_container)
        self.splitter_vertical.addWidget(self.graph_widget_container)

        self.splitter_right_vertical.addWidget(self.right_panel_container)
        self.splitter_right_vertical.addWidget(self.node_options_container)

        self.splitter_horizontal.addWidget(self.splitter_vertical)
        self.splitter_horizontal.addWidget(self.splitter_right_vertical)

        # Setup layout
        layout.addWidget(self.splitter_horizontal)
        self.widget.setLayout(layout)
        self.setCentralWidget(self.widget)

        # Connect signals
        self.canvas.node_selected.connect(self.node_options_panel.update_selected_node)
        self.canvas.edge_selected.connect(self.node_options_panel.update_selected_edge)

        # Add view menu actions
        self.setup_view_menu()

    def setup_view_menu(self):
        view_menu = self.menuBar().findChild(QMenu, "View")
        if not view_menu:
            view_menu = self.menuBar().addMenu("View")

        # Create actions for each panel
        panels = {
            "Canvas": self.canvas_container,
            "Graph Data": self.graph_widget_container,
            "Options": self.right_panel_container,
            "Node Options": self.node_options_container
        }

        for name, container in panels.items():
            action = QAction(f"Show {name}", self)
            action.setCheckable(True)
            action.setChecked(True)
            action.triggered.connect(lambda checked, c=container: self.toggle_panel(c, checked))
            view_menu.addAction(action)
            self.view_actions[name] = action

    def toggle_panel(self, container, show):
        container.setVisible(show)
        if show:
            container.content_widget.setVisible(container.is_visible)

    def new_file(self):
        dialog = UniquePropertyDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            attributes = dialog.get_attributes()
            self.graph.clear_graph()
            self.saved_attributes = attributes  # Save the new attributes
            self.setup_main_layout()  # Re-setup the main layout

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
            with open(filename, 'r') as f:
                self.data = json.load(f)
                self.graph.from_json(json.dumps(self.data))
            self.update_view_with_data()
            self.saved_attributes = self.graph.get_all_attribute_types()
            self.graph_widget.updateTable()

    def update_view_with_data(self):
        self.canvas.update_graph(self.graph.graph)

class NumericDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        editor.setValidator(QDoubleValidator())  # For decimal numbers
        return editor

    def setEditorData(self, editor, index):
        value = index.data(Qt.EditRole)
        if value is not None:
            editor.setText(str(value))

    def setModelData(self, editor, model, index):
        try:
            value = float(editor.text())
            model.setData(index, value, Qt.EditRole)
        except ValueError:
            model.setData(index, None, Qt.EditRole)
    
class GraphWidget(QWidget):
    def __init__(self, graph, main_window, parent=None):
        super().__init__(parent)
        self.graph = graph
        self.main_window = main_window  # Store the reference to MainWindow
        self.initUI()

    def setModelData(self, editor, model, index):
        value = editor.text()
        if value == "":
            value = "0"
        model.setData(index, value)

    def initUI(self):
        self.layout = QVBoxLayout()

        self.table = QTableWidget(0, 0)
        self.table.itemChanged.connect(self.handleItemChanged)
        # self.table.setItemDelegate(NumericDelegate())
        self.layout.addWidget(self.table)

        self.addNodeButton = QPushButton('Add Node')
        self.addNodeButton.clicked.connect(self.addNode)
        self.layout.addWidget(self.addNodeButton)

        self.deleteNodeButton = QPushButton('Delete Node')
        self.deleteNodeButton.clicked.connect(self.deleteNode)
        self.layout.addWidget(self.deleteNodeButton)

        self.setLayout(self.layout)

    def update_view(self):
        """Called when graph changes."""
        self.updateTable()
        self.main_window.canvas.plot_graph()

    def addNode(self):
        node, ok = QInputDialog.getText(self, 'Add Node', 'Enter node name:')
        if ok and node:
            dialog = QDialog(self)
            dialog.setWindowTitle("Add Node Attributes")
            layout = QVBoxLayout(dialog)

            attribute_widgets = {}
            for attr, attr_type in self.main_window.saved_attributes.items():
                attr_layout = QHBoxLayout()
                attr_label = QLabel(f"{attr} ({attr_type}):")
                attr_input = QLineEdit()
                attr_layout.addWidget(attr_label)
                attr_layout.addWidget(attr_input)
                layout.addLayout(attr_layout)
                attribute_widgets[attr] = attr_input

            done_button = QPushButton("Done")
            done_button.clicked.connect(dialog.accept)
            layout.addWidget(done_button)

            if dialog.exec() == QDialog.DialogCode.Accepted:
                attr_dict = {}
                for attr, widget in attribute_widgets.items():
                    value = widget.text()
                    attr_type = self.main_window.saved_attributes[attr]
                    if attr_type == "int":
                        try:
                            value = int(value)
                        except ValueError:
                            QMessageBox.warning(self, 'Error', f'Invalid value for {attr}, expected an integer!')
                            return
                    elif attr_type == "float":
                        try:
                            value = float(value)
                        except ValueError:
                            QMessageBox.warning(self, 'Error', f'Invalid value for {attr}, expected a float!')
                            return
                    attr_dict[attr] = {"value": value, "type": attr_type}

                self.graph.add_node(node, **attr_dict)
                self.update_view_with_data()
                self.updateTable()

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
                if i == j:
                    item = QTableWidgetItem("0")
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                else:
                    node1 = nodes[i]
                    node2 = nodes[j]
                    if self.graph.has_edge(node1, node2):
                        weight = self.graph.get_edge_weight(node1, node2)
                        # Create the item directly with the text
                        item = QTableWidgetItem(str(int(weight)))
                    else:
                        item = QTableWidgetItem("0")
                self.table.setItem(i, j, item)

    def resetTable(self):
        self.table.clear()
        self.table.setRowCount(0)
        self.table.setColumnCount(0)

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
                        node1 = nodes[i]
                        node2 = nodes[j]
                        if weight_item.text() == "0" or weight_item.text() == "":
                            self.graph.delete_edge(node1, node2)
                        else:
                            weight = int(weight_item.text())
                            self.graph.add_edge(node1, node2, weight=weight)
        self.update_view_with_data()

    def update_view_with_data(self):
        self.main_window.update_view_with_data()
