from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QScrollArea, QWidget
from PyQt6.QtCore import Qt, pyqtSignal
from util_widgets import Page, HomeSideBar, PrimaryButton, FilePreview
from util_widgets import primary_color, dark_text_color

import requests

class HomePage(Page):
    # Session Signals
    sign_out_requested = pyqtSignal()
    navigate_to_sign_in = pyqtSignal()

    # File Signals
    navigate_to_file_edit = pyqtSignal(int)
    navigate_to_file_create = pyqtSignal()

    # Menu Bar Signals
    navigate_to_token_purchase = pyqtSignal()
    navigate_to_settings = pyqtSignal()
    navigate_to_history = pyqtSignal()
    navigate_to_invites = pyqtSignal()
    navigate_to_blacklist = pyqtSignal()

    # Menu Bar Admin Signals
    navigate_to_applications = pyqtSignal()
    navigate_to_rejections = pyqtSignal()
    navigate_to_complaints = pyqtSignal()
    navigate_to_moderation = pyqtSignal()

    def __init__(self, session_token: int, account_type: str):
        super().__init__()

        self.central_layout = QHBoxLayout(self)
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.central_layout.setSpacing(0)

        # API ENDPOINT FOR USERNAME AND TOKEN COUNT #

        user_name = "test101"
        token_count = 1337

        self.side_bar = HomeSideBar(account_type, user_name, token_count)
        self.side_bar.buy_token_button.clicked.connect(self.on_buy_token_click)
        self.side_bar.settings_button.clicked.connect(self.on_settings_click)
        self.side_bar.history_button.clicked.connect(self.on_history_click)
        self.side_bar.invites_button.clicked.connect(self.on_invites_click)
        self.side_bar.blacklist_button.clicked.connect(self.on_blacklist_click)
        self.side_bar.sign_out_button.clicked.connect(self.on_sign_out_click)

        if account_type == "SUPER":
            self.side_bar.applications_button.clicked.connect(self.on_applications_click)
            self.side_bar.rejections_button.clicked.connect(self.on_rejections_click)
            self.side_bar.complaints_button.clicked.connect(self.on_complaints_click)
            self.side_bar.moderation_button.clicked.connect(self.on_moderation_click)

        self.central_layout.addWidget(self.side_bar, stretch=2)

        self.body_layout = QVBoxLayout()
        self.body_layout.setContentsMargins(32, 32, 32, 32)
        self.body_layout.setSpacing(32)
        self.central_layout.addLayout(self.body_layout, stretch=8)

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

        self.__init_files(session_token)

        self.new_file_button = PrimaryButton("New File")
        self.new_file_button.clicked.connect(self.on_new_file_click)
        self.body_layout.addWidget(self.new_file_button)
        self.body_layout.setAlignment(self.new_file_button, Qt.AlignmentFlag.AlignHCenter)

    def __init_files(self, session_token: int):
        # API ENDPOINT #
        # Ask Backend To Return File Details For All Files Of User
        # File Details: File Name, File Head, File ID
        # API ENDPOINT #

        # TEMP #
        for i in range(10):
            fp = FilePreview(f"File #{i}", "Lorem ipsum e pluribus ...", i)
            fp.edit_file_label.clicked.connect(lambda file_id: self.on_edit_file_click(i))
            self.file_container_layout.addWidget(fp)
        # TEMP #
    
    def on_sign_out_click(self):
        self.sign_out_requested.emit()
        self.navigate_to_sign_in.emit()
    
    def on_edit_file_click(self, file_id: int):
        self.navigate_to_file_edit.emit(file_id)
    
    def on_new_file_click(self):
        self.navigate_to_file_create.emit()
    
    def on_buy_token_click(self):
        self.navigate_to_token_purchase.emit()
    
    def on_settings_click(self):
        self.navigate_to_settings.emit()

    def on_history_click(self):
        self.navigate_to_history.emit()

    def on_invites_click(self):
        self.navigate_to_invites.emit()

    def on_blacklist_click(self):
        self.navigate_to_blacklist.emit()

    def on_applications_click(self):
        self.navigate_to_applications.emit()

    def on_rejections_click(self):
        self.navigate_to_rejections.emit()
    
    def on_complaints_click(self):
        self.navigate_to_complaints.emit()

    def on_moderation_click(self):
        self.navigate_to_moderation.emit()