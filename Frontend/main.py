import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt6.QtCore import Qt

# Adds the parent directory to sys.path so 'llm' becomes importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from llm.llm_local import ensure_ollama_ready

from page_sign_in import SignInPage
from page_sign_up import SignUpPage
from page_llm_test import LLMTestPage


MODEL = "llama3.2"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("HungryText")
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        # Page Loading
        self.pages = {
            "SignIn": SignInPage(),
            "SignUp": SignUpPage(),
            "LLMTest": LLMTestPage(),
        }

        for page in self.pages.values():
            self.central_widget.addWidget(page)

        # Session Token Storage
        self.session_token = None
        self.pages["SignIn"].session_token_received.connect(self.store_session_token)

        # Page Navigation
        self.pages["SignIn"].navigate_to_home.connect(lambda: self.switch_to_page("Home"))
        self.pages["SignIn"].navigate_to_sign_up.connect(lambda: self.switch_to_page("SignUp"))
        self.pages["SignUp"].navigate_to_sign_in.connect(lambda: self.switch_to_page("SignIn"))
        self.pages["SignIn"].navigate_to_llm_test.connect(lambda: self.switch_to_page("LLMTest"))


    def store_session_token(self, token):
        self.session_token = token

    def switch_to_page(self, page: str):
        if page in self.pages:
            self.central_widget.setCurrentWidget(self.pages[page])
        else:
            print(f"Error (switch_to_page): Page '{page}' not found in Pages!")

def main():
    try:
        print(f"🔄 Initializing model '{MODEL}'...")
        ensure_ollama_ready(MODEL)
        print(f"✅ Model '{MODEL}' is ready.")

        app = QApplication(sys.argv)
        window = MainWindow()
        window.showMaximized()
        sys.exit(app.exec())

    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
