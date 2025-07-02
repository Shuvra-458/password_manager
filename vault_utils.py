import os
import json
import hashlib
from datetime import datetime
import random
import string

DATA_DIR = "data"

def get_user_file():
    return os.path.join(DATA_DIR, "users.json")

def get_vault_file(username):
    return os.path.join(DATA_DIR, f"vault_{username}.json")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if not os.path.exists(get_user_file()):
        return {}
    with open(get_user_file(), "r") as f:
        return json.load(f)

def save_users(users):
    with open(get_user_file(), "w") as f:
        json.dump(users, f, indent=4)

def register_user(username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = hash_password(password)
    save_users(users)
    return True

def authenticate_user(username, password):
    users = load_users()
    hashed = hash_password(password)
    return users.get(username) == hashed

def load_vault(username):
    vault_file = get_vault_file(username)
    if not os.path.exists(vault_file):
        return []
    with open(vault_file, "r") as f:
        return json.load(f)

def save_vault(username, vault):
    vault_file = get_vault_file(username)
    with open(vault_file, "w") as f:
        json.dump(vault, f, indent=4)

def generate_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))
