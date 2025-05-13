from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QScrollArea, QWidget
from PyQt6.QtCore import Qt, pyqtSignal
from util_widgets import Page, SideBar, PrimaryButton, FilePreview
from util_widgets import primary_color, dark_text_color

import requests

class HomePage(Page):
    # File Signals
    navigate_to_file_edit = pyqtSignal(int)
    navigate_to_file_create = pyqtSignal()

    def __init__(self, session_token: int, account_type: str):
        super().__init__()

        self.session_token = session_token
        self.account_type = account_type

        self.central_layout = QHBoxLayout(self)
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.central_layout.setSpacing(0)

        # user_name, token_count = self.fetch_username_and_tokens(session_token)

        # TEMP #
        user_name = "test101"
        token_count = 1337
        # TEMP #

        self.side_bar = SideBar(account_type, user_name, token_count)
        self.central_layout.addWidget(self.side_bar, stretch=1)

        self.body_layout = QVBoxLayout()
        self.body_layout.setContentsMargins(32, 32, 32, 32)
        self.body_layout.setSpacing(32)
        self.central_layout.addLayout(self.body_layout, stretch=4)

        self.body_header = QLabel("Welcome to HungryText")
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

        self.__init_files()

        self.new_file_button = PrimaryButton("New File")
        self.new_file_button.clicked.connect(self.navigate_to_file_create.emit)
        self.body_layout.addWidget(self.new_file_button)
        self.body_layout.setAlignment(self.new_file_button, Qt.AlignmentFlag.AlignHCenter)

    def fetch_username_and_tokens(self) -> tuple[str, str]:
        # API ENDPOINT #
        # Ask Backend To Return First Name And Token Count Of User
        # API ENDPOINT #

        pass

    def fetch_file_previews(self) -> list:
        # API ENDPOINT #
        # Ask Backend To Return File Details For All Files Of User
        # File Details: File Name, File Head, File ID
        # API ENDPOINT #
        
        pass
    
    def __init_files(self):
        # file_previews = self.fetch_file_previews()

        # for file_prev in file_previews:
        #     ...

        # TEMP #
        for i in range(10):
            fp = FilePreview(f"File #{i}", "Lorem ipsum e pluribus ...", i)
            fp.edit_file_label.clicked.connect(lambda file_id: self.navigate_to_file_edit.emit(i))
            self.file_container_layout.addWidget(fp)
        # TEMP #