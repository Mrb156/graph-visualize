from PyQt6.QtWidgets import QWidget, QLabel, QSpinBox, QColorDialog, QPushButton, QVBoxLayout, QGridLayout
from PyQt6.QtCore import Qt

class NodeOptionsPanel(QWidget):
    def __init__(self, global_options, canvas):
        super().__init__()

        # Store the reference to GlobalOptions and Canvas
        self.global_options = global_options
        self.canvas = canvas

        # Create the main layout
        main_layout = QVBoxLayout(self)

        # Align the layout to the top
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Create a label to display the selected node name
        self.selected_node_label = QLabel("Selected Node: None", self)
        main_layout.addWidget(self.selected_node_label)

        # Create a grid layout for labels and controls
        grid_layout = QGridLayout()

        # Node color
        self.node_color_label = QLabel("Node Color", self)
        self.node_color_button = QPushButton("Choose Color", self)
        self.node_color_button.clicked.connect(self.choose_node_color)

        grid_layout.addWidget(self.node_color_label, 0, 0)
        grid_layout.addWidget(self.node_color_button, 0, 1)

        # Node size
        self.node_size_label = QLabel("Node Size", self)
        self.node_size_spinbox = QSpinBox(self)
        self.node_size_spinbox.setRange(1, 5000)
        self.node_size_spinbox.setValue(self.global_options.get_option("node_size"))  # Set initial value
        self.node_size_spinbox.valueChanged.connect(self.update_node_size)  # Connect to update

        grid_layout.addWidget(self.node_size_label, 1, 0)
        grid_layout.addWidget(self.node_size_spinbox, 1, 1)

        # Add the grid layout to the main layout
        main_layout.addLayout(grid_layout)

        # Set the layout
        self.setLayout(main_layout)

    def choose_node_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.node_color_button.setStyleSheet(f"background-color: {color.name()}")
            self.canvas.change_selected_node_color(color.name())

    def update_node_size(self, value):
        self.global_options.set_option("node_size", value)

    def update_selected_node(self, node_name):
        """Update the label to display the selected node name."""
        self.selected_node_label.setText(f"Selected Node: {node_name}")