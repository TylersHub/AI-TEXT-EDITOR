from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HungryText Prototype")
        self.setStyleSheet("background-color: white")
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        layout.setSpacing(50)

        # TITLE

        title = QLabel("Your Best Value Proposition")
        title.setStyleSheet("color: black; font-size: 50px")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # SUBTITLE

        subtitle = QLabel("\"If you don't try this app, you won't become the superhero you were meant to be!\"")
        subtitle.setStyleSheet("color: black; font-size: 15px")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)

        sub_layout = QHBoxLayout()

        # TOKEN BOX 1

        box_1 = QWidget()
        box_1.setFixedSize(250, 375)
        box_1.setStyleSheet("background-color: rgb(235, 235, 235);")
        wid_layout = QVBoxLayout(box_1)

        inner_box_1 = QWidget()
        inner_box_1.setFixedSize(232, 232)
        inner_box_1.setStyleSheet("background-color: rgb(25, 25, 25)")
        wid_layout.addWidget(inner_box_1)

        token_count = QLabel("250 Tokens")
        token_count.setStyleSheet("color: black; font-size: 25px")
        token_count.setAlignment(Qt.AlignmentFlag.AlignCenter)
        wid_layout.addWidget(token_count)

        price_button = QPushButton("$2.50 USD")
        price_button.setFixedHeight(50)
        price_button.setStyleSheet("""
                                    QPushButton {
                                        font-size: 15px; border: 2px solid black; color: black; border-radius: 6px;
                                    }
                                    QPushButton:hover {
                                        background-color: rgb(200, 200, 200);
                                    }
                                    """)

        price_button.clicked.connect(lambda: self.on_button_clicked(250))
        wid_layout.addWidget(price_button)

        # TOKEN BOX 2

        box_2 = QWidget()
        box_2.setFixedSize(250, 375)
        box_2.setStyleSheet("background-color: rgb(235, 235, 235);")
        wid_layout = QVBoxLayout(box_2)

        inner_box_1 = QWidget()
        inner_box_1.setFixedSize(232, 232)
        inner_box_1.setStyleSheet("background-color: rgb(25, 25, 25)")
        wid_layout.addWidget(inner_box_1)

        token_count = QLabel("500 Tokens")
        token_count.setStyleSheet("color: black; font-size: 25px")
        token_count.setAlignment(Qt.AlignmentFlag.AlignCenter)
        wid_layout.addWidget(token_count)

        price_button = QPushButton("$4.50 USD")
        price_button.setFixedHeight(50)
        price_button.setStyleSheet("""
                                    QPushButton {
                                        font-size: 15px; border: 2px solid black; color: black; border-radius: 6px;
                                    }
                                    QPushButton:hover {
                                        background-color: rgb(200, 200, 200);
                                    }
                                    """)
        price_button.clicked.connect(lambda: self.on_button_clicked(500))
        wid_layout.addWidget(price_button)

        # TOKEN BOX 3

        box_3 = QWidget()
        box_3.setFixedSize(250, 375)
        box_3.setStyleSheet("background-color: rgb(235, 235, 235);")
        wid_layout = QVBoxLayout(box_3)

        inner_box_1 = QWidget()
        inner_box_1.setFixedSize(232, 232)
        inner_box_1.setStyleSheet("background-color: rgb(25, 25, 25)")
        wid_layout.addWidget(inner_box_1)

        token_count = QLabel("1000 Tokens")
        token_count.setStyleSheet("color: black; font-size: 25px")
        token_count.setAlignment(Qt.AlignmentFlag.AlignCenter)
        wid_layout.addWidget(token_count)

        price_button = QPushButton("$9.00 USD")
        price_button.setFixedHeight(50)
        price_button.setStyleSheet("""
                                    QPushButton {
                                        font-size: 15px; border: 2px solid black; color: black; border-radius: 6px;
                                    }
                                    QPushButton:hover {
                                        background-color: rgb(200, 200, 200);
                                    }
                                    """)
        price_button.clicked.connect(lambda: self.on_button_clicked(1000))
        wid_layout.addWidget(price_button)

        # TOKEN BOX 4

        box_4 = QWidget()
        box_4.setFixedSize(250, 375)
        box_4.setStyleSheet("background-color: rgb(235, 235, 235);")
        wid_layout = QVBoxLayout(box_4)

        inner_box_1 = QWidget()
        inner_box_1.setFixedSize(232, 232)
        inner_box_1.setStyleSheet("background-color: rgb(25, 25, 25)")
        wid_layout.addWidget(inner_box_1)

        token_count = QLabel("2500 Tokens")
        token_count.setStyleSheet("color: black; font-size: 25px")
        token_count.setAlignment(Qt.AlignmentFlag.AlignCenter)
        wid_layout.addWidget(token_count)

        price_button = QPushButton("$20.00 USD")
        price_button.setFixedHeight(50)
        price_button.setStyleSheet("""
                                    QPushButton {
                                        font-size: 15px; border: 2px solid black; color: black; border-radius: 6px;
                                    }
                                    QPushButton:hover {
                                        background-color: rgb(200, 200, 200);
                                    }
                                    """)
        price_button.clicked.connect(lambda: self.on_button_clicked(2500))
        wid_layout.addWidget(price_button)

        # END OF TOKEN BOXES

        sub_layout.addWidget(box_1)
        sub_layout.addWidget(box_2)
        sub_layout.addWidget(box_3)
        sub_layout.addWidget(box_4)

        layout.addLayout(sub_layout)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.setCentralWidget(central_widget)

    def on_button_clicked(self, token_count):
        print(f"{token_count} button clicked")
        self.load_other_page(token_count)

    def load_other_page(self, token_count):
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        # TITLE

        title = QLabel(f"To Be Added: Page to purchase {token_count} tokens.")
        title.setStyleSheet("color: black; font-size: 50px")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())