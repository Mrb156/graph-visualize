import networkx as nx
import json
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QHBoxLayout, QLabel
import sys

class Graph:
    def __init__(self):
        self.graph = nx.Graph()
        self.nodes = []

    def add_node(self, node, **attrs):
        self.graph.add_node(node, **attrs)
        self.nodes.append(node)

    def add_edge(self, node1, node2, **attrs):
        self.graph.add_edge(node1, node2, **attrs)

    def from_json(self, json_data):
        data = json.loads(json_data)
        self.graph = nx.node_link_graph(data)
        self.nodes = list(self.graph.nodes)

    def to_json(self):
        data = nx.node_link_data(self.graph)
        return json.dumps(data, indent=4)

    def save_to_json_file(self, file_path):
        data = self.to_json()
        with open(file_path, 'w') as f:
            f.write(data)

# Example usage:
# g = Graph()
# g.add_node(1)
# g.add_node(2)
# g.add_edge(1, 2)
# print(g.to_json())
# g.save_to_json_file('graph.json')