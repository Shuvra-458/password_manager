import sys
import os
import bcrypt
import base64
from cryptography.fernet import Fernet

base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
MASTER_FILE = os.path.join(base_path, "data", "master.json")

def generate_key(master_password):
    return base64.urlsafe_b64encode(bcrypt.kdf(
        password=master_password.encode(),
        salt=b"salty_salt_12345",
        desired_key_bytes=32,
        rounds=100
    ))

def encrypt_data(data, fernet):
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(data, fernet):
    return fernet.decrypt(data.encode()).decode()

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

def save_master_password(password):
    hashed = hash_password(password)
    with open(MASTER_FILE, 'wb') as f:
        f.write(hashed)

def verify_master_password(password):
    import os
    if not os.path.exists(MASTER_FILE):
        save_master_password(password)
        return True
    with open(MASTER_FILE, 'rb') as f:
        hashed = f.read()
    return check_password(password, hashed)
