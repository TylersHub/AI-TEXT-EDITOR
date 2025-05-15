from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QWidget
from PyQt6.QtCore import Qt, pyqtSignal
from util_widgets import Page, SideBar, HeaderText, InputLabel, InputField, InputWarningLabel, ActionLabel, PrimaryButton
from util_widgets import primary_color, dark_text_color

import requests

class ModerationPage(Page):
    def __init__(self, session_token, account_type, user_id):
        super().__init__()

        self.session_token = session_token
        self.account_type = account_type
        self.user_id = user_id

        self.central_layout = QHBoxLayout(self)
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.central_layout.setSpacing(0)

        self.side_bar = SideBar(account_type, user_id)
        self.central_layout.addWidget(self.side_bar, stretch=1)

        self.body_layout = QVBoxLayout()
        self.body_layout.setContentsMargins(32, 32, 32, 32)
        self.body_layout.setSpacing(32)
        self.central_layout.addLayout(self.body_layout, stretch=4)  

        self.body_header = QLabel("Moderation Portal")
        self.body_header.setStyleSheet(f"color: {dark_text_color.name()}; font-size: 32px; font-weight: 600;")
        self.body_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body_layout.addWidget(self.body_header)

        