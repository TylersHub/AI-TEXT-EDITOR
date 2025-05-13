from PyQt6.QtWidgets import QHBoxLayout, QWidget
from PyQt6.QtCore import pyqtSignal
from util_widgets import Page, HomeSideBar

class HomePage(Page):
    sign_out_requested = pyqtSignal()
    navigate_to_sign_in = pyqtSignal()

    def __init__(self, account_type: str):
        super().__init__()

        self.central_layout = QHBoxLayout(self)
        self.central_layout.setContentsMargins(0, 0, 0, 0)

        self.side_bar = HomeSideBar(account_type)
        self.side_bar.sign_out_button.clicked.connect(self.on_sign_out_click)
        self.central_layout.addWidget(self.side_bar, stretch=2)

        wid = QWidget()
        self.central_layout.addWidget(wid, stretch=10)

    def on_sign_out_click(self):
        self.sign_out_requested.emit()
        self.navigate_to_sign_in.emit()