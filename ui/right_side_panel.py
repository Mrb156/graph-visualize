from PyQt6.QtWidgets import QWidget, QLabel, QSpinBox, QColorDialog, QPushButton, QVBoxLayout, QGridLayout
from PyQt6.QtCore import Qt

class RightSidePanel(QWidget):
    def __init__(self):
        super().__init__()

        # Create the main layout
        main_layout = QVBoxLayout(self)

        # Align the layout to the top
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Create a grid layout for labels and controls
        grid_layout = QGridLayout()

        # Font size
        self.font_size_label = QLabel("Font Size", self)
        self.font_size_spinbox = QSpinBox(self)
        self.font_size_spinbox.setRange(1, 100)

        grid_layout.addWidget(self.font_size_label, 0, 0)
        grid_layout.addWidget(self.font_size_spinbox, 0, 1)

        # Node size
        self.node_size_label = QLabel("Node Size", self)
        self.node_size_spinbox = QSpinBox(self)
        self.node_size_spinbox.setRange(1, 100)

        grid_layout.addWidget(self.node_size_label, 1, 0)
        grid_layout.addWidget(self.node_size_spinbox, 1, 1)

        # Node colors
        self.node_color_label = QLabel("Node Colors", self)
        self.node_color_button = QPushButton("Choose Color", self)
        self.node_color_button.clicked.connect(self.choose_node_color)

        grid_layout.addWidget(self.node_color_label, 2, 0)
        grid_layout.addWidget(self.node_color_button, 2, 1)

        # Edge color
        self.edge_color_label = QLabel("Edge Color", self)
        self.edge_color_button = QPushButton("Choose Color", self)
        self.edge_color_button.clicked.connect(self.choose_edge_color)

        grid_layout.addWidget(self.edge_color_label, 3, 0)
        grid_layout.addWidget(self.edge_color_button, 3, 1)

        # Line widths
        self.line_width_label = QLabel("Line Widths", self)
        self.line_width_spinbox = QSpinBox(self)
        self.line_width_spinbox.setRange(1, 100)

        grid_layout.addWidget(self.line_width_label, 4, 0)
        grid_layout.addWidget(self.line_width_spinbox, 4, 1)

        # Width
        self.width_label = QLabel("Width", self)
        self.width_spinbox = QSpinBox(self)
        self.width_spinbox.setRange(1, 100)

        grid_layout.addWidget(self.width_label, 5, 0)
        grid_layout.addWidget(self.width_spinbox, 5, 1)

        # Add grid layout to the main layout
        main_layout.addLayout(grid_layout)

        # Set the layout
        self.setLayout(main_layout)

    def choose_node_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.node_color_button.setStyleSheet(f"background-color: {color.name()}")

    def choose_edge_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.edge_color_button.setStyleSheet(f"background-color: {color.name()}")
