import networkx as nx
import json
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QHBoxLayout, QLabel
import sys
from PyQt6.QtWidgets import QFileDialog

import networkx as nx
import json
from PyQt6.QtWidgets import QFileDialog

class Graph:
    def __init__(self):
        """Initialize an empty graph with NetworkX."""
        self.graph = nx.Graph()
        self.nodes = []  # Keep track of nodes in order of addition
    #     self._observers = []  # List of observers for graph changes


    # def add_observer(self, observer):
    #     """Add an observer that will be notified of graph changes."""
    #     self._observers.append(observer)

    # def notify_observers(self):
    #     """Notify all observers of a graph change."""
    #     for observer in self._observers:
    #         observer.update_view()

    def add_node(self, node, **attrs):
        """Add a node with attributes to the graph."""
        try:
            if not isinstance(attrs, dict):
                raise TypeError("Attributes must be a dictionary")
            if node not in self.graph:
                self.graph.add_node(node, **attrs)
                self.nodes.append(node)
            else:
                self.update_node_attributes(node, **attrs)
        except Exception as e:
            raise Exception(f"Error adding node: {str(e)}")

    def add_edge(self, node1, node2, **attrs):
        """Add an edge with attributes between two nodes."""
        try:
            if not isinstance(attrs, dict):
                raise TypeError("Attributes must be a dictionary")
            # Add nodes if they don't exist
            if node1 not in self.graph:
                self.add_node(node1)
            if node2 not in self.graph:
                self.add_node(node2)
            self.graph.add_edge(node1, node2, **attrs)
        except Exception as e:
            raise Exception(f"Error adding edge: {str(e)}")
        
    def delete_edge(self, node1, node2):
        """Remove an edge between two nodes."""
        try:
            if self.graph.has_edge(node1, node2):
                self.graph.remove_edge(node1, node2)
            # else:
            #     raise ValueError(f"Edge between {node1} and {node2} not found")
        except Exception as e:
            raise Exception(f"Error removing edge: {str(e)}")
        
    def delete_node(self, node):
        """Delete a node and all its edges from the graph."""
        try:
            if node in self.graph:
                self.graph.remove_node(node)
                if node in self.nodes:
                    self.nodes.remove(node)
        except Exception as e:
            raise Exception(f"Error deleting node: {str(e)}")

    def update_node_attributes(self, node, **attrs):
        """Update attributes of an existing node."""
        try:
            if node in self.graph:
                nx.set_node_attributes(self.graph, {node: attrs})
            else:
                raise ValueError(f"Node {node} not found in graph")
        except Exception as e:
            raise Exception(f"Error updating node attributes: {str(e)}")

    def update_edge_attributes(self, node1, node2, **attrs):
        """Update attributes of an existing edge."""
        try:
            if self.graph.has_edge(node1, node2):
                nx.set_edge_attributes(self.graph, {(node1, node2): attrs})
            else:
                raise ValueError(f"Edge between {node1} and {node2} not found")
        except Exception as e:
            raise Exception(f"Error updating edge attributes: {str(e)}")

    def from_json(self, json_str):
        """Load graph from a JSON string."""
        try:
            data = json.loads(json_str)
            self.graph.clear()
            self.nodes.clear()
            
            # Add nodes first
            for node in data.get('nodes', []):
                self.add_node(node['id'], **node.get('attributes', {}))
            
            # Then add edges
            for link in data.get('links', []):
                self.add_edge(link['source'], link['target'], **link.get('attributes', {}))
        except Exception as e:
            raise Exception(f"Error loading from JSON: {str(e)}")

    def to_dict(self):
        """Convert graph to dictionary format."""
        try:
            return {
                'nodes': [{'id': node, 'attributes': dict(self.graph.nodes[node])} 
                         for node in self.graph.nodes],
                'links': [{'source': u, 'target': v, 'attributes': dict(self.graph.edges[u, v])} 
                         for u, v in self.graph.edges]
            }
        except Exception as e:
            raise Exception(f"Error converting to dictionary: {str(e)}")

    def to_json(self):
        """Convert graph to JSON string."""
        try:
            return json.dumps(self.to_dict(), indent=4)
        except Exception as e:
            raise Exception(f"Error converting to JSON: {str(e)}")

    def save_to_json_file(self, file_path):
        """Save graph to a JSON file."""
        try:
            with open(file_path, 'w') as f:
                json.dump(self.to_dict(), f, indent=4)
        except Exception as e:
            raise Exception(f"Error saving to file: {str(e)}")

    def save_as_file_dialog(self):
        """Open a file dialog to save the graph."""
        try:
            filename, _ = QFileDialog.getSaveFileName(
                None,
                "Save File",
                "",
                "JSON Files (*.json);;All Files (*)"
            )
            if filename:
                self.save_to_json_file(filename)
            return filename
        except Exception as e:
            raise Exception(f"Error in save dialog: {str(e)}")

    def has_edge(self, node1, node2):
        """Check if an edge exists between two nodes."""
        return self.graph.has_edge(node1, node2)

    def get_edge_weight(self, node1, node2):
        """Get the weight of an edge between two nodes."""
        try:
            if self.has_edge(node1, node2):
                return (self.graph.edges[node1, node2].get('weight', None))
            return None
        except Exception as e:
            raise Exception(f"Error getting edge weight: {str(e)}")

    def get_nodes(self):
        """Return list of nodes in order of addition."""
        return self.nodes.copy()

    def get_edges(self):
        """Return list of edges."""
        return list(self.graph.edges())

    def get_node_attribute(self, node, attribute):
        """Get the value of a specific attribute for a node."""
        try:
            if node in self.graph:
                return self.graph.nodes[node].get(attribute, None)
            raise ValueError(f"Node {node} not found in graph")
        except Exception as e:
            raise Exception(f"Error getting node attribute: {str(e)}")
        
    def set_node_attribute(self, node, attribute, value):
        """Set the value of a specific attribute for a node."""
        try:
            if node in self.graph:
                self.graph.nodes[node][attribute]['value'] = value
            else:
                raise ValueError(f"Node {node} not found in graph")
        except Exception as e:
            raise Exception(f"Error setting node attribute: {str(e)}")
        
    def get_node_id(self, node):
        """Get the ID of a node."""
        try:
            if node in self.graph:
                return node
            raise ValueError(f"Node {node} not found in graph")
        except Exception as e:
            raise Exception(f"Error getting node ID: {str(e)}")
        
    def set_node_id(self, node, new_id):
        """Get the ID of a node."""
        try:
            if node in self.graph:
                self.nodes[self.nodes.index(node)] = new_id
                # return node
            raise ValueError(f"Node {node} not found in graph")
        except Exception as e:
            raise Exception(f"Error getting node ID: {str(e)}")
        
    # def set_node_id(self, old_id, new_id):
    #     """Set a new ID for a node."""
    #     try:
    #         if old_id in self.graph:
    #             # Copy node attributes
    #             attrs = self.graph.nodes[old_id]
    #             # Add new node with copied attributes
    #             self.add_node(new_id, **attrs)
    #             # Copy edges
    #             for neighbor in list(self.graph.neighbors(old_id)):
    #                 self.add_edge(new_id, neighbor, **self.graph[old_id][neighbor])
    #             # Remove old node
    #             self.delete_node(old_id)
    #         else:
    #             raise ValueError(f"Node {old_id} not found in graph")
    #     except Exception as e:
    #         raise Exception(f"Error setting node ID: {str(e)}")
    
    def get_node_attributes(self, node):
        """Get all attributes of a node."""
        try:
            if node in self.graph:
                return dict(self.graph.nodes[node])
            raise ValueError(f"Node {node} not found in graph")
        except Exception as e:
            raise Exception(f"Error getting node attributes: {str(e)}")
        
    def get_all_attribute_types(self):
        """Get all attribute types for nodes in the graph."""
        try:
            if not self.nodes:
                return []
            # Assuming all nodes have the same attribute types
            first_node = self.nodes[0]
            dicty = dict(self.graph.nodes[first_node].items())
            attribute_types = {}
            for key, value in dicty.items():
                if isinstance(value, dict) and 'type' in value:
                    attribute_types[key] = value['type']
                else:
                    attribute_types[key] = type(value).__name__
            return attribute_types
        except Exception as e:
            raise Exception(f"Error getting attribute types: {str(e)}")
        
    def get_all_attribute_keys_and_types(self):
     
        first_node = self.nodes[0].keys()

        try:
            attribute_keys_and_types = {}
            for key, value in self.graph.nodes[0].items():
                if isinstance(value, dict) and 'type' in value:
                    attribute_keys_and_types[key] = value['type']
                else:
                    attribute_keys_and_types[key] = type(value).__name__
                    raise Exception(f"Error getting attribute keys and types: {str(e)}")
        except Exception as e:
            return attribute_keys_and_types
        except Exception as e:
            raise Exception(f"Error getting attribute keys and types: {str(e)}")