from PyQt6.QtWidgets import QWidget, QLabel, QSpinBox, QColorDialog, QPushButton

class RightSidePanel(QWidget):
    def __init__(self):
        super().__init__()

        # Font size
        self.font_size_label = QLabel("Font Size", self)
        self.font_size_label.move(10, 10)
        self.font_size_spinbox = QSpinBox(self)
        self.font_size_spinbox.setRange(1, 100)
        self.font_size_spinbox.move(80, 10)

        # Node size
        self.node_size_label = QLabel("Node Size", self)
        self.node_size_label.move(10, 50)
        self.node_size_spinbox = QSpinBox(self)
        self.node_size_spinbox.setRange(1, 100)
        self.node_size_spinbox.move(150, 50)

        # Node colors
        self.node_color_label = QLabel("Node Colors", self)
        self.node_color_label.move(10, 90)
        self.node_color_button = QPushButton("Choose Color", self)
        self.node_color_button.move(150, 90)
        self.node_color_button.clicked.connect(self.choose_node_color)

        # Edge color
        self.edge_color_label = QLabel("Edge Color", self)
        self.edge_color_label.move(10, 130)
        self.edge_color_button = QPushButton("Choose Color", self)
        self.edge_color_button.move(150, 130)
        self.edge_color_button.clicked.connect(self.choose_edge_color)

        # Line widths
        self.line_width_label = QLabel("Line Widths", self)
        self.line_width_label.move(10, 170)
        self.line_width_spinbox = QSpinBox(self)
        self.line_width_spinbox.setRange(1, 100)
        self.line_width_spinbox.move(150, 170)

        # Width
        self.width_label = QLabel("Width", self)
        self.width_label.move(10, 210)
        self.width_spinbox = QSpinBox(self)
        self.width_spinbox.setRange(1, 100)
        self.width_spinbox.move(150, 210)

    def choose_node_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.node_color_button.setStyleSheet(f"background-color: {color.name()}")

    def choose_edge_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.edge_color_button.setStyleSheet(f"background-color: {color.name()}")
