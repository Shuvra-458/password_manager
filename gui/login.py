import tkinter as tk
from tkinter import ttk, messagebox
from gui.app import PasswordManagerApp
from core.encryption import verify_master_password

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🔑 Unlock Vault")
        self.geometry("300x150")
        self.resizable(False, False)

        self.password_var = tk.StringVar()

        ttk.Label(self, text="Enter Master Password").pack(pady=10)
        ttk.Entry(self, textvariable=self.password_var, show="*").pack(pady=5)
        ttk.Button(self, text="Unlock", command=self.try_login).pack(pady=10)

    def try_login(self):
        pw = self.password_var.get()
        if verify_master_password(pw):
            self.destroy()
            app = PasswordManagerApp(pw)
            app.mainloop()
        else:
            messagebox.showerror("Access Denied", "Incorrect master password!")
