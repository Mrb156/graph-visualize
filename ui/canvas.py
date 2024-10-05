import sys
import matplotlib
from globals.options import GlobalOptions
matplotlib.use('QtAgg')
import networkx as nx
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class Canvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100, data=None, optionsObject=None):
        fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(fig)
        self.ax = fig.add_subplot()
        self.ax.margins()
        self.ax.axis("off")

        self.data = data  # Graph data
        self.optionsObject = optionsObject  # Reference to GlobalOptions

        # Listen to global options change and replot the graph
        self.optionsObject.optionsChanged.connect(self.plot_graph)

        self.plot_graph()

    def plot_graph(self):
        """This method plots the graph using the global options."""
        self.ax.clear()  # Clear the previous graph

        # Fetch options from GlobalOptions
        options = self.optionsObject.get_all_option()

        # Create the graph using NetworkX
        G = nx.node_link_graph(self.data)
        
        # Define the layout for the graph
        pos = nx.spring_layout(G)

        # Plot the graph with the options
        nx.draw_networkx(G, pos, ax=self.ax, **options)
        self.draw()

    def update_graph(self, new_data):
        """Update the graph with new data and replot."""
        self.data = new_data
        self.plot_graph()
