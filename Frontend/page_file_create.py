from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QTextEdit, QWidget
from PyQt6.QtCore import Qt, pyqtSignal
from Frontend.util_widgets import Page, SideBar, PrimaryButton, InputWarningLabel
from Frontend.util_widgets import primary_color, dark_text_color

import requests

class FileCreatePage(Page):
    navigate_to_file_edit = pyqtSignal(str, str)

    def __init__(self, session_token: str, account_type: str, user_id: str):
        super().__init__()

        self.session_token = session_token
        self.account_type = account_type
        self.user_id = user_id
        self.penalty = 0

        self.central_layout = QHBoxLayout(self)
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.central_layout.setSpacing(0)

        self.side_bar = SideBar(account_type, user_id)
        self.central_layout.addWidget(self.side_bar, stretch=1)

        self.body_layout = QVBoxLayout()
        self.body_layout.setContentsMargins(32, 32, 32, 32)
        self.body_layout.setSpacing(32)
        self.central_layout.addLayout(self.body_layout, stretch=4)

        # Header

        self.body_header = QLabel("New File")
        self.body_header.setStyleSheet(f"color: {dark_text_color.name()}; font-size: 32px; font-weight: 600;")
        self.body_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body_layout.addWidget(self.body_header)

        self.bar_one = QWidget()
        self.bar_one.setStyleSheet(f"background-color: {dark_text_color.name()};")
        self.bar_one.setFixedHeight(2)
        self.body_layout.addWidget(self.bar_one)

        # Upload File Section

        self.upload_file_layout = QHBoxLayout()
        self.upload_file_layout.setContentsMargins(0, 0, 0, 0)
        self.upload_file_layout.setSpacing(16)
        self.body_layout.addLayout(self.upload_file_layout)

        self.upload_file_label = QLabel("Upload File:")
        self.upload_file_label.setStyleSheet(f"color: {dark_text_color.name()}; font-size: 20px; font-weight: 500;")
        self.upload_file_layout.addWidget(self.upload_file_label)

        self.upload_file_button = PrimaryButton("Upload")
        self.upload_file_button.clicked.connect(self.on_file_upload_click)
        self.upload_file_layout.addWidget(self.upload_file_button)

        self.upload_file_warning_label = InputWarningLabel()
        self.upload_file_layout.addWidget(self.upload_file_warning_label)

        self.upload_file_layout.addStretch()

        self.divider_bar_layout = QHBoxLayout()
        self.divider_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.divider_bar_layout.setSpacing(32)
        self.body_layout.addLayout(self.divider_bar_layout)

        self.bar_two = QWidget()
        self.bar_two.setStyleSheet(f"background-color: {dark_text_color.name()};")
        self.bar_two.setFixedHeight(1)
        self.divider_bar_layout.addWidget(self.bar_two, 1)

        self.or_label = QLabel("Or")
        self.or_label.setStyleSheet(f"color: {dark_text_color.name()}; font-size: 20px; font-weight: 500;")
        self.divider_bar_layout.addWidget(self.or_label)

        self.bar_three = QWidget()
        self.bar_three.setStyleSheet(f"background-color: {dark_text_color.name()};")
        self.bar_three.setFixedHeight(1)
        self.divider_bar_layout.addWidget(self.bar_three, 1)

        # Type Submission Section

        self.type_submission_label_layout = QHBoxLayout()
        self.type_submission_label_layout.setContentsMargins(0, 0, 0, 0)
        self.type_submission_label_layout.setSpacing(16)
        self.body_layout.addLayout(self.type_submission_label_layout)

        self.type_submission_label = QLabel("Type Submission:")
        self.type_submission_label.setStyleSheet(f"color: {dark_text_color.name()}; font-size: 20px; font-weight: 500;")
        self.type_submission_label_layout.addWidget(self.type_submission_label)

        self.type_submission_warning_label = InputWarningLabel()
        self.type_submission_label_layout.addWidget(self.type_submission_warning_label)

        self.type_submission_label_layout.addStretch()

        self.type_submission_box = QTextEdit()
        self.type_submission_box.setStyleSheet(
            f"color: {dark_text_color.name()};"
            f"background-color: {primary_color.darker(110).name()};"
            f"border: 1px solid {dark_text_color.name()};"
            "border-radius: 8px;"
            "height: 32px;"
            "padding: 0 4px;"
            "font-size: 16px;"
        )
        self.body_layout.addWidget(self.type_submission_box)

        self.bar_four = QWidget()
        self.bar_four.setStyleSheet(f"background-color: {dark_text_color.name()};")
        self.bar_four.setFixedHeight(2)
        self.body_layout.addWidget(self.bar_four)

        # Call-To-Action

        self.submission_button_layout = QHBoxLayout()
        self.submission_button_layout.setContentsMargins(0, 0, 0, 0)
        self.submission_button_layout.setSpacing(0)
        self.body_layout.addLayout(self.submission_button_layout)

        self.submission_button_layout.addStretch()

        self.submit_button_self = PrimaryButton("Submit (Self)")
        self.submit_button_self.clicked.connect(lambda: self.on_submit_click("self"))
        self.submission_button_layout.addWidget(self.submit_button_self)

        self.submission_button_layout.addStretch()

        self.submit_button_llm = PrimaryButton("Submit (LLM)")
        self.submit_button_llm.clicked.connect(lambda: self.on_submit_click("llm"))
        self.submission_button_layout.addWidget(self.submit_button_llm)

        self.submission_button_layout.addStretch()

    def lock_out(self, text: str):
        try:
            data = {"user_id": self.user_id, "text": text}
            headers = {"Content-Type": "application/json"}

            response = requests.post("http://127.0.0.1:5000/submit/text", json=data, headers=headers)

            if response.status_code != 403:
                response.raise_for_status()
            else:
                print("works as expected")
        except requests.exceptions.RequestException as e:
            print(f"Error locking out free account: {e}")

        self.side_bar.sign_out_requested.emit()
        self.side_bar.navigate_to_sign_in.emit()

    def attempt_submission(self, text: str) -> tuple[bool, str]:
        success = None
        file_id = None
        
        try:
            submission_data = {"user_id": self.user_id, "text": text}
            headers = {"Content-Type": "application/json"}

            response = requests.post("http://127.0.0.1:5000/submit/text", json=submission_data, headers=headers)

            if response.status_code == 403:
                self.type_submission_warning_label.setText("Free users are limited to 20 words. Timing out...")
                self.type_submission_warning_label.toggle_text(True)

                self.side_bar.sign_out_requested.emit()
                self.side_bar.navigate_to_sign_in.emit()

                success = False
            elif response.status_code == 400:
                data = response.json()

                self.penalty += int(data["penalty"])

                self.side_bar.update_token_count_penalty(self.penalty)
                self.type_submission_warning_label.setText(data["error"])
                self.type_submission_warning_label.toggle_text(True)

                success = False
            else:
                response.raise_for_status()

            data = response.json()

            success = True
            file_id = data["document"]["id"]
        except requests.exceptions.RequestException as e:
            print(f"Error locking out free account: {e}")
            sucess = False

        return (success, file_id)
    
    def on_file_upload_click(self):
        pass

    def on_submit_click(self, edit_mode: str):
        text = self.type_submission_box.toPlainText()

        # Check For Empty Input
        if not text.strip():
            self.type_submission_warning_label.setText("Submission cannot be empty")
            self.type_submission_warning_label.toggle_text(True)
            return
        
        successful_submission, file_id = self.attempt_submission(text)

        if not successful_submission:
            return

        if edit_mode in ("self", "llm"):
            self.navigate_to_file_edit.emit(file_id, edit_mode)
        else:
            print("Error (on_submit_click): Wrong submission type value provided")