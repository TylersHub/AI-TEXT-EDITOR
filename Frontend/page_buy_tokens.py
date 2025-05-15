from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
from Frontend.util_widgets import Page, SideBar, HeaderText, InputLabel, InputField, InputWarningLabel, ActionLabel, PrimaryButton
from Frontend.util_widgets import dark_text_color

import requests

class BuyTokensPage(Page):
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

        self.body_header = QLabel("Buy Tokens!")
        self.body_header.setStyleSheet(f"color: {dark_text_color.name()}; font-size: 32px; font-weight: 600;")
        self.body_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body_layout.addWidget(self.body_header)

        self.body_layout.addStretch()

        self.button_layout = QHBoxLayout()
        self.button_layout.setContentsMargins(0, 0, 0, 0)
        self.button_layout.setSpacing(32)
        self.body_layout.addLayout(self.button_layout)

        self.buy_100_button = PrimaryButton("100 Tokens ($1 USD)")
        self.buy_100_button.clicked.connect(lambda: self.buy_tokens(100))
        self.button_layout.addWidget(self.buy_100_button)

        self.buy_250_button = PrimaryButton("250 Tokens ($2.50 USD)")
        self.buy_250_button.clicked.connect(lambda: self.buy_tokens(250))
        self.button_layout.addWidget(self.buy_250_button)

        self.buy_500_button = PrimaryButton("500 Tokens ($4.50 USD)")
        self.buy_500_button.clicked.connect(lambda: self.buy_tokens(500))
        self.button_layout.addWidget(self.buy_500_button)

        self.buy_1000_button = PrimaryButton("1000 Tokens ($9.00 USD)")
        self.buy_1000_button.clicked.connect(lambda: self.buy_tokens(1000))
        self.button_layout.addWidget(self.buy_1000_button)

        self.body_layout.addStretch()

    def buy_tokens(self, amount: int):
        try:
            internal_data = {"amount": amount, "user_id": self.user_id}
            headers = {"Content-Type": "application/json"}

            response = requests.post(f"http://127.0.0.1:5000/tokens/add", json=internal_data, headers=headers)
            response.raise_for_status()

            file_previews = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error buying tokens: {e}")

        self.side_bar.navigate_to_home.emit()