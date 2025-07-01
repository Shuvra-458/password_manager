import streamlit as st
import json
import os
import random
import string
from datetime import datetime

# Paths
VAULT_FILE = 'vault.json'
MASTER_FILE = 'master.json'

# Utility: Load master password
def load_master_password():
    if not os.path.exists(MASTER_FILE):
        return None  # Means no master password exists yet
    with open(MASTER_FILE, 'r') as f:
        data = json.load(f)
        return data.get('master_password')


# Utility: Load vault data
def load_vault():
    if os.path.exists(VAULT_FILE):
        with open(VAULT_FILE, 'r') as file:
            return json.load(file)
    return []

# Utility: Save vault data
def save_vault(vault_data):
    with open(VAULT_FILE, 'w') as file:
        json.dump(vault_data, file, indent=4)

# Password Generator
def generate_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

# Security Audit
def security_audit(vault_data):
    weak_passwords = []
    for entry in vault_data:
        pwd = entry['password']
        if len(pwd) < 8 or pwd.isalpha() or pwd.isnumeric():
            weak_passwords.append(entry)
    return weak_passwords

# -------------------- Streamlit UI --------------------

st.set_page_config(page_title="🔐 Password Manager", layout="centered")

if 'unlocked' not in st.session_state:
    st.session_state.unlocked = False
master_password = load_master_password()


st.title("🔐 Password Manager")
if master_password is None:
    st.title("🔐 Setup Master Password (First Time Launch)")

    new_master_password = st.text_input("Set a Master Password", type="password")
    confirm_password = st.text_input("Confirm Master Password", type="password")

    if st.button("Save Master Password"):
        if new_master_password and new_master_password == confirm_password:
            with open(MASTER_FILE, 'w') as f:
                json.dump({"master_password": new_master_password}, f, indent=4)
            st.success("Master password set successfully! Please restart the app and login.")
            st.stop()
        else:
            st.error("Passwords do not match or empty.")
    st.stop()

# ✅ Normal Unlock Screen
if not st.session_state.unlocked:
    st.title("🔐 Enter Master Password")
    input_password = st.text_input("Master Password", type="password")
    if st.button("Unlock"):
        if input_password == master_password:
            st.session_state.unlocked = True
            st.success("Vault unlocked!")
        else:
            st.error("Incorrect master password.")
    if not st.session_state.unlocked:
        st.stop()
# Load vault after unlock
vault = load_vault()

# Navigation menu
menu = st.sidebar.selectbox("📋 Menu", ["View Vault", "Add New Password", "Generate Password", "Search", "Security Audit", "Export Vault"])

# View Vault
if menu == "View Vault":
    st.subheader("🔎 Saved Passwords")
    if vault:
        st.dataframe(vault)
    else:
        st.info("Vault is empty.")

# Add New Password
elif menu == "Add New Password":
    st.subheader("➕ Add New Password Entry")
    website = st.text_input("Website / App")
    username = st.text_input("Username / Email")
    password = st.text_input("Password")
    if st.button("Save"):
        new_entry = {
            "website": website,
            "username": username,
            "password": password,
            "date_added": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        vault.append(new_entry)
        save_vault(vault)
        st.success("New password saved!")

# Generate Password
elif menu == "Generate Password":
    st.subheader("🔑 Password Generator")
    length = st.slider("Select password length", 8, 32, 12)
    generated_password = generate_password(length)
    st.code(generated_password)
    if st.button("Copy to Clipboard"):
        st.write("Copy manually from above. (Streamlit can't auto-copy for now)")

# Search & Filter
elif menu == "Search":
    st.subheader("🔍 Search Passwords")
    search_term = st.text_input("Search by Website or Username")
    filtered = [entry for entry in vault if search_term.lower() in entry['website'].lower() or search_term.lower() in entry['username'].lower()]
    if filtered:
        st.dataframe(filtered)
    else:
        st.info("No matching entries found.")

# Security Audit
elif menu == "Security Audit":
    st.subheader("🛡️ Weak Password Check")
    weak = security_audit(vault)
    if weak:
        st.warning(f"Found {len(weak)} weak passwords:")
        st.dataframe(weak)
    else:
        st.success("All passwords meet basic strength criteria.")

# Export Vault
elif menu == "Export Vault":
    st.subheader("📤 Export Vault")
    if st.button("Download as CSV"):
        import pandas as pd
        df = pd.DataFrame(vault)
        st.download_button("Click to Download CSV", df.to_csv(index=False), file_name="vault_export.csv", mime="text/csv")
