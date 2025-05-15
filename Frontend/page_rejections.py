from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QWidget
from PyQt6.QtCore import Qt, pyqtSignal
from util_widgets import Page, SideBar, HeaderText, InputLabel, InputField, InputWarningLabel, ActionLabel, PrimaryButton
from util_widgets import primary_color, dark_text_color

import requests

class RejectionsPage(Page):
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

        self.body_header = QLabel("Pending LLM Correction Rejections")
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

        rejections = self.fetch_rejections()
        print(rejections)

        for rej in rejections:
            print(rej)
            sug_widget = QWidget()
            self.file_container_layout.addWidget(sug_widget)

            sug_layout = QVBoxLayout(sug_widget)

            header = QLabel(f"")
            header.setStyleSheet(f"color: {dark_text_color.name()}; font-size: 20px;")
            sug_layout.addWidget(header)
            sug_layout.setAlignment(header, Qt.AlignmentFlag.AlignCenter)

            accept_button = PrimaryButton("Accept")
            accept_button.clicked.connect(lambda _, app_id=rej["id"], sug_wg=sug_widget: self.accept_application(app_id, sug_wg))
            sug_layout.addWidget(accept_button)
            sug_layout.setAlignment(accept_button, Qt.AlignmentFlag.AlignCenter)

            reject_button = PrimaryButton("Reject")
            reject_button.clicked.connect(lambda _, app_id=rej["id"], sug_wg=sug_widget: self.reject_application(app_id, sug_wg))
            sug_layout.addWidget(reject_button)
            sug_layout.setAlignment(reject_button, Qt.AlignmentFlag.AlignCenter)

    def accept_rejection(self, rej_id, app_wg):
        try:
            internal_data = {"rejection_id": rej_id, "decision": "accepted"}
            headers = {"Content-Type": "application/json"}

            response = requests.post(f"http://127.0.0.1:5000/corrections/llm/review-rejection?user_id={self.user_id}", json=internal_data, headers=headers)
            response.raise_for_status()

            file_previews = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error accepting blacklist suggestion: {e}")

        self.file_container_layout.removeWidget(app_wg)
        app_wg.deleteLater()

    def reject_rejection(self, rej_id, app_wg):
        try:
            internal_data = {"rejection_id": rej_id, "decision": "rejected"}
            headers = {"Content-Type": "application/json"}

            response = requests.post(f"http://127.0.0.1:5000/corrections/llm/review-rejection?user_id={self.user_id}", json=internal_data, headers=headers)
            response.raise_for_status()

            file_previews = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error rejecting blacklist suggestion: {e}")

        self.file_container_layout.removeWidget(app_wg)
        app_wg.deleteLater()
    
    def fetch_rejections(self):
        rejections = []

        try:
            headers = {"Content-Type": "application/json"}

            response = requests.get(f"http://127.0.0.1:5000/corrections/llm/rejections?user_id={self.user_id}", headers=headers)
            response.raise_for_status()

            rejections = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching account applications: {e}")

        return rejections