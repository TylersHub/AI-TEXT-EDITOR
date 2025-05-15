from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QSizePolicy, QVBoxLayout, QHBoxLayout, QScrollArea
from PyQt6.QtGui import QColor, QCursor
from PyQt6.QtCore import Qt, pyqtSignal

import requests

# Color Palette
primary_color = QColor("#F8F8FF")
secondary_color = QColor("#7D55C7")
accent_color = QColor("#F3D03E")
dark_text_color = QColor("#2C2C2C")
light_text_color = QColor("#F8F8FF")

class Page(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet(f"Page {{ background-color: {primary_color.name()}; }}")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

class HeaderText(QLabel):
    def __init__(self, text: str):
        super().__init__(text)

        self.setStyleSheet(
            f"{type(self).__name__} {{"
            f"color: {dark_text_color.name()};"
            "font-size: 40px;"
            "font-weight: 600;"
            "}"
        )

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

class InputLabel(QLabel):
    def __init__(self, text: str):
        super().__init__(text)

        self.setStyleSheet(
            f"{type(self).__name__} {{"
            f"color: {dark_text_color.name()};"
            "padding-left: 2px;"
            "font-size: 12px;"
            "}"
        )

class InputWarningLabel(QLabel):
    def __init__(self, text: str = None):
        super().__init__(text)

        self.is_text_visible = False
        self.toggle_text(False)

    def toggle_text(self, show_text: bool):
        if show_text: 
            self.is_text_visible = True

            self.setStyleSheet(
                f"{type(self).__name__} {{"
                "color: rgb(200, 0, 0);"
                "padding-left: 2px;"
                "font-size: 12px;"
                "}"
            )
        else:
            self.is_text_visible = False

            self.setStyleSheet(
                f"{type(self).__name__} {{"
                "color: transparent;"
                "padding-left: 2px;"
                "font-size: 12px;"
                "}"
            )

class InputField(QLineEdit):
    def __init__(self, text: str = None, is_sensitive = False):
        super().__init__(text)

        self.setStyleSheet(
            f"{type(self).__name__} {{"
            f"color: {dark_text_color.name()};"
            f"background-color: {primary_color.name()};"
            f"border: 1px solid {dark_text_color.name()};"
            "border-radius: 8px;"
            "height: 32px;"
            "padding: 0 4px;"
            "font-size: 16px;"
            "}"
        )

        if is_sensitive: self.setEchoMode(QLineEdit.EchoMode.Password)

class ActionLabel(QPushButton):
    def __init__(self, text: str):
        super().__init__(text)

        self.setStyleSheet(
            f"{type(self).__name__} {{"
            f"color: {secondary_color.name()};"
            "background-color: transparent;"
            "font-size: 12px;"
            "font-weight: 600;"
            "}"
        )

        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setFlat(True)

class PrimaryButton(QPushButton):
    def __init__(self, text: str = None):
        super().__init__(text)

        self.setStyleSheet(
            f"{type(self).__name__} {{"
            f"color: {primary_color.name()};"
            f"background-color: {secondary_color.name()};"
            "border-radius: 8px;"
            "height: 32px;"
            "min-width: 128px;"
            "border-radius: 16px;"
            "font-size: 16px;"
            "font-weight: 600;"
            "}"
        )

        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

class SecondaryButton(QPushButton):
    def __init__(self, text: str = None):
        super().__init__(text)

        self.setStyleSheet(
            f"{type(self).__name__} {{"
            f"color: {dark_text_color.name()};"
            f"background-color: {primary_color.name()};"
            "border-radius: 8px;"
            "height: 32px;"
            "min-width: 128px;"
            "border-radius: 16px;"
            "font-size: 16px;"
            "font-weight: 600;"
            "}"
        )

        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

class SideBar(QWidget):
    # Session Signals
    sign_out_requested = pyqtSignal()
    navigate_to_sign_in = pyqtSignal()

    # Side Bar Signals
    navigate_to_token_purchase = pyqtSignal()
    navigate_to_home = pyqtSignal()
    navigate_to_blacklist = pyqtSignal()
    navigate_to_history = pyqtSignal()
    navigate_to_invites = pyqtSignal()

    # Side Bar Admin Signals
    navigate_to_applications = pyqtSignal()
    navigate_to_rejections = pyqtSignal()
    navigate_to_complaints = pyqtSignal()
    navigate_to_moderation = pyqtSignal()
    
    def __init__(self, account_type: str, user_id: str):
        super().__init__()

        self.setStyleSheet(
            f"{type(self).__name__} {{"
            f"background-color: {secondary_color.name()}"
            "}"
        )

        self.user_name, self.token_count = self.fetch_side_bar_data(user_id)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.__init_body(account_type)

    def fetch_side_bar_data(self, user_id) -> tuple[str, str]:
        first_name = "?"
        token_count = "?"

        try:
            headers = {"Content-Type": "application/json"}
            
            response = requests.get(f"http://127.0.0.1:5000/user/sidebar/{user_id}", headers=headers)
            response.raise_for_status()

            data = response.json()

            first_name = data["first_name"]
            token_count = data["tokens"]
        except requests.exceptions.RequestException as e:
            print(f"Error fetching side bar data: {e}")

        return (first_name, token_count)

    def __init_body(self, account_type: str):
        self.central_layout = QVBoxLayout(self)
        self.central_layout.setContentsMargins(32, 32, 32, 32)
        self.central_layout.setSpacing(32)

        self.profile_layout = QHBoxLayout()
        self.central_layout.addLayout(self.profile_layout)

        self.profile_avatar = QLabel("👤")
        self.profile_avatar.setStyleSheet("background-color: white; border-radius: 20px; font-size: 24px;")
        self.profile_avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.profile_avatar.setFixedSize(40, 40)
        self.profile_layout.addWidget(self.profile_avatar)

        self.profile_name = QLabel(self.user_name)
        self.profile_name.setStyleSheet(f"color: {primary_color.name()}; font-size: 32px;")
        self.profile_name.setMinimumWidth(128)
        self.profile_layout.addWidget(self.profile_name)

        self.bar_one = QWidget()
        self.bar_one.setStyleSheet(f"background-color: {primary_color.name()};")
        self.bar_one.setFixedHeight(2)
        self.central_layout.addWidget(self.bar_one)

        self.token_layout = QHBoxLayout()
        self.central_layout.addLayout(self.token_layout)

        self.token_count_label = QLabel(f"Tokens: {self.token_count}")
        self.token_count_label.setStyleSheet(f"color: {primary_color.name()}; font-size: 24px;")
        self.token_layout.addWidget(self.token_count_label)

        self.token_layout.addStretch()

        self.buy_token_button = QPushButton("➕")
        self.buy_token_button.setStyleSheet(f"background-color: {primary_color.name()}; color: {dark_text_color.name()}; font-size: 16px; border-radius: 16px;")
        self.buy_token_button.setMinimumSize(32, 32)
        self.buy_token_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.buy_token_button.clicked.connect(self.navigate_to_token_purchase.emit)
        self.token_layout.addWidget(self.buy_token_button)

        self.bar_two = QWidget()
        self.bar_two.setStyleSheet(f"background-color: {primary_color.name()};")
        self.bar_two.setFixedHeight(2)
        self.central_layout.addWidget(self.bar_two)

        self.home_button = SecondaryButton("Home")
        self.home_button.clicked.connect(self.navigate_to_home.emit)
        self.central_layout.addWidget(self.home_button)

        self.blacklist_button = SecondaryButton("Blacklist")
        self.blacklist_button.clicked.connect(self.navigate_to_blacklist.emit)
        self.central_layout.addWidget(self.blacklist_button)

        if account_type in ("PAID", "SUPER"):
            self.history_button = SecondaryButton("History")
            self.history_button.clicked.connect(self.navigate_to_history.emit)
            self.central_layout.addWidget(self.history_button)

            self.invites_button = SecondaryButton("Invites")
            self.invites_button.clicked.connect(self.navigate_to_invites.emit)
            self.central_layout.addWidget(self.invites_button)

        if account_type == "SUPER":
            self.applications_button = SecondaryButton("Applications")
            self.applications_button.clicked.connect(self.navigate_to_applications.emit)
            self.central_layout.addWidget(self.applications_button)

            self.rejections_button = SecondaryButton("Rejections")
            self.rejections_button.clicked.connect(self.navigate_to_rejections.emit)
            self.central_layout.addWidget(self.rejections_button)

            self.complaints_button = SecondaryButton("Complaints")
            self.complaints_button.clicked.connect(self.navigate_to_complaints.emit)
            self.central_layout.addWidget(self.complaints_button)

            self.moderation_button = SecondaryButton("Moderation")
            self.moderation_button.clicked.connect(self.navigate_to_moderation.emit)
            self.central_layout.addWidget(self.moderation_button)

        self.central_layout.addStretch()

        self.bar_three = QWidget()
        self.bar_three.setStyleSheet(f"background-color: {primary_color.name()};")
        self.bar_three.setFixedHeight(2)
        self.central_layout.addWidget(self.bar_three)

        self.sign_out_button = SecondaryButton("Sign Out")
        self.sign_out_button.clicked.connect(self.sign_out)
        self.central_layout.addWidget(self.sign_out_button)

    def update_token_count_penalty(self, penalty: int):
        self.token_count_label.setText(f"Tokens: {self.token_count} (-{penalty})")

    def sign_out(self):
        self.sign_out_requested.emit()
        self.navigate_to_sign_in.emit()

class TopBar(QWidget):
    def __init__(self, user_id: str):
        super().__init__()

        self.setStyleSheet(
            f"{type(self).__name__} {{"
            f"background-color: {primary_color.darker(105).name()};"
            f"border: 2px solid {dark_text_color.lighter(400).name()};"
            "}"
        )

        file_count, correction_count, tokens_used = self.fetch_top_bar_data(user_id)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.__init_body(file_count, correction_count, tokens_used)

    def fetch_top_bar_data(self, user_id) -> tuple[str, str, str]:
        submission_count = "?"
        correction_count = "?"
        tokens_used = "?"

        try:
            headers = {"Content-Type": "application/json"}
            
            response = requests.get(f"http://127.0.0.1:5000/stats/{user_id}", headers=headers)
            response.raise_for_status()

            data = response.json()

            submission_count = data["total_submissions"]
            correction_count = data["total_corrections"]
            tokens_used = data["total_tokens_used"]
        except requests.exceptions.RequestException as e:
            print(f"Error fetching top bar data: {e}")

        return (submission_count, correction_count, tokens_used)

    def __init_body(self, file_count: int, correction_count: int, tokens_used: int):
        self.central_layout = QHBoxLayout(self)
        self.central_layout.setContentsMargins(16, 16, 16, 16)
        self.central_layout.setSpacing(16)

        self.central_layout.addStretch()

        self.file_count_label = QLabel(f"File Count: {file_count}")
        self.file_count_label.setStyleSheet(f"color: {dark_text_color.name()}; font-size: 16px;")
        self.central_layout.addWidget(self.file_count_label)

        self.central_layout.addStretch()

        self.correction_count_label = QLabel(f"Correction Count: {correction_count}")
        self.correction_count_label.setStyleSheet(f"color: {dark_text_color.name()}; font-size: 16px;")
        self.central_layout.addWidget(self.correction_count_label)

        self.central_layout.addStretch()

        self.tokens_used_label = QLabel(f"Tokens Used: {tokens_used}")
        self.tokens_used_label.setStyleSheet(f"color: {dark_text_color.name()}; font-size: 16px;")
        self.central_layout.addWidget(self.tokens_used_label)

        self.central_layout.addStretch()

class FileEditSideBar(QWidget):
    def __init__(self, user_id: str, file_id: str, new_file: bool, edit_mode: str):
        super().__init__()

        self.setStyleSheet(
            f"{type(self).__name__} {{"
            f"background-color: {secondary_color.name()}"
            "}"
        )

        self.file_loading_failed = None
        self.file_name, self.file_content = self.fetch_file_data(user_id, file_id)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.__init_body(new_file, edit_mode)

    def fetch_file_data(self, user_id: str, file_id: str) -> tuple[str, str]:
        try:
            url = f"http://127.0.0.1:5000/documents/{file_id}?user_id={user_id}"
            print(f"📡 Requesting file content from: {url}")
            headers = {"Content-Type": "application/json"}
            response = requests.get(url, headers=headers)

            print(f"📡 Response status: {response.status_code}")
            print(f"📦 Response body: {response.text}")

            response.raise_for_status()
            data = response.json()

            file_name = data.get("title", "Untitled")
            file_content = data.get("content", "")

            if not file_content.strip():
                print("⚠️ File content is empty.")
            else:
                print("✅ File content loaded successfully.")

            return file_name, file_content

        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching file edit side bar data: {e}")
            self.file_loading_failed = True
            return "Untitled", ""


    def __init_body(self, new_file: bool, edit_mode: str):
        self.central_layout = QVBoxLayout(self)
        self.central_layout.setContentsMargins(32, 32, 32, 32)
        self.central_layout.setSpacing(32)

        self.name_text_box = InputField(self.file_name)
        self.name_text_box.setStyleSheet(
            f"color: {dark_text_color.name()};"
            f"background-color: {primary_color.name()};"
            f"border: 1px solid {dark_text_color.name()};"
            "border-radius: 8px;"
            "padding: 0 4px;"
            "font-size: 30px;"
        )
        self.central_layout.addWidget(self.name_text_box)

        self.bar_one = QWidget()
        self.bar_one.setStyleSheet(f"background-color: {primary_color.name()};")
        self.bar_one.setFixedHeight(2)
        self.central_layout.addWidget(self.bar_one)

        if not new_file:
            self.invite_button = SecondaryButton("Invite Collaborator")
            self.central_layout.addWidget(self.invite_button)

            self.report_button = SecondaryButton("Report Collaborator")
            self.central_layout.addWidget(self.report_button)

            self.central_layout.addStretch()

            self.bar_two = QWidget()
            self.bar_two.setStyleSheet(f"background-color: {primary_color.name()};")
            self.bar_two.setFixedHeight(2)
            self.central_layout.addWidget(self.bar_two)

            self.delete_file_button = SecondaryButton("Delete File")
            self.central_layout.addWidget(self.delete_file_button)
        else:
            if edit_mode == "llm":
                self.suggestions_area = QScrollArea()
                self.suggestions_area.setWidgetResizable(True)
                self.suggestions_area.setStyleSheet(f"background-color: {primary_color.darker(105).name()}; border: 1px solid {dark_text_color.lighter(400).name()};")
                self.central_layout.addWidget(self.suggestions_area)

                self.suggestion_container = QWidget()
                self.suggestion_container.setStyleSheet("border: 0px;")
                self.suggestions_area.setWidget(self.suggestion_container)

                self.suggestion_container_layout = QVBoxLayout()
                self.suggestion_container_layout.setContentsMargins(16, 16, 16, 16)
                self.suggestion_container_layout.setSpacing(16)
                self.suggestion_container.setLayout(self.suggestion_container_layout)
            else:
                self.central_layout.addStretch()

class FilePreview(QWidget):
    def __init__(self, file_name: str, file_head: str):
        super().__init__()

        self.setStyleSheet(
            f"{type(self).__name__} {{"
            f"background-color: {primary_color.darker(105).name()};"
            "border: 0px;"
            "}"
        )

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)
        self.__init_body(file_name, file_head)

    def __init_body(self, file_name: str, file_head: str):
        self.central_layout = QHBoxLayout(self)
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.central_layout.setSpacing(16)

        self.file_icon = QLabel("🗎")
        self.file_icon.setStyleSheet(f"background-color: {dark_text_color.name()}; color: {primary_color.name()}; font-size: 56px; border-radius: 16px;")
        self.file_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.file_icon.setFixedSize(100, 100)
        self.central_layout.addWidget(self.file_icon)

        self.file_info_layout = QVBoxLayout()
        self.file_info_layout.setContentsMargins(0, 0, 0, 0)
        self.file_info_layout.setSpacing(0)
        self.central_layout.addLayout(self.file_info_layout)

        self.file_name = QLabel(file_name)
        self.file_name.setStyleSheet(f"color: {dark_text_color.name()}; font-size: 24px; font-weight: 600;")
        self.file_info_layout.addWidget(self.file_name)

        self.file_head = QLabel(file_head)
        self.file_head.setStyleSheet(f"color: {dark_text_color.name()}; font-size: 16px;")
        self.file_info_layout.addWidget(self.file_head)

        self.file_info_layout.addStretch()

        self.edit_file_label = ActionLabel("Edit File")
        self.file_info_layout.addWidget(self.edit_file_label)

        self.central_layout.addStretch()

class LLMSuggestion(QWidget):
    def __init__(self, diff_index, string_index, old_word, new_word):
        super().__init__()

        self.setStyleSheet(
            f"{type(self).__name__} {{"
            f"background-color: {primary_color.darker(105).name()};"
            "border-bottom: 1px solid;"
            "}"
        )

        self.diff_index = diff_index
        self.string_index = string_index

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.__init_body(old_word, new_word)

    def __init_body(self, old_word, new_word):
        self.central_layout = QVBoxLayout(self)
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.central_layout.setSpacing(0)

        self.text_label = QLabel(f"{self.diff_index}: Change {old_word} to {new_word}?")
        self.text_label.setStyleSheet(f"color: {dark_text_color.name()}")
        self.central_layout.addWidget(self.text_label)
        self.central_layout.setAlignment(self.text_label, Qt.AlignmentFlag.AlignCenter)

        self.accept_action_label = ActionLabel("Accept")
        self.central_layout.addWidget(self.accept_action_label)
        self.central_layout.setAlignment(self.accept_action_label, Qt.AlignmentFlag.AlignCenter)

        self.reject_action_label = ActionLabel("Reject")
        self.central_layout.addWidget(self.reject_action_label)
        self.central_layout.setAlignment(self.reject_action_label, Qt.AlignmentFlag.AlignCenter)