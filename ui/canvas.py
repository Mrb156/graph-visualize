import sys
import matplotlib
matplotlib.use('QtAgg')
import networkx as nx
import matplotlib.pyplot as plt

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QPoint

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import json

class Canvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100, data=None):
        fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(fig)
        self.ax = fig.add_subplot(111)
        self.ax.margins(0.20)
        self.ax.axis("off")
        self.data = data
        self.plot_graph()

    def plot_graph(self):
        """This method plots the graph."""
        self.ax.clear()  # Clear the previous graph
        G = nx.node_link_graph(self.data)
        
        # Define the layout for the graph
        pos = nx.spring_layout(G)
        options = {
            "font_size": 12,
            "node_size": 3000,
            "node_color": "white",
            "edgecolors": "black",
            "linewidths": 2,
            "width": 2,
        }
        nx.draw_networkx(G, pos, ax=self.ax, **options)
        self.draw()

    def update_graph(self, new_data):
        """Update the graph with new data."""
        self.data = new_data
        self.plot_graph()
