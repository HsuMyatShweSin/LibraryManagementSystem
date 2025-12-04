import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import pickle
import os
from library_management import *
from typing import Optional

from member import Member 

class AccountManager:
    DATA_FILE = "accounts.pkl"

    def __init__(self):
        self.accounts = {}
        self.library = LibraryManager()
        self.load_accounts()

    def load_accounts(self):
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, "rb") as f:
                    self.accounts = pickle.load(f)
            except:
                self.accounts = {}
        else:
            self.accounts = {
                "admin": {"password": "admin123", "role": "admin"}
            }
            self.save_accounts()

    def save_accounts(self):
        with open(self.DATA_FILE, "wb") as f:
            pickle.dump(self.accounts, f)

    def login(self, username, password) -> tuple[bool, Optional[str]]:
        user = self.accounts.get(username)
        if user and user["password"] == password:
            return True, user["role"]
        return False, None

    def signup(self, username, password, role, email="", phone=""):
        if username in self.accounts:
            return False, "Username already exists."
        
        self.accounts[username] = {"password": password, "role": role}
        
        if role == "user":
            member_id = self.library.get_next_member_id()
            
            new_member = Member(member_id=member_id, name=username, email=email, phone=phone)
            
            if self.library.find_member(member_id) is None:
                 if self.library.add_member(new_member):
                    pass
                 else:
                    return False, "Account created, but failed to register as member."
            else:
                 return False, f"Generated Member ID {member_id} already exists."
        
        self.save_accounts()
        return True, "Account created successfully."

class LoginSignupPage(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Library System - Login / Signup")
        self.geometry("400x520") 

        self.manager = AccountManager()

        self.tab_frame = ctk.CTkTabview(self, width=380, height=490)
        self.tab_frame.pack(padx=10, pady=10, fill="both", expand=True)
        self.tab_frame.add("Login")
        self.tab_frame.add("Sign Up")

        self.create_login_tab()
        self.create_signup_tab()

    def create_login_tab(self):
        tab = self.tab_frame.tab("Login")

        tk.Label(tab, text="Username:").pack(pady=(20,5), anchor="w", padx=20)
        self.login_user = ctk.CTkEntry(tab)
        self.login_user.pack(pady=5, padx=20, fill="x")

        tk.Label(tab, text="Password:").pack(pady=(10,5), anchor="w", padx=20)
        self.login_pass = ctk.CTkEntry(tab, show="*")
        self.login_pass.pack(pady=5, padx=20, fill="x")

        
        login_btn = ctk.CTkButton(tab, text="Login", command=self.login_action)
        login_btn.pack(pady=20)

    def login_action(self):
        username = self.login_user.get().strip()
        password = self.login_pass.get().strip()

        if not username or not password:
            messagebox.showwarning("Missing Fields", "Enter username and password.")
            return

        ok, user_role = self.manager.login(username, password)
        
        if ok:
            messagebox.showinfo("Success", f"Logged in as {user_role}.")
            self.destroy()
            app = LibraryApp(user_role, username) 
            app.mainloop()
        else:
            messagebox.showerror("Failed", "Invalid credentials.")

    def create_signup_tab(self):
        tab = self.tab_frame.tab("Sign Up")

        tk.Label(tab, text="Choose Username:").pack(pady=(10,5), anchor="w", padx=20)
        self.signup_user = ctk.CTkEntry(tab)
        self.signup_user.pack(pady=5, padx=20, fill="x")

        tk.Label(tab, text="Choose Password:").pack(pady=(5,5), anchor="w", padx=20)
        self.signup_pass = ctk.CTkEntry(tab, show="*")
        self.signup_pass.pack(pady=5, padx=20, fill="x")

        tk.Label(tab, text="Email (Required for User):").pack(pady=(5,5), anchor="w", padx=20)
        self.signup_email = ctk.CTkEntry(tab)
        self.signup_email.pack(pady=5, padx=20, fill="x")

        tk.Label(tab, text="Phone (Required for User):").pack(pady=(5,5), anchor="w", padx=20)
        self.signup_phone = ctk.CTkEntry(tab)
        self.signup_phone.pack(pady=5, padx=20, fill="x")
        
        tk.Label(tab, text="Role:").pack(pady=(5,5), anchor="w", padx=20)
        self.role_var = tk.StringVar(value="user")
        tk.Radiobutton(tab, text="User", variable=self.role_var, value="user").pack(anchor="w", padx=40)
        tk.Radiobutton(tab, text="Admin", variable=self.role_var, value="admin").pack(anchor="w", padx=40)

        signup_btn = ctk.CTkButton(tab, text="Sign Up", command=self.signup_action)
        signup_btn.pack(pady=20)

    def signup_action(self):
        username = self.signup_user.get().strip()
        password = self.signup_pass.get().strip()
        email = self.signup_email.get().strip()
        phone = self.signup_phone.get().strip()
        role = self.role_var.get()

        if not username or not password:
            messagebox.showwarning("Missing Fields", "Enter username and password.")
            return

        if role == "user" and (not email or not phone):
            messagebox.showwarning("Missing Fields", "User signups require Email and Phone Number.")
            return

        ok, msg = self.manager.signup(username, password, role, email, phone)
        if ok:
            messagebox.showinfo("Success", msg)
            self.tab_frame.set("Login")
            self.login_user.delete(0, tk.END)
            self.login_pass.delete(0, tk.END)
            self.login_user.insert(0, username)
            self.login_pass.insert(0, password)
        else:
            messagebox.showerror("Error", msg)


if __name__ == "__main__":
    login = LoginSignupPage()
    login.mainloop()