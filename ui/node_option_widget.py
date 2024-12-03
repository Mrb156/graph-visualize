from PyQt6.QtWidgets import QWidget, QLabel, QSpinBox, QColorDialog, QPushButton, QVBoxLayout, QGridLayout, QLineEdit
from PyQt6.QtCore import Qt

class NodeOptionsPanel(QWidget):
    def __init__(self, graph, canvas):
        super().__init__()

        # Store the reference to GlobalOptions and Canvas
        self.graph = graph
        self.canvas = canvas

        # Create the main layout
        self.main_layout = QVBoxLayout(self)

        # Align the layout to the top
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Create a label to display the selected node name
        self.selected_node_label = QLabel("Selected Node: None", self)
        self.main_layout.addWidget(self.selected_node_label)

        # Create a grid layout for labels and controls
        self.grid_layout = QGridLayout()
        self.main_layout.addLayout(self.grid_layout)

        # Create a dictionary to store the text fields for each attribute
        self.attribute_fields = {}

        # Set the layout
        self.setLayout(self.main_layout)
        # Create a save button
        self.save_button = QPushButton("Save Changes", self)
        self.main_layout.addWidget(self.save_button)

        # Connect the save button to the save_changes method

    def save_changes(self):
        """Save the changes made to the node attributes."""
        selected_node = self.selected_node_label.text().replace("Selected Node: ", "")
        if selected_node != "None":
            # self.graph.set_node_id(self.node, self.node_id_field.text())
            for attribute, text_field in self.attribute_fields.items():
                new_value = text_field.text()
                self.graph.set_node_attribute(selected_node, attribute, new_value)
                self.canvas.update()

    def update_selected_node(self, node_name):
        """Update the label to display the selected node name and update the layout."""
        self.selected_node_label.setText(f"Selected Node: {node_name}")

        # Clear the existing grid layout
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Clear the attribute fields dictionary
        self.attribute_fields.clear()

        # Populate the grid layout with the new node's attributes
        if node_name != "None":
            self.node = node_name
            self.node_id = self.graph.get_node_id(node_name)

            # Create a label for the Node ID
            label = QLabel("Node ID:", self)
            self.grid_layout.addWidget(label, 0, 0)

            # Create a text field for the Node ID value
            node_id_field = QLineEdit(self)
            self.grid_layout.addWidget(node_id_field, 0, 1)

            node_id_field.setText(str(self.node_id))  # Convert to string

            # Store the Node ID field separately
            self.node_id_field = node_id_field

            # Populate the grid layout with the new node's attributes
            for row, attribute in enumerate(self.graph.get_node_attributes(node_name)):
                attr_data = self.graph.get_node_attribute(node_name, attribute)
                current_value = attr_data.get("value", "")
                # Convert value to string, handling different types
                if isinstance(current_value, (int, float)):
                    current_value = str(current_value)

                # Create a label for the attribute
                label = QLabel(f"{attribute}:", self)
                self.grid_layout.addWidget(label, row + 1, 0)

                # Create a text field for the attribute value
                text_field = QLineEdit(self)
                self.grid_layout.addWidget(text_field, row + 1, 1)

                text_field.setText(current_value)

                # Store the text field in the dictionary
                self.attribute_fields[attribute] = text_field
            self.save_button.clicked.connect(self.save_changes)
        

    def save_edge_changes(self):
        """Save the changes made to the edge attributes."""
        selected_edge = self.selected_node_label.text().replace("Selected Edge: ", "")
        if selected_edge != "None":
            # Parse the edge string format "(source, target)"
            edge_str = selected_edge.strip('()').split(',')
            source, target = edge_str[0].strip(), edge_str[1].strip()
            for attribute, text_field in self.attribute_fields.items():
                new_value = int(text_field.text())
                print(source, target)
                self.graph.set_edge_attribute(source, target, attribute, new_value)
            self.canvas.update()

    def update_selected_edge(self, edge):
        """Update the label to display the selected edge and update the layout."""
        if edge is None:
            self.selected_node_label.setText("Selected Edge: None")
        else:
            source, target = edge
            self.selected_node_label.setText(f"Selected Edge: ({source}, {target})")

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
                current_value = self.graph.get_edge_attribute(source, target, attribute)

                # Create a label for the attribute
                label = QLabel(f"{attribute}:", self)
                self.grid_layout.addWidget(label, row, 0)

                # Create a text field for the attribute value
                text_field = QLineEdit(self)
                self.grid_layout.addWidget(text_field, row, 1)

                text_field.setText(str(current_value))

                # Store the text field in the dictionary
                self.attribute_fields[attribute] = text_field
            self.save_button.clicked.connect(self.save_edge_changes)
