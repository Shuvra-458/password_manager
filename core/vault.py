import json
import os
import sys

base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
VAULT_FILE = os.path.join(base_path, "data", "vault.json")

def load_vault():
    if not os.path.exists(VAULT_FILE):
        return []
    with open(VAULT_FILE, 'r') as f:
        return json.load(f)

def save_vault(entries):
    with open(VAULT_FILE, 'w') as f:
        json.dump(entries, f, indent=4)


