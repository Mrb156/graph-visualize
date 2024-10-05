from PyQt6.QtCore import QObject, pyqtSignal

class GlobalOptions(QObject):
    optionsChanged = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.options = {
            "font_size": 12,
            "node_size": 3000,
            "node_color": "white",
            "edgecolors": "black",
            "linewidths": 2,
            "width": 2,
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