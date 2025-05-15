from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
from util_widgets import Page, SideBar, HeaderText, InputLabel, InputField, InputWarningLabel, ActionLabel, PrimaryButton
from util_widgets import dark_text_color

import requests

class ApplicationsPage(Page):
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

        self.body_header = QLabel("Applications")
        self.body_header.setStyleSheet(f"color: {dark_text_color.name()}; font-size: 32px; font-weight: 600;")
        self.body_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body_layout.addWidget(self.body_header)     

        applications = self.fetch_applications()

        print(applications)

    def fetch_applications(self):
        applications = []

        try:
            headers = {"Content-Type": "application/json"}

            response = requests.get(f"http://127.0.0.1:5000/auth/upgrade/requests", headers=headers)
            response.raise_for_status()

            applications = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching black submissions: {e}")

        return applications