from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QWidget, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal
from Frontend.util_widgets import Page, SideBar, HeaderText, InputLabel, InputField, InputWarningLabel, ActionLabel, PrimaryButton
from Frontend.util_widgets import primary_color, dark_text_color

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

        self.blacklist_scroll_area = QScrollArea()
        self.blacklist_scroll_area.setWidgetResizable(True)
        self.blacklist_scroll_area.setStyleSheet(f"background-color: {primary_color.darker(105).name()}; border: 2px solid {dark_text_color.lighter(400).name()};")
        self.body_layout.addWidget(self.blacklist_scroll_area)

        self.blacklist_container = QWidget()
        self.blacklist_container.setStyleSheet("border: 0px;")
        self.blacklist_scroll_area.setWidget(self.blacklist_container)

        self.blacklist_container_layout = QVBoxLayout()
        self.blacklist_container_layout.setContentsMargins(16, 16, 16, 16)
        self.blacklist_container_layout.setSpacing(16)
        self.blacklist_container.setLayout(self.blacklist_container_layout)

        blacklisted_words = self.fetch_blacklisted_words()

        for blw in blacklisted_words:
            sug_widget = QWidget()
            self.blacklist_container_layout.addWidget(sug_widget)

            sug_layout = QVBoxLayout(sug_widget)

            header = QLabel(f"{blw}")
            header.setStyleSheet(f"color: {dark_text_color.name()}; font-size: 20px;")
            sug_layout.addWidget(header)
            sug_layout.setAlignment(header, Qt.AlignmentFlag.AlignCenter)

        if account_type in ("FREE", "PAID"):
            self.body_header = QLabel("Blacklist Suggestions")
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

        if account_type == "SUPER":
            self.body_header = QLabel("Pending Blacklist Suggestions")
            self.body_header.setStyleSheet(f"color: {dark_text_color.name()}; font-size: 32px; font-weight: 600;")
            self.body_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.body_layout.addWidget(self.body_header)

            self.file_scroll_area = QScrollArea()
            self.file_scroll_area.setWidgetResizable(True)
            self.file_scroll_area.setStyleSheet(f"background-color: {primary_color.darker(105).name()}; border: 2px solid {dark_text_color.lighter(400).name()};")
            self.body_layout.addWidget(self.file_scroll_area)

            self.file_container = QWidget()
            self.file_container.setStyleSheet("border: 0px;")
            self.file_scroll_area.setWidget(self.file_container)

            self.file_container_layout = QVBoxLayout()
            self.file_container_layout.setContentsMargins(16, 16, 16, 16)
            self.file_container_layout.setSpacing(16)
            self.file_container.setLayout(self.file_container_layout)

            blacklist_suggestions = self.fetch_blacklist_suggestions()

            for suggestion in blacklist_suggestions:
                sug_widget = QWidget()
                self.file_container_layout.addWidget(sug_widget)

                sug_layout = QVBoxLayout(sug_widget)

                header = QLabel(f"Suggestion: {suggestion['word']}")
                header.setStyleSheet(f"color: {dark_text_color.name()}; font-size: 20px;")
                sug_layout.addWidget(header)
                sug_layout.setAlignment(header, Qt.AlignmentFlag.AlignCenter)

                accept_button = PrimaryButton("Accept")
                accept_button.clicked.connect(lambda _, sug_id=suggestion["id"], sug_wg=sug_widget: self.accept_suggestion(sug_id, sug_wg))
                sug_layout.addWidget(accept_button)
                sug_layout.setAlignment(accept_button, Qt.AlignmentFlag.AlignCenter)

                reject_button = PrimaryButton("Reject")
                reject_button.clicked.connect(lambda _, sug_id=suggestion["id"], sug_wg=sug_widget: self.reject_suggestion(sug_id, sug_wg))
                sug_layout.addWidget(reject_button)
                sug_layout.setAlignment(reject_button, Qt.AlignmentFlag.AlignCenter)

    def accept_suggestion(self, sug_id, sug_wg):
        try:
            internal_data = {"submission_id": sug_id}
            headers = {"Content-Type": "application/json"}

            response = requests.post(f"http://127.0.0.1:5000/blacklist/approve?user_id={self.user_id}", json=internal_data, headers=headers)
            response.raise_for_status()

            file_previews = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error accepting blacklist suggestion: {e}")

        self.file_container_layout.removeWidget(sug_wg)
        sug_wg.deleteLater()

    def reject_suggestion(self, sug_id, sug_wg):
        try:
            internal_data = {"submission_id": sug_id}
            headers = {"Content-Type": "application/json"}

            response = requests.post(f"http://127.0.0.1:5000/blacklist/reject?user_id={self.user_id}", json=internal_data, headers=headers)
            response.raise_for_status()

            file_previews = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error rejecting blacklist suggestion: {e}")

        self.file_container_layout.removeWidget(sug_wg)
        sug_wg.deleteLater()

    def fetch_blacklisted_words(self):
        blws = []

        try:
            headers = {"Content-Type": "application/json"}

            response = requests.get(f"http://127.0.0.1:5000/blacklist/all?user_id={self.user_id}", headers=headers)
            response.raise_for_status()

            blws = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching black submissions: {e}")

        return blws["blacklisted_words"]

    def fetch_blacklist_suggestions(self):
        suggestions = []

        try:
            headers = {"Content-Type": "application/json"}

            response = requests.get(f"http://127.0.0.1:5000/blacklist/submissions?user_id={self.user_id}", headers=headers)
            response.raise_for_status()

            suggestions = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching black submissions: {e}")

        return suggestions

    def on_suggest_bl_button_click(self):
        suggestion = self.suggest_bl_input.text()

        try:
            internal_data = {"user_id": self.user_id, "word": suggestion}
            headers = {"Content-Type": "application/json"}

            response = requests.post(f"http://127.0.0.1:5000/blacklist", json=internal_data, headers=headers)
            response.raise_for_status()

            file_previews = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error buying tokens: {e}")

        self.side_bar.navigate_to_blacklist.emit()