from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QScrollArea, QWidget, QComboBox

class UniquePropertyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Unique Properties")

        self.layout = QVBoxLayout(self)

        # Scroll area to hold the attributes
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget(self.scroll_area)
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content)

        self.layout.addWidget(self.scroll_area)

        # Add button to add more attributes
        self.add_button = QPushButton("Add Attribute", self)
        self.add_button.clicked.connect(self.add_attribute)
        self.layout.addWidget(self.add_button)

        # Create button to finalize the properties
        self.create_button = QPushButton("Create", self)
        self.create_button.clicked.connect(self.accept)
        self.layout.addWidget(self.create_button)

        self.attributes = []

        self.add_attribute()  # Add the first attribute input by default

    def add_attribute(self):
        """Add a new attribute input row."""
        row_layout = QHBoxLayout()

        name_label = QLabel("Attribute Name:", self)
        name_input = QLineEdit(self)

        type_label = QLabel("Attribute Type:", self)
        type_input = QComboBox(self)
        type_input.addItems(["String", "Integer", "Float", "Boolean"])

        row_layout.addWidget(name_label)
        row_layout.addWidget(name_input)
        row_layout.addWidget(type_label)
        row_layout.addWidget(type_input)

        self.scroll_layout.addLayout(row_layout)
        self.attributes.append((name_input, type_input))

    def get_attributes(self):
        """Return the attributes as a dictionary."""
        dict= {name_input.text(): type_input.currentText() for name_input, type_input in self.attributes if name_input.text() and type_input.currentText()}
        return dict