import sys
import matplotlib
from globals.options import GlobalOptions
matplotlib.use('QtAgg')
import networkx as nx
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class Canvas(FigureCanvasQTAgg):
    node_selected = pyqtSignal(str)  # Signal to emit when a node is selected
    edge_selected = pyqtSignal(tuple)  # Signal to emit when an edge is selected

    def __init__(self, parent=None, width=5, height=4, dpi=100, graph=None, optionsObject=None, seed=42):
        fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(fig)
        self.ax = fig.add_subplot()
        self.ax.margins(x=0.1)  # Set margins to ensure nodes are not cut off
        self.ax.axis("off")

        self.graph = graph  # NetworkX graph object
        self.optionsObject = optionsObject  # Reference to GlobalOptions
        self.seed = seed  # Seed for the layout

        self.selected_node = None
        self.selected_edge = None
        self.selected_node_color = "red"  # Default color for the selected node

        # Listen to global options change and replot the graph
        self.optionsObject.optionsChanged.connect(self.plot_graph)

        self.plot_graph()

        # Connect the click event
        self.mpl_connect("button_press_event", self.on_click)

    def plot_graph(self):
        """This method plots the graph using the global options."""
        self.ax.clear()  # Clear the previous graph
        self.ax.axis("off")  # Ensure the axes are turned off

        # Check if the graph is empty
        if self.graph is None or len(self.graph.nodes) == 0:
            self.draw()  # Just draw an empty canvas
            return
        
        # Fetch options from GlobalOptions
        options = self.optionsObject.get_all_options()
        
        # Correct the key for edge colors
        if 'node_edge_color' in options:
            options['edgecolors'] = options.pop('node_edge_color')

        # Define the layout for the graph with a seed
        self.pos = nx.spring_layout(self.graph, seed=self.seed)

        # Plot the graph with the options
        nx.draw_networkx(self.graph, self.pos, ax=self.ax, **options)

        # Highlight the selected node
        if self.selected_node is not None:
            nx.draw_networkx_nodes(self.graph, self.pos, nodelist=[self.selected_node], node_color=self.selected_node_color, ax=self.ax)

        # Highlight the selected edge
        if self.selected_edge is not None:
            edge_list = [self.selected_edge]
            nx.draw_networkx_edges(self.graph, self.pos, edgelist=edge_list, edge_color='red', width=2.0, ax=self.ax)

        x_values, y_values = zip(*self.pos.values())
        self.ax.set_xlim(min(x_values) - 1, max(x_values) + 1)
        self.ax.set_ylim(min(y_values) - 1, max(y_values) + 1)

        # Ensure the plot stretches to fill the available space
        self.ax.set_aspect('auto')
        self.ax.figure.tight_layout(pad=0)

        self.draw()

    # def on_click(self, event):
    #     """Handle click events to detect node selection."""
    #     if event.inaxes is not self.ax:
    #         return

    #     # Ensure layout is consistent with the plot
    #     if not hasattr(self, 'pos'):
    #         self.pos = nx.spring_layout(self.graph, seed=self.seed)

    #     # Find the closest node to the click event
    #     closest_node = None
    #     min_distance = float('inf')
    #     for node, (x, y) in self.pos.items():
    #         distance = (x - event.xdata) ** 2 + (y - event.ydata) ** 2
    #         if distance < min_distance:
    #             closest_node = node
    #             min_distance = distance

    #     # Check if the closest node is within a threshold distance to be considered "clicked"
    #     if closest_node is not None and min_distance < 0.05:  # Adjust this threshold as needed
    #         self.selected_node = closest_node
    #         self.node_selected.emit(closest_node)
    #         self.plot_graph()  # Replot the graph to highlight the selected node


    def update_graph(self, new_graph):
        """Update the graph with a new NetworkX graph object and replot."""
        self.graph = new_graph
        self.plot_graph()

    def change_selected_node_color(self, color):
        """Change the color of the selected node and replot the graph."""
        self.selected_node_color = color
        self.plot_graph()
    def select_edge(self, edge):
        """Select an edge in the graph and highlight it."""
        if edge in self.graph.edges():
            self.selected_edge = edge
            # Draw the edge with a different color
            edge_list = [edge]
            nx.draw_networkx_edges(self.graph, self.pos, edgelist=edge_list, 
                                    edge_color='red', width=2.0, ax=self.ax)
            self.draw()

            
    def on_edge_click(self, event):
        """Handle click events to detect edge selection."""
        if event.inaxes is not self.ax or not hasattr(self, 'pos'):
            return

        # Convert click coordinates to graph coordinates
        click_x, click_y = event.xdata, event.ydata
        
        # Find the closest edge to the click
        closest_edge = None
        min_distance = float('inf')
        
        for edge in self.graph.edges():
            # Get edge endpoint coordinates
            x1, y1 = self.pos[edge[0]]
            x2, y2 = self.pos[edge[1]]
            
            # Calculate distance from click to edge line segment
            length = ((x2-x1)**2 + (y2-y1)**2)**0.5
            if length == 0:
                continue
                
            # Calculate perpendicular distance to line segment
            dist = abs((y2-y1)*click_x - (x2-x1)*click_y + x2*y1 - y2*x1) / length
            
            if dist < min_distance:
                min_distance = dist
                closest_edge = edge

        # If click is close enough to an edge, select it
        if closest_edge is not None and min_distance < 0.05:
            self.select_edge(closest_edge)


    def on_click(self, event):
        """Handle click events to detect both node and edge selection."""
        if event.inaxes is not self.ax:
            return

        # Ensure layout is consistent with the plot
        if not hasattr(self, 'pos'):
            self.pos = nx.spring_layout(self.graph, seed=self.seed)

        # Find the closest node
        closest_node = None
        min_node_distance = float('inf')
        for node, (x, y) in self.pos.items():
            distance = (x - event.xdata) ** 2 + (y - event.ydata) ** 2
            if distance < min_node_distance:
                closest_node = node
                min_node_distance = distance

        # Find the closest edge
        closest_edge = None
        min_edge_distance = float('inf')
        for edge in self.graph.edges():
            x1, y1 = self.pos[edge[0]]
            x2, y2 = self.pos[edge[1]]
            
            # Calculate distance from click to edge line segment
            length = ((x2-x1)**2 + (y2-y1)**2)**0.5
            if length == 0:
                continue
                
            # Calculate perpendicular distance to line segment
            dist = abs((y2-y1)*event.xdata - (x2-x1)*event.ydata + x2*y1 - y2*x1) / length
            
            if dist < min_edge_distance:
                min_edge_distance = dist
                closest_edge = edge

        # Set thresholds for selection
        NODE_THRESHOLD = 0.07
        EDGE_THRESHOLD = 0.07

        # Select the closest element (node or edge) if it's within threshold
        if min_node_distance < NODE_THRESHOLD and min_node_distance/NODE_THRESHOLD < min_edge_distance/EDGE_THRESHOLD:
            # Node is closer (relative to its threshold)
            self.selected_node = closest_node
            self.selected_edge = None
            self.node_selected.emit(closest_node)
            self.plot_graph()
        elif min_edge_distance < EDGE_THRESHOLD:
            # Edge is closer (relative to its threshold)
            self.selected_edge = closest_edge
            self.selected_node = None
            self.edge_selected.emit(closest_edge)
            self.select_edge(closest_edge)
            self.plot_graph()
