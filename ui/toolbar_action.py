from PyQt6.QtGui import QIcon,QAction

class ToolbarAction(QAction):
    def __init__(self, icon: QIcon, text: str, action, parent=None):
        super().__init__(icon, text, parent)
        # Additional customization can be added here
        self.setStatusTip(text)
        self.triggered.connect(action)

