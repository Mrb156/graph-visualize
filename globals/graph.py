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

    def delete_node(self, node):
        if node in self.graph:
            self.graph.remove_node(node)
            self.nodes.remove(node)

    def from_json(self, json_str):
        data = json.loads(json_str)
        self.graph.clear()
        self.nodes.clear()
        for node in data['nodes']:
            self.add_node(node['id'], **node.get('attributes', {}))
        for link in data['links']:
            self.add_edge(link['source'], link['target'], **link.get('attributes', {}))

    def to_json(self):
        data = nx.node_link_data(self.graph)
        return json.dumps(data, indent=4)

    def save_to_json_file(self, file_path):
        data = self.to_json()
        with open(file_path, 'w') as f:
            f.write(data)

    def has_edge(self, node1, node2):
        return self.graph.has_edge(node1, node2)

    def get_edge_weight(self, node1, node2):
        return self.graph.get_edge_data(node1, node2).get('weight', '')