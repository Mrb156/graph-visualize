from PyQt6.QtWidgets import QMainWindow, QToolBar, QApplication
from PyQt6.QtGui import QAction
import sys

class GraphToolbar(QMainWindow):
    def __init__(self, action_list):
        super().__init__()

        self.action_list = action_list
        self.initUI()

    def initUI(self):
        self.toolbar = QToolBar("My main toolbar")
        self.addToolBar(self.toolbar)

        # Add actions to the toolbar
        self.add_actions()

        self.setWindowTitle('Custom Toolbar')
        self.show()

    def add_actions(self):
        for action_name, action_tip, action_callback in self.action_list:
            action = QAction(action_name, self)
            action.setStatusTip(action_tip)
            action.triggered.connect(action_callback)
            self.toolbar.addAction(action)

    def action1_triggered(self):
        print('Action 1 triggered')

    def action2_triggered(self):
        print('Action 2 triggered')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Define the action list
    actions = [
        ('Action 1', 'This is Action 1', lambda: print('Action 1 triggered')),
        ('Action 2', 'This is Action 2', lambda: print('Action 2 triggered'))
    ]
    
    ex = GraphToolbar(actions)
    sys.exit(app.exec_())