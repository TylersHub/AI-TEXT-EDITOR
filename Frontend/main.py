from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt6.QtCore import Qt

import sys
import requests

from page_sign_in import SignInPage
from page_sign_up import SignUpPage
from page_home import HomePage
from page_file_create import FileCreatePage
from page_file_edit import FileEditPage
from page_buy_tokens import BuyTokensPage
from page_blacklist import BlacklistPage
from page_applications import ApplicationsPage
from page_rejections import RejectionsPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("HungryText")
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        # Session Credentials

        self.session_token = None
        self.account_type = None
        self.user_id = None

        # Page Storage

        self.pages = {
            "SignIn": SignInPage(),
            "SignUp": SignUpPage(),
            "Home": None,
            "FileCreate": None,
            "FileEdit": None,
            "BuyTokens": None,
            "Blacklist": None,
            "Applications": None,
            "Rejections": None,
        }

        # Page Slots

        self.pages["SignIn"].session_credentials_received.connect(self.store_session_credentials)
        self.pages["SignIn"].navigate_to_sign_up.connect(lambda: self.switch_to_page("SignUp"))
        self.pages["SignIn"].navigate_to_home.connect(lambda: self.switch_to_page("Home"))

        self.pages["SignUp"].navigate_to_sign_in.connect(lambda: self.switch_to_page("SignIn"))

        # Page Loading

        self.central_widget.addWidget(self.pages["SignIn"])
        self.central_widget.addWidget(self.pages["SignUp"])

        # End Of Setup

        self.showMaximized()

    def store_session_credentials(self, token: str, acc_type: str, user_id: str):
        self.session_token = token
        self.account_type = acc_type
        self.user_id = user_id

    def clear_session_credentials(self):
        try:
            session_data = {"session_token": self.session_token}
            headers = {"Content-Type": "application/json"}

            response = requests.post("http://127.0.0.1:5000/auth/logout", json=session_data, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error clearing session: {e}")

        self.session_token = None
        self.account_type = None
        self.user_id = None

    def authenticate_session_credentials(self) -> bool:
        if not self.session_token or not self.account_type or not self.user_id or (self.account_type != "FREE" and self.account_type != "PAID" and self.account_type != "SUPER"):
            self.clear_session_credentials()
            return False

        try:
            # session_data = {"session_token": self.session_token, "account_type": self.account_type}
            session_data = {"session_token": self.session_token} # TEMP
            headers = {"Content-Type": "application/json"}

            response = requests.post("http://127.0.0.1:5000/auth/session/validate", json=session_data, headers=headers)
            response.raise_for_status()

            data = response.json()

            if data["valid"]:
                return True
            else:
                raise requests.exceptions.RequestException("Invalid session token")
        except requests.exceptions.RequestException as e:
            print(f"Error authenticating session: {e}")
            self.clear_session_credentials()
            return False

    def connect_side_bar(self, page: str):
        # Session Slots
        self.pages[page].side_bar.sign_out_requested.connect(self.clear_session_credentials)
        self.pages[page].side_bar.navigate_to_sign_in.connect(lambda: self.switch_to_page("SignIn"))

        # Side Bar Slots
        self.pages[page].side_bar.navigate_to_token_purchase.connect(lambda: self.switch_to_page("BuyTokens"))
        self.pages[page].side_bar.navigate_to_home.connect(lambda: self.switch_to_page("Home"))
        self.pages[page].side_bar.navigate_to_blacklist.connect(lambda: self.switch_to_page("Blacklist"))
        self.pages[page].side_bar.navigate_to_history.connect(lambda: self.switch_to_page("History"))
        self.pages[page].side_bar.navigate_to_invites.connect(lambda: self.switch_to_page("Invites"))

        # Side Bar Admin Slots
        self.pages[page].side_bar.navigate_to_applications.connect(lambda: self.switch_to_page("Applications"))
        self.pages[page].side_bar.navigate_to_rejections.connect(lambda: self.switch_to_page("Rejections"))
        self.pages[page].side_bar.navigate_to_complaints.connect(lambda: self.switch_to_page("Complaints"))
        self.pages[page].side_bar.navigate_to_moderation.connect(lambda: self.switch_to_page("Moderation"))
    
    def unload_page(self, page: str):
        self.central_widget.removeWidget(self.pages[page])
        self.pages[page].deleteLater()
        self.pages[page] = None
    
    def load_page(self, page: str, pars: dict = None):
        # Clear Pages And Redirect To Sign In If Invalid Credentials
        if self.authenticate_session_credentials() == False:
            print(f"Error (load_page): Page '{page}' given, but invalid credentials provided!")

            for pg in self.pages:
                if pg != "SignIn" and pg != "SignUp" and self.pages[pg] != None:
                    self.unload_page(pg)

            self.central_widget.setCurrentWidget(self.pages["SignIn"])

            return

        # Unload Page If It Already Exists
        if self.pages[page] != None:
            self.unload_page(page)

        # Load New Page
        if page == "Home":
            self.pages[page] = HomePage(self.session_token, self.account_type, self.user_id)

            # Side Bar Slots
            self.connect_side_bar(page)

            # File Slots
            self.pages[page].navigate_to_file_create.connect(lambda: self.switch_to_page("FileCreate"))
            self.pages[page].navigate_to_file_edit.connect(lambda file_id, edit_mode: self.switch_to_page("FileEdit", {"file_id": file_id, "edit_mode": edit_mode, "new_file": False}))
        elif page == "FileCreate":
            self.pages[page] = FileCreatePage(self.session_token, self.account_type, self.user_id)

            # Side Bar Slots
            self.connect_side_bar(page)

            # Submission Slot
            self.pages[page].navigate_to_file_edit.connect(lambda file_id, edit_mode: self.switch_to_page("FileEdit", {"file_id": file_id, "edit_mode": edit_mode, "new_file": True}))
        elif page == "FileEdit":
            self.pages[page] = FileEditPage(self.session_token, self.account_type, self.user_id, pars["file_id"], pars["edit_mode"], pars["new_file"])

            # Side Bar Slots
            self.connect_side_bar(page)
        elif page == "BuyTokens":
            self.pages[page] = BuyTokensPage(self.session_token, self.account_type, self.user_id)

            # Side Bar Slots
            self.connect_side_bar(page)
        elif page == "Blacklist":
            self.pages[page] = BlacklistPage(self.session_token, self.account_type, self.user_id)

            # Side Bar Slots
            self.connect_side_bar(page)
        elif page == "Applications":
            self.pages[page] = ApplicationsPage(self.session_token, self.account_type, self.user_id)

            # Side Bar Slots
            self.connect_side_bar(page)
        elif page == "Rejections":
            self.pages[page] = RejectionsPage(self.session_token, self.account_type, self.user_id)

            # Side Bar Slots
            self.connect_side_bar(page)

        self.central_widget.addWidget(self.pages[page])
        self.central_widget.setCurrentWidget(self.pages[page])

    def switch_to_page(self, page: str, pars: dict = None):
        if page not in self.pages:
            print(f"Error (switch_to_page): Page '{page}' not found in Pages!")
            return
        
        if page == "SignIn" or page == "SignUp":
            self.central_widget.setCurrentWidget(self.pages[page])
            return

        self.load_page(page, pars)

    def closeEvent(self, event):
        self.clear_session_credentials()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())