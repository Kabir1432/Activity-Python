# utils.py
import secrets
import string


def generate_discount_code(length=10):
    characters = string.ascii_uppercase + string.digits
    code = "".join(secrets.choice(characters) for _ in range(length))
    return code
