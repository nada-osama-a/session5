from PySide6.QtWidgets import QMainWindow
from console.gui.status_widget import StatusWidget
from console.ros_nodes.mediator import Mediator

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
       
        self._mediator = Mediator()

        self.status_widget = StatusWidget('compass.qml',self._mediator)
        self.setCentralWidget(self.status_widget)
        
        self.show()