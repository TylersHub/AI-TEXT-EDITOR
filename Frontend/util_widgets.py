from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QSizePolicy, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QColor, QCursor
from PyQt6.QtCore import Qt

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

class HomeSideBar(QWidget):
    def __init__(self, account_type: str, user_name: str, token_count: int):
        super().__init__()

        self.setStyleSheet(
            f"{type(self).__name__} {{"
            f"background-color: {secondary_color.name()}"
            "}"
        )

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.account_type = account_type
        self.user_name = user_name
        self.token_count = token_count
        self.__init_body()

    def __init_body(self):
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

        self.token_count = QLabel(f"Tokens: {self.token_count}")
        self.token_count.setStyleSheet(f"color: {primary_color.name()}; font-size: 24px;")
        self.token_layout.addWidget(self.token_count)

        self.token_layout.addStretch()

        self.buy_token_button = QPushButton("➕")
        self.buy_token_button.setStyleSheet(f"background-color: {primary_color.name()}; color: {dark_text_color.name()}; font-size: 16px; border-radius: 16px;")
        self.buy_token_button.setMinimumSize(32, 32)
        self.buy_token_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.token_layout.addWidget(self.buy_token_button)

        self.bar_two = QWidget()
        self.bar_two.setStyleSheet(f"background-color: {primary_color.name()};")
        self.bar_two.setFixedHeight(2)
        self.central_layout.addWidget(self.bar_two)

        self.settings_button = SecondaryButton("Settings")
        self.central_layout.addWidget(self.settings_button)

        self.history_button = SecondaryButton("History")
        self.central_layout.addWidget(self.history_button)

        if self.account_type == "SUPER":
            self.complaints_button = SecondaryButton("Complaints")
            self.central_layout.addWidget(self.complaints_button)

            self.rejections_button = SecondaryButton("Rejections")
            self.central_layout.addWidget(self.rejections_button)

        self.central_layout.addStretch()

        self.bar_three = QWidget()
        self.bar_three.setStyleSheet(f"background-color: {primary_color.name()};")
        self.bar_three.setFixedHeight(2)
        self.central_layout.addWidget(self.bar_three)

        self.sign_out_button = SecondaryButton("Sign Out")
        self.central_layout.addWidget(self.sign_out_button)

class FilePreview(QWidget):
    def __init__(self, file_name: str, file_head: str, file_id: int):
        super().__init__()

        self.setStyleSheet(
            f"{type(self).__name__} {{"
            f"background-color: {primary_color.darker(105).name()};"
            "border: 0px;"
            "}"
        )

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.__init_body(file_name, file_head, file_id)

    def __init_body(self, file_name: str, file_head: str, file_id: int):
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