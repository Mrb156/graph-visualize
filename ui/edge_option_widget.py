from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtCore import Qt

class EdgeOptionWidget(QWidget):
    def __init__(self, graph, canvas, parent=None):
        super().__init__(parent)
        
        # Store the reference to GlobalOptions and Canvas
        self.graph = graph
        self.canvas = canvas

        # Create the main layout
        self.main_layout = QVBoxLayout(self)

        # Align the layout to the top
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Create a label to display the selected edge
        self.selected_edge_label = QLabel("Selected Edge: None", self)
        self.main_layout.addWidget(self.selected_edge_label)

        # Create a grid layout for labels and controls
        self.grid_layout = QGridLayout()
        self.main_layout.addLayout(self.grid_layout)

        # Create a dictionary to store the text fields for each attribute
        self.attribute_fields = {}

        # Create a save button
        self.save_button = QPushButton("Save Changes", self)
        self.main_layout.addWidget(self.save_button)

        # Connect the save button to the save_changes method
        self.save_button.clicked.connect(self.save_changes)

        # Set the layout
        self.setLayout(self.main_layout)

    def save_changes(self):
        """Save the changes made to the edge attributes."""
        selected_edge = self.selected_edge_label.text().replace("Selected Edge: ", "")
        if selected_edge != "None":
            source, target = eval(selected_edge)  # Convert string tuple to actual tuple
            for attribute, text_field in self.attribute_fields.items():
                new_value = text_field.text()
                self.graph.set_edge_attribute(source, target, attribute, new_value)
            self.canvas.update()

    def update_selected_edge(self, edge):
        """Update the label to display the selected edge and update the layout."""
        if edge is None:
            self.selected_edge_label.setText("Selected Edge: None")
        else:
            source, target = edge
            self.selected_edge_label.setText(f"Selected Edge: ({source}, {target})")

        # Clear the existing grid layout
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Clear the attribute fields dictionary
        self.attribute_fields.clear()

        # Populate the grid layout with the new edge's attributes
        if edge is not None:
            source, target = edge
            # Populate the grid layout with the edge's attributes
            for row, attribute in enumerate(self.graph.get_edge_attributes(source, target)):
                current_value = self.graph.get_edge_attribute(source, target, attribute).get("value", "")

                # Create a label for the attribute
                label = QLabel(f"{attribute}:", self)
                self.grid_layout.addWidget(label, row, 0)

                # Create a text field for the attribute value
                text_field = QLineEdit(self)
                self.grid_layout.addWidget(text_field, row, 1)

                text_field.setText(str(current_value))

                # Store the text field in the dictionary
                self.attribute_fields[attribute] = text_field