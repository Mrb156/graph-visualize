from PyQt6.QtCore import QObject, pyqtSignal

class GlobalOptions(QObject):
    optionsChanged = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.options = {
            "font_size": 12,
            "node_size": 2000,
            "node_color": "white",
            "node_edge_color": "black",  # Corrected key
            "linewidths": 2,
            "width": 2,
            "edge_color": "black",  # Added edge color option
        }

    def set_option(self, key, value):
        self.options[key] = value
        self.optionsChanged.emit()

    def get_option(self, key, default=None):
        return self.options.get(key, default)

    def get_all_option(self):
        return self.options

    def remove_option(self, key):
        if key in self.options:
            del self.options[key]
            self.optionsChanged.emit()

# Create a global instance of GlobalOptions
global_options = GlobalOptions()