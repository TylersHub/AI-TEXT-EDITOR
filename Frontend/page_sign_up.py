from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtCore import pyqtSignal
from util_widgets import Page, HeaderText, InputLabel, InputField, InputWarningLabel, ActionLabel, PrimaryButton
from util_functions import validate_name, validate_email, validate_password

import requests

class SignUpPage(Page):
    navigate_to_sign_in = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.central_layout = QVBoxLayout(self)
        self.central_layout.addStretch()

        # Header Section

        self.sign_in_header = HeaderText("Enter HungryText")
        self.central_layout.addWidget(self.sign_in_header)

        # First Name Section

        self.fname_label = InputLabel("First Name")
        self.central_layout.addWidget(self.fname_label)

        self.fname_input = InputField()
        self.central_layout.addWidget(self.fname_input)

        self.fname_warning_label = InputWarningLabel("Invalid name")
        self.central_layout.addWidget(self.fname_warning_label)

        # Last Name Section

        self.lname_label = InputLabel("Last Name")
        self.central_layout.addWidget(self.lname_label)

        self.lname_input = InputField()
        self.central_layout.addWidget(self.lname_input)

        self.lname_warning_label = InputWarningLabel("Invalid name")
        self.central_layout.addWidget(self.lname_warning_label)

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

        # Call-To-Action

        self.sign_up_button = PrimaryButton("Sign Up")
        self.sign_up_button.clicked.connect(self.on_sign_up_click)
        self.central_layout.addWidget(self.sign_up_button)

        self.sign_in_label = ActionLabel("Already have an account?")
        self.sign_in_label.clicked.connect(self.on_sign_in_click)
        self.central_layout.addWidget(self.sign_in_label)

        # Form Submission Shortcuts

        self.fname_input.returnPressed.connect(self.sign_up_button.click)
        self.lname_input.returnPressed.connect(self.sign_up_button.click)
        self.email_input.returnPressed.connect(self.sign_up_button.click)
        self.password_input.returnPressed.connect(self.sign_up_button.click)

        # End Of Layout

        self.central_layout.addStretch()

    def __flush(self):
        for input_field in self.findChildren(InputField):
            input_field.clear()

        for input_warning_label in self.findChildren(InputWarningLabel):
            input_warning_label.toggle_text(False)

    def on_sign_up_click(self):
        fname_input_text = self.fname_input.text()
        lname_input_text = self.lname_input.text()
        email_input_text = self.email_input.text()
        password_input_text = self.password_input.text()
        invalid_input = False
        incorrect_input = False

        # First Name Input Validation

        is_fname_input_valid, invalid_fname_input_error = validate_name(fname_input_text)

        if is_fname_input_valid == False:
            if invalid_fname_input_error == "EMPTY":
                self.fname_warning_label.setText("Please enter a name")
            elif invalid_fname_input_error == "INVALID":
                self.fname_warning_label.setText("Please enter a valid name")

            self.fname_warning_label.toggle_text(True)
            invalid_input = True
        else:
            self.fname_warning_label.toggle_text(False)

        # Last Name Input Validation

        is_lname_input_valid, invalid_lname_input_error = validate_name(lname_input_text)

        is_lname_input_valid, invalid_lname_input_error = validate_name(lname_input_text)

        if is_lname_input_valid == False:
            if invalid_lname_input_error == "EMPTY":
                self.lname_warning_label.setText("Please enter a name")
            elif invalid_lname_input_error == "INVALID":
                self.lname_warning_label.setText("Please enter a valid name")

            self.lname_warning_label.toggle_text(True)
            invalid_input = True
        else:
            self.lname_warning_label.toggle_text(False)

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
            sign_up_data = {"first_name": fname_input_text, "last_name": lname_input_text, "email": email_input_text.lower(), "password": password_input_text}
            headers = {"Content-Type": "application/json"}

            response = requests.post("http://127.0.0.1:5000/auth/signup", json=sign_up_data, headers=headers)

            if response.status_code not in (200, 401):
                response.raise_for_status()

            data = response.json()

            if data["success"] == False:
                if data["error"] == "Account already exists":
                    self.email_warning_label.setText("This email is already registered")
                else:
                    raise requests.exceptions.RequestException(f"Invalid failure message '{data['error']}'")
                    
                self.email_warning_label.toggle_text(True)
                incorrect_input = True
            elif data["success"] != True:
                raise requests.exceptions.RequestException(f"Invalid success value '{data['success']}'")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")

            self.fname_warning_label.setText("Server error encountered. Try again later.")
            self.fname_warning_label.toggle_text(True)
            self.lname_warning_label.setText("Server error encountered. Try again later.")
            self.lname_warning_label.toggle_text(True)
            self.email_warning_label.setText("Server error encountered. Try again later.")
            self.email_warning_label.toggle_text(True)
            self.password_warning_label.setText("Server error encountered. Try again later.")
            self.password_warning_label.toggle_text(True)

            incorrect_input = True

        if incorrect_input:
            return

        self.__flush()
        self.navigate_to_sign_in.emit()

    def on_sign_in_click(self):
        self.__flush()
        self.navigate_to_sign_in.emit()