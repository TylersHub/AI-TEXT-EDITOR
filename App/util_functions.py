import re

# Email Regex: Requires sub-domain, @, and 2+ domain sections (e.g., user@example.co.com)
EMAIL_REGEX = re.compile(r"^[\w\.-]+@([\w-]+\.)+[a-zA-Z]{2,}$")
# Password Regex: Requires 1+ uppercase, 1+ lowercase, 1+ digit, and 8+ characters
PASSWORD_REGEX = re.compile(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$")

def validate_email(email_input_text: str) -> tuple[bool, str]:
    if email_input_text == "" or email_input_text.isspace():
        return (False, "EMPTY")
    elif not EMAIL_REGEX.match(email_input_text):
        return (False, "INVALID")
    else:
        return (True, "")

def validate_password(password_input_text: str) -> tuple[bool, str]:
    if password_input_text == "" or password_input_text.isspace():
        return (False, "EMPTY")
    elif not PASSWORD_REGEX.match(password_input_text):
        return (False, "INVALID")
    else:
        return (True, "")