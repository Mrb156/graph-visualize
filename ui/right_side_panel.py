from PyQt6.QtWidgets import QWidget, QLabel, QSpinBox, QColorDialog, QPushButton, QVBoxLayout, QGridLayout
from PyQt6.QtCore import Qt

class RightSidePanel(QWidget):
    def __init__(self, global_options):
        super().__init__()

        # Store the reference to GlobalOptions
        self.global_options = global_options

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
        self.font_size_spinbox.setValue(self.global_options.get_option("font_size"))  # Set initial value
        self.font_size_spinbox.valueChanged.connect(self.update_font_size)  # Connect to update

        grid_layout.addWidget(self.font_size_label, 0, 0)
        grid_layout.addWidget(self.font_size_spinbox, 0, 1)

        # Node size
        self.node_size_label = QLabel("Node Size", self)
        self.node_size_spinbox = QSpinBox(self)
        self.node_size_spinbox.setRange(1, 5000)
        self.node_size_spinbox.setValue(self.global_options.get_option("node_size"))  # Set initial value
        self.node_size_spinbox.valueChanged.connect(self.update_node_size)  # Connect to update

        grid_layout.addWidget(self.node_size_label, 1, 0)
        grid_layout.addWidget(self.node_size_spinbox, 1, 1)

        # Node colors
        self.node_color_label = QLabel("Node Colors", self)
        self.node_color_button = QPushButton("", self)
        self.node_color_button.setStyleSheet(f"background-color: {self.global_options.get_option('node_color')}")
        self.node_color_button.clicked.connect(self.choose_node_color)

        grid_layout.addWidget(self.node_color_label, 2, 0)
        grid_layout.addWidget(self.node_color_button, 2, 1)

        # Edge color
        self.node_edge_color_label = QLabel("Node edge Color", self)
        self.node_edge_color_button = QPushButton("", self)
        self.node_edge_color_button.setStyleSheet(f"background-color: {self.global_options.get_option('node_edge_color')}")
        self.node_edge_color_button.clicked.connect(self.choose_node_edge_color)

        grid_layout.addWidget(self.node_edge_color_label, 3, 0)
        grid_layout.addWidget(self.node_edge_color_button, 3, 1)

        # Line widths
        self.line_width_label = QLabel("Line Widths", self)
        self.line_width_spinbox = QSpinBox(self)
        self.line_width_spinbox.setRange(1, 100)
        self.line_width_spinbox.setValue(self.global_options.get_option("linewidths"))  # Set initial value
        self.line_width_spinbox.valueChanged.connect(self.update_line_width)  # Connect to update

        grid_layout.addWidget(self.line_width_label, 4, 0)
        grid_layout.addWidget(self.line_width_spinbox, 4, 1)

        # Width
        self.width_label = QLabel("Width", self)
        self.width_spinbox = QSpinBox(self)
        self.width_spinbox.setRange(1, 100)
        self.width_spinbox.setValue(self.global_options.get_option("width"))  # Set initial value
        self.width_spinbox.valueChanged.connect(self.update_width)  # Connect to update

        grid_layout.addWidget(self.width_label, 5, 0)
        grid_layout.addWidget(self.width_spinbox, 5, 1)

        # Edge colors
        self.edge_color_label = QLabel("Edge Colors", self)
        self.edge_color_button = QPushButton("", self)
        self.edge_color_button.setStyleSheet(f"background-color: {self.global_options.get_option('edge_color')}")
        self.edge_color_button.clicked.connect(self.choose_edge_color)

        grid_layout.addWidget(self.edge_color_label, 6, 0)
        grid_layout.addWidget(self.edge_color_button, 6, 1)

        # Add grid layout to the main layout
        main_layout.addLayout(grid_layout)

        # Set the layout
        self.setLayout(main_layout)

    def update_font_size(self, value):
        """Update font size in global options."""
        self.global_options.set_option("font_size", value)

    def update_node_size(self, value):
        """Update node size in global options."""
        self.global_options.set_option("node_size", value)

    def choose_node_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.global_options.set_option("node_color", color.name())
            self.node_color_button.setStyleSheet(f"background-color: {color.name()}")

    def choose_node_edge_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.global_options.set_option("node_edge_color", color.name())
            self.node_edge_color_button.setStyleSheet(f"background-color: {color.name()}")

    def choose_edge_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.global_options.set_option("edge_color", color.name())
            self.edge_color_button.setStyleSheet(f"background-color: {color.name()}")

    def update_line_width(self, value):
        """Update line widths in global options."""
        self.global_options.set_option("linewidths", value)

    def update_width(self, value):
        """Update width in global options."""
        self.global_options.set_option("width", value)
