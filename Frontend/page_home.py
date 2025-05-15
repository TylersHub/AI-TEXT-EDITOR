from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QScrollArea, QWidget
from PyQt6.QtCore import Qt, pyqtSignal
from util_widgets import Page, SideBar, TopBar, PrimaryButton, FilePreview
from util_widgets import primary_color, dark_text_color

import requests

class HomePage(Page):
    # File Signals
    navigate_to_file_create = pyqtSignal()
    navigate_to_file_edit = pyqtSignal(int)

    def __init__(self, session_token: str, account_type: str, user_id: str):
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

        self.body_header = QLabel("Welcome to HungryText")
        self.body_header.setStyleSheet(f"color: {dark_text_color.name()}; font-size: 32px; font-weight: 600;")
        self.body_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body_layout.addWidget(self.body_header)

        if account_type in ("PAID", "SUPER"):
            self.top_bar = TopBar(user_id)
            self.body_layout.addWidget(self.top_bar)

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

        if account_type in ("PAID", "SUPER"):
            self.file_previews = []
            self.__init_file_previews()
        else:
            self.file_container_layout.addStretch()

            self.upgrade_message = QLabel("Buy Tokens to save files!")
            self.upgrade_message.setStyleSheet(f"color: {dark_text_color.name()}; font-size: 24px; font-weight: 600;")
            self.file_container_layout.addWidget(self.upgrade_message)
            self.file_container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            self.file_container_layout.addStretch()

        self.new_file_button = PrimaryButton("New File")
        self.new_file_button.clicked.connect(self.navigate_to_file_create.emit)
        self.body_layout.addWidget(self.new_file_button)
        self.body_layout.setAlignment(self.new_file_button, Qt.AlignmentFlag.AlignHCenter)

    def fetch_file_previews(self) -> list[dict]:
        file_previews = []

        try:
            headers = {"Content-Type": "application/json"}

            response = requests.get(f"http://127.0.0.1:5000/documents/previews/{self.user_id}", headers=headers)
            response.raise_for_status()

            file_previews = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching file previews: {e}")

        return file_previews
    
    def __init_file_previews(self):
        file_prevs = self.fetch_file_previews()

        for file_prev in file_prevs:
            file_pr = FilePreview(file_prev["title"], file_prev["preview"])
            file_pr.edit_file_label.clicked.connect(lambda: self.navigate_to_file_edit.emit(file_prev["id"]))
            self.file_previews.append(file_pr)
            self.file_container_layout.addWidget(file_pr)

        self.file_container_layout.addStretch(1)