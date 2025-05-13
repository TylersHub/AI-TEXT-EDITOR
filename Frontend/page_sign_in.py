from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtCore import pyqtSignal
from util_widgets import Page, HeaderText, InputLabel, InputField, InputWarningLabel, ActionLabel, PrimaryButton
from util_functions import validate_email, validate_password

import requests

class SignInPage(Page):
    session_credentials_received = pyqtSignal(int, str)
    navigate_to_home = pyqtSignal()
    navigate_to_sign_up = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.central_layout = QVBoxLayout(self)
        self.central_layout.addStretch()

        # Header Section

        self.sign_in_header = HeaderText("Enter HungryText")
        self.central_layout.addWidget(self.sign_in_header)

        # Email Section

        self.email_label = InputLabel("Email")
        self.central_layout.addWidget(self.email_label)

        self.email_input = InputField()
        self.central_layout.addWidget(self.email_input)

        self.email_warning_label = InputWarningLabel("Invalid email")
        self.central_layout.addWidget(self.email_warning_label)

        # Password Section

        self.password_label = InputLabel("Password")
        self.central_layout.addWidget(self.password_label)

        self.password_input = InputField(is_sensitive=True)
        self.central_layout.addWidget(self.password_input)

        self.password_warning_label = InputWarningLabel("Invalid password")
        self.central_layout.addWidget(self.password_warning_label)

        # self.forgot_password_label = ActionLabel("Forgot password?")
        # self.forgot_password_label.clicked.connect(self.on_forgot_password_click)
        # self.central_layout.addWidget(self.forgot_password_label)

        # Call-To-Action

        self.sign_in_button = PrimaryButton("Sign In")
        self.sign_in_button.clicked.connect(self.on_sign_in_click)
        self.central_layout.addWidget(self.sign_in_button)

        self.sign_up_label = ActionLabel("Don't have an account?")
        self.sign_up_label.clicked.connect(self.on_sign_up_click)
        self.central_layout.addWidget(self.sign_up_label)

        # Form Submission Shortcuts

        self.email_input.returnPressed.connect(self.sign_in_button.click)
        self.password_input.returnPressed.connect(self.sign_in_button.click)

        # End Of Layout

        self.central_layout.addStretch()

    def __flush(self):
        for input_field in self.findChildren(InputField):
            input_field.clear()

        for input_warning_label in self.findChildren(InputWarningLabel):
            input_warning_label.toggle_text(False)

    def on_sign_in_click(self):
        email_input_text = self.email_input.text()
        password_input_text = self.password_input.text()
        invalid_input = False
        incorrect_input = False
        session_token = None
        account_type = None

        # Email Input Validation

        is_email_input_valid, invalid_email_input_error = validate_email(email_input_text)

        if is_email_input_valid == False:
            if invalid_email_input_error == "EMPTY":
                self.email_warning_label.setText("Please enter an email")
            elif invalid_email_input_error == "INVALID":
                self.email_warning_label.setText("Please enter a valid email")

            self.email_warning_label.toggle_text(True)
            invalid_input = True
        else:
            self.email_warning_label.toggle_text(False)

        # Password Input Validation

        is_password_input_valid, invalid_password_input_error = validate_password(password_input_text)

        if is_password_input_valid == False:
            if invalid_password_input_error == "EMPTY":
                self.password_warning_label.setText("Please enter a password")
            elif invalid_password_input_error == "INVALID":
                self.password_warning_label.setText("Please enter a valid password")

            self.password_warning_label.toggle_text(True)
            invalid_input = True
        else:
            self.password_warning_label.toggle_text(False)

        if invalid_input:
            return
        
        # Input Authentication

        try:
            login_data = {"email": email_input_text, "password": password_input_text}
            headers = {"Content-Type": "application/json"}

            response = requests.post("http://127.0.0.1:5000/auth/login", json=login_data, headers=headers)
            response.raise_for_status()

            data = response.json()

            if data["success"] == False:
                if data["error"] == "Invalid credentials":
                    self.email_warning_label.setText("Incorrect email or password")
                    self.password_warning_label.setText("Incorrect email or password")
                elif data["error"] == "Account temporarily locked":
                    self.email_warning_label.setText("Account temporarily locked")
                    self.password_warning_label.setText("Account temporarily locked")
                else:
                    raise requests.exceptions.RequestException(f"Invalid failure message '{data["error"]}'")
                    
                self.email_warning_label.toggle_text(True)
                self.password_warning_label.toggle_text(True)
                incorrect_input = True
            elif data["success"] == True:
                session_token = data["session_token"]
                account_type = data["account_type"].upper()
            else:
                raise requests.exceptions.RequestException(f"Invalid success value '{data["success"]}")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")

            self.email_warning_label.setText("Server error encountered. Try again later.")
            self.email_warning_label.toggle_text(True)
            self.password_warning_label.setText("Server error encountered. Try again later.")
            self.password_warning_label.toggle_text(True)

            incorrect_input = True

        if incorrect_input:
            return

        self.__flush()
        self.session_credentials_received.emit(session_token, account_type)
        self.navigate_to_home.emit()
        
    def on_sign_up_click(self):
        self.__flush()
        self.navigate_to_sign_up.emit()