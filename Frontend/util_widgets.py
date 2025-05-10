from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QSizePolicy
from PyQt6.QtGui import QColor, QCursor
from PyQt6.QtCore import Qt

# Color Palette
primary_color = QColor("#F8F8FF")
secondary_color = QColor("#7D55C7")
accent_color = QColor("#8e78a3")
dark_text_color = QColor("#252525")
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
            f"color: {accent_color.name()};"
            "background-color: transparent;"
            "font-size: 12px;"
            "font-weight: 600;"
            "text-align: left;"
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
            f"background-color: {accent_color.name()};"
            "border-radius: 8px;"
            "height: 32px;"
            "font-size: 16px;"
            "font-weight: 600;"
            "}"
        )

        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))