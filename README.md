# 🔐 Multi-User Password Manager - Streamlit App

This is a **multi-user password manager** built with **Python** and **Streamlit**, allowing each user to **register**, **login**, and manage their own **private password vault** securely.

---

## ✅ Features

- 🧑‍💻 **User Registration & Login (Multi-User Support)**
- 🔑 **Per-user Master Password (Hashed for security)**
- 📂 **Each user has their own vault file (`vault_<username>.json`)**
- ➕ **Add New Passwords**
- 👁️ **Show/Hide Passwords with dot masking and toggle**
- 🔍 **Search by website or username**
- 🗑️ **Delete Password Entries**
- 🛡️ **Security Audit (Detect Weak Passwords)**
- 🎲 **Password Generator**
- 🚪 **Logout with full session clearing**
- ☁️ **Streamlit Cloud Ready for Deployment**

---

## ✅ Installation & Running Locally

1. **Clone the repository:**

```bash
git clone https://github.com/Shuvra-458/password_manager.git
cd password_manager
```
2. **Create a virtual environment (optional but recommended):**
```bash
python -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)
```
3. **Install dependencies:**
```bash
pip install -r requirements.txt
```
4. **Run the App**
```bash
streamlit run web_app.py
```

