from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from PyQt6.QtCore import Qt

from frontend.page_sign_in import SignInPage
from frontend.page_sign_up import SignUpPage
from frontend.page_home import HomePage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("HungryText")
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.session_token = None
        self.account_type = None

        self.pages = {
            "SignIn": SignInPage(),
            "SignUp": SignUpPage(),
            "Home": None,
            "FileCreate": None,
            "FileEdit": None,
        }

        self.pages["SignIn"].session_credentials_received.connect(self.store_session_credentials)
        self.pages["SignIn"].navigate_to_sign_up.connect(lambda: self.switch_to_page("SignUp"))
        self.pages["SignIn"].navigate_to_home.connect(lambda: self.switch_to_page("Home"))

        self.pages["SignUp"].navigate_to_sign_in.connect(lambda: self.switch_to_page("SignIn"))

        self.central_widget.addWidget(self.pages["SignIn"])
        self.central_widget.addWidget(self.pages["SignUp"])

        self.showMaximized()

    def store_session_credentials(self, token, acc_type):
        self.session_token = token
        self.account_type = acc_type

    def clear_session_credentials(self):
        self.session_token = None
        self.account_type = None

    def authenticate_session_credentials(self) -> bool:
        if not self.session_token or not self.account_type or self.account_type not in {"FREE", "PAID", "SUPER"}:
            self.session_token = None
            self.account_type = None
            return False
        return True

    def unload_page(self, page: str):
        self.central_widget.removeWidget(self.pages[page])
        self.pages[page].deleteLater()
        self.pages[page] = None

    def load_page(self, page: str, pars: dict = None):
        if not self.authenticate_session_credentials():
            print(f"Error (load_page): Invalid credentials, redirecting to SignIn.")
            for pg in self.pages:
                if pg not in {"SignIn", "SignUp"} and self.pages[pg] is not None:
                    self.unload_page(pg)
            self.central_widget.setCurrentWidget(self.pages["SignIn"])
            return

        if self.pages[page] is not None:
            self.unload_page(page)

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
            print(f"Error (switch_to_page): Page '{page}' not found!")
            return

        if page in {"SignIn", "SignUp"}:
            self.central_widget.setCurrentWidget(self.pages[page])
            return

        self.load_page(page, pars)
