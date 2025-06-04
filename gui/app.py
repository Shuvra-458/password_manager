import tkinter as tk
from tkinter import ttk, messagebox
from core.vault import load_vault, save_vault
from core.encryption import generate_key, encrypt_data, decrypt_data
from core.generator import generate_password
from datetime import datetime
from cryptography.fernet import Fernet

class PasswordManagerApp(tk.Tk):
    def __init__(self, master_password):
        super().__init__()
        self.title("🔐 Secure Password Manager")
        self.geometry("700x500")
        self.resizable(False, False)

        self.fernet = Fernet(generate_key(master_password))
        self.entries = load_vault()

        self.create_widgets()
        self.refresh_table()

    def create_widgets(self):
        search_frame = ttk.Frame(self)
        search_frame.pack(pady=10)
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self.refresh_table())
        ttk.Entry(search_frame, textvariable=self.search_var, width=30).pack(side=tk.LEFT, padx=5)

        columns = ("site", "username", "password", "last_updated")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=160)
        self.tree.pack(pady=5)

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="➕ Add", command=self.add_entry_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🧪 Audit", command=self.audit_vault).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🔁 Refresh", command=self.refresh_table).pack(side=tk.LEFT, padx=5)

    def refresh_table(self):
        self.tree.delete(*self.tree.get_children())
        query = self.search_var.get().lower()
        for entry in self.entries:
            try:
                decrypted = {
                    k: decrypt_data(entry[k], self.fernet) if k != 'last_updated' else entry[k]
                    for k in ['site', 'username', 'password', 'last_updated']
                }
                if query in decrypted['site'].lower() or query in decrypted['username'].lower():
                    self.tree.insert('', tk.END, values=(decrypted['site'], decrypted['username'],
                                                         decrypted['password'], decrypted['last_updated']))
            except Exception:
                continue

    def add_entry_dialog(self):
        def save():
            site = site_var.get()
            user = user_var.get()
            pwd = pwd_var.get()
            if not site or not user or not pwd:
                messagebox.showerror("Error", "All fields required")
                return
            entry = {
                'site': encrypt_data(site, self.fernet),
                'username': encrypt_data(user, self.fernet),
                'password': encrypt_data(pwd, self.fernet),
                'last_updated': datetime.now().strftime("%Y-%m-%d")
            }
            self.entries.append(entry)
            save_vault(self.entries)
            top.destroy()
            self.refresh_table()

        def generate():
            pwd_var.set(generate_password())

        top = tk.Toplevel(self)
        top.title("Add New Password")
        top.geometry("400x250")

        site_var = tk.StringVar()
        user_var = tk.StringVar()
        pwd_var = tk.StringVar()

        ttk.Label(top, text="Site:").pack()
        ttk.Entry(top, textvariable=site_var).pack(fill='x', padx=10)
        ttk.Label(top, text="Username:").pack()
        ttk.Entry(top, textvariable=user_var).pack(fill='x', padx=10)
        ttk.Label(top, text="Password:").pack()
        ttk.Entry(top, textvariable=pwd_var).pack(fill='x', padx=10)

        ttk.Button(top, text="Generate Password", command=generate).pack(pady=5)
        ttk.Button(top, text="Save", command=save).pack()

    def audit_vault(self):
        used_passwords = {}
        reused = set()
        weak = []

        for entry in self.entries:
            try:
                password = decrypt_data(entry['password'], self.fernet)
                if password in used_passwords:
                    reused.add(password)
                else:
                    used_passwords[password] = 1
                if len(password) < 8 or password.isalpha() or password.isdigit():
                    weak.append(password)
            except Exception:
                continue

        msg = f"🔁 Reused passwords: {len(reused)}\n❗ Weak passwords: {len(weak)}"
        if reused:
            msg += "\nReused Examples:\n" + "\n".join(list(reused)[:3])
        if weak:
            msg += "\nWeak Examples:\n" + "\n".join(list(weak)[:3])
        messagebox.showinfo("Security Audit", msg)