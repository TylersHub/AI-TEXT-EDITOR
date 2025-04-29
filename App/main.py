from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
import sys

from page_sign_in import SignInPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("HungryText")

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.pages = {
            "SignIn": SignInPage()
        }

        for page in self.pages.values():
            self.central_widget.addWidget(page)

        self.showMaximized()

    def switch_to_page(self, page: str):
        self.central_widget.setCurrentWidget(self.pages[page])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())