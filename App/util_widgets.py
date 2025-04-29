from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt

class Page(QWidget):
    def __init__(self):
        super().__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("background-color: white;")