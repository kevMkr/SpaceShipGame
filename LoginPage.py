import tkinter as tk
from tkinter import ttk,messagebox
import pyodbc

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login Page")
        self.geometry("400x300")  # Increased window size
        self.create_widgets()

    def create_widgets(self):
        # Add a title label
        tk.Label(self, text="Login", font=("Arial", 16, "bold")).pack(pady=10)

        # Username label and entry
        tk.Label(self, text="Username:", font=("Arial", 12)).pack(pady=5)
        self.username_entry = tk.Entry(self, font=("Arial", 12), width=30)
        self.username_entry.pack(pady=5)

        # Password label and entry
        tk.Label(self, text="Password:", font=("Arial", 12)).pack(pady=5)
        self.password_entry = tk.Entry(self, show="*", font=("Arial", 12), width=30)
        self.password_entry.pack(pady=5)

        # Button frame for buttons in the same row
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)

        # Login button
        login_button = tk.Button(button_frame, text="Login", font=("Arial", 12), command=self.login)
        login_button.grid(row=0, column=0, padx=10)

        # Exit button
        exit_button = tk.Button(button_frame, text="Exit", font=("Arial", 12), command=self.exit_app)
        exit_button.grid(row=0, column=1, padx=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == "admin" and password == "password":
            messagebox.showinfo("Login Successful", "Welcome, admin!")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def exit_app(self):
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()