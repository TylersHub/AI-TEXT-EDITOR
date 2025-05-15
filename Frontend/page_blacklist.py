from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
from util_widgets import Page, SideBar, HeaderText, InputLabel, InputField, InputWarningLabel, ActionLabel, PrimaryButton
from util_widgets import dark_text_color

import requests

class BlacklistPage(Page):
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

        self.body_header = QLabel("Blacklist")
        self.body_header.setStyleSheet(f"color: {dark_text_color.name()}; font-size: 32px; font-weight: 600;")
        self.body_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body_layout.addWidget(self.body_header)

        self.suggest_bl_label = QLabel("Suggest a blacklisted word:")
        self.suggest_bl_label.setStyleSheet(f"color: {dark_text_color.name()}; font-size: 16px;")
        self.body_layout.addWidget(self.suggest_bl_label)

        self.suggest_bl_input = InputField()
        self.body_layout.addWidget(self.suggest_bl_input)

        self.suggest_bl_button = PrimaryButton("Submit")
        self.suggest_bl_button.clicked.connect(self.on_suggest_bl_button_click)
        self.body_layout.addWidget(self.suggest_bl_button)

        self.body_layout.addStretch()

    def on_suggest_bl_button_click(self):
        suggestion = self.suggest_bl_input.text()

        try:
            internal_data = {"word": suggestion}
            headers = {"Content-Type": "application/json"}

            response = requests.post(f"http://127.0.0.1:5000/blacklist", json=internal_data, headers=headers)
            response.raise_for_status()

            file_previews = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error buying tokens: {e}")

        self.side_bar.navigate_to_home.emit()