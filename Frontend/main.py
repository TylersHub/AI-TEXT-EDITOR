from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt6.QtCore import Qt
import sys

from page_sign_in import SignInPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("HungryText")
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        # Page Loading

        self.pages = {
            "SignIn": SignInPage()
        }

        for page in self.pages.values():
            self.central_widget.addWidget(page)

        # Session Token Storage

        self.session_token = None

        self.pages["SignIn"].session_token_received.connect(self.store_session_token)

        # Page Navigation

        self.pages["SignIn"].navigate_to_home.connect(lambda: self.switch_to_page("Home"))
        self.pages["SignIn"].navigate_to_sign_up.connect(lambda: self.switch_to_page("SignUp"))

        # End Of Setup

        self.showMaximized()

    def store_session_token(self, token):
        self.session_token = token

    def switch_to_page(self, page: str):
        if page in self.pages:
            self.central_widget.setCurrentWidget(self.pages[page])
        else:
            print(f"Error (switch_to_page): Page '{page}' not found in Pages!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())