from django.core.exceptions import ValidationError
import re

def validate_username(username):
    if not username:
        raise ValidationError("Username cannot be empty.")
    if len(username) < 6:
        raise ValidationError("Username must be at least 6 characters.")
    if not re.match("^[a-zA-Z0-9_]+$", username):
        raise ValidationError("Username can only contain letters, numbers, and underscores.")

def validate_password(password):
    if not password:
        raise ValidationError("Password cannot be empty.")
    if len(password) < 6:
        raise ValidationError("Password must be at least 6 characters.")
    if not re.match("^[a-zA-Z0-9_]+$", password):
        raise ValidationError("Password can only contain letters, numbers, and underscores.")

def validate_passwords_match(pass1, pass2):
    if pass1 != pass2:
        raise ValidationError("Passwords do not match.")