from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QSizePolicy
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt

class Page(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("Page { background-color: white; }")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

class HeaderText(QLabel):
    def __init__(self, text: str):
        super().__init__(text)

        self.setStyleSheet(
            f"{type(self).__name__} {{"
            "color: black;"
            "font-size: 40px;"
            "font-weight: 550;"
            "}"
        )

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

class InputLabel(QLabel):
    def __init__(self, text: str):
        super().__init__(text)

        self.setStyleSheet(
            f"{type(self).__name__} {{"
            "color: black;"
            "font-size: 12px;"
            "}"
        )

class InputWarningLabel(QLabel):
    def __init__(self, text: str = None):
        super().__init__(text)

        self.is_text_visible = False

        self.setStyleSheet(
            f"{type(self).__name__} {{"
            "color: transparent;"
            "font-size: 12px;"
            "}"
        )

    def toggle_text(self, show_text: bool):
        if show_text: 
            self.is_text_visible = True
            self.setStyleSheet(f"{type(self).__name__} {{ color: red; }}")
        else:
            self.is_text_visible = False
            self.setStyleSheet(f"{type(self).__name__} {{ color: transparent; }}")

class InputField(QLineEdit):
    def __init__(self, text: str = None, is_sensitive = False):
        super().__init__(text)

        self.setStyleSheet(
            f"{type(self).__name__} {{"
            "background-color: rgb(240, 240, 240);"
            "color: black;"
            "font-size: 15px;"
            "}"
        )

        if is_sensitive: self.setEchoMode(QLineEdit.EchoMode.Password)

class ActionLabel(QPushButton):
    def __init__(self, text: str):
        super().__init__(text)

        self.setStyleSheet(
            f"{type(self).__name__} {{"
            "background-color: transparent;"
            "color: purple;"
            "font-size: 12px;"
            "text-align: left;"
            "}"
        )

        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setFlat(True)

class PrimaryButton(QPushButton):
    def __init__(self, text: str = None):
        super().__init__(text)

        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))