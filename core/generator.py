# --- core/generator.py ---
import string
import random

def generate_password(length=16, use_specials=True):
    chars = string.ascii_letters + string.digits
    if use_specials:
        chars += "!@#$%^&*()"
    return ''.join(random.choice(chars) for _ in range(length))
