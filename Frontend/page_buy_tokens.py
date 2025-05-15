from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtCore import pyqtSignal
from Frontend.util_widgets import Page, HeaderText, InputLabel, InputField, InputWarningLabel, ActionLabel, PrimaryButton

import requests

class BuyTokensPage(Page):
    def __init__(self):
        super().__init__()

        