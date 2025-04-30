from PyQt6.QtWidgets import QVBoxLayout
from util_widgets import Page, HeaderText, InputLabel, InputField, InputWarningLabel, ActionLabel, PrimaryButton

class SignInPage(Page):
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

        self.forgot_password_label = ActionLabel("Forgot password?")
        self.central_layout.addWidget(self.forgot_password_label)

        # Call-To-Action

        self.sign_in_button = PrimaryButton("Sign In")
        self.central_layout.addWidget(self.sign_in_button)

        self.sign_up_label = ActionLabel("Don't have an account?")
        self.central_layout.addWidget(self.sign_up_label)

        # End Of Layout

        self.central_layout.addStretch()