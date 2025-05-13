from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt6.QtCore import Qt

import sys
import requests

from page_sign_in import SignInPage
from page_sign_up import SignUpPage
from page_home import HomePage

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

        # Page Storage

        self.pages = {
            "SignIn": SignInPage(),
            "SignUp": SignUpPage(),
            "Home": None,
        }

        # Page Slots

        self.pages["SignIn"].session_credentials_received.connect(self.store_session_credentials)
        self.pages["SignIn"].navigate_to_sign_up.connect(lambda: self.switch_to_page("SignUp"))
        self.pages["SignIn"].navigate_to_home.connect(lambda: self.switch_to_page("Home"))

        self.pages["SignUp"].navigate_to_sign_in.connect(lambda: self.switch_to_page("SignIn"))

        # Page Loading

        self.central_widget.addWidget(self.pages["SignIn"])
        self.central_widget.addWidget(self.pages["SignUp"])

        ###########################
        ###### TEMP: TESTING ######
        # self.session_token = 12345
        # self.account_type = "PAID"
        # self.switch_to_page("Home")
        ###### TEMP: TESTING ######
        ###########################

        # End Of Setup

        self.showMaximized()

    def store_session_credentials(self, token, acc_type):
        self.session_token = token
        self.account_type = acc_type

    def clear_session_credentials(self):
        # API ENDPOINT #
        # Tell Backend To Discard Session Token
        # API ENDPOINT #

        self.session_token = None
        self.account_type = None

    def authenticate_session_credentials(self) -> bool:
        if not self.session_token or not self.account_type or (self.account_type != "FREE" and self.account_type != "PAID" and self.account_type != "SUPER"):
            self.session_token = None
            self.account_type = None

            return False
        
        # API ENDPOINT #
        # Ask Backend To Verify Session Token And Account Type
        # API ENDPOINT #
        
        # TEMP
        return True
        # TEMP

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
            self.pages[page] = HomePage(self.session_token, self.account_type)
            self.pages[page].sign_out_requested.connect(self.clear_session_credentials)
            self.pages[page].navigate_to_sign_in.connect(lambda: self.switch_to_page("SignIn"))
            self.pages[page].navigate_to_file_edit.connect(lambda file_id: self.switch_to_page("FileCreate", {"file_id": file_id}))
        elif page == "FileEdit":
            pass
        elif page == "FileCreate":
            pass

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())