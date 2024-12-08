import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login Page")
        self.geometry("400x300")  # Increased window size
        self.create_widgets()
        self.init_database()  # Initialize the database

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

        # Register button
        register_button = tk.Button(button_frame, text="Register", font=("Arial", 12), command=self.open_registration)
        register_button.grid(row=0, column=1, padx=10)

        # Forgot Password button
        forgot_password_button = tk.Button(button_frame, text="Forgot Password", font=("Arial", 12),
                                           command=self.open_forgot_password)
        forgot_password_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Exit button
        exit_button = tk.Button(button_frame, text="Exit", font=("Arial", 12), command=self.exit_app)
        exit_button.grid(row=2, column=0, columnspan=2, pady=10)

    def init_database(self):
        """Initializes the SQLite3 database and creates the users table if it doesn't exist."""
        self.conn = sqlite3.connect("users.db")  # Database file
        cursor = self.conn.cursor()

        # Create table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            security_answer TEXT NOT NULL
        )
        """)

        # Insert a default admin user if the table is empty
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:  # Check if table is empty
            cursor.execute(
                "INSERT INTO users (username, password, security_answer) VALUES (?, ?, ?)",
                ("admin", "password", "blue"))
            self.conn.commit()

    def login(self):
        """Handles login logic with SQLite3 database."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()

        if user:
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def open_registration(self):
        """Opens the registration window."""
        RegistrationWindow(self)

    def open_forgot_password(self):
        """Opens the forgot password window."""
        ForgotPasswordWindow(self)

    def exit_app(self):
        """Closes the application and database connection."""
        self.conn.close()  # Close database connection
        self.destroy()


class RegistrationWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Register")
        self.geometry("400x250")
        self.parent = parent

        # Username
        tk.Label(self, text="Username:", font=("Arial", 12)).pack(pady=5)
        self.username_entry = tk.Entry(self, font=("Arial", 12), width=30)
        self.username_entry.pack(pady=5)

        # Password
        tk.Label(self, text="Password:", font=("Arial", 12)).pack(pady=5)
        self.password_entry = tk.Entry(self, show="*", font=("Arial", 12), width=30)
        self.password_entry.pack(pady=5)

        # Security question label
        tk.Label(self, text="Security Question: What’s your favourite colour?", font=("Arial", 12)).pack(pady=5)

        # Security answer
        tk.Label(self, text="Answer:", font=("Arial", 12)).pack(pady=5)
        self.security_answer_entry = tk.Entry(self, font=("Arial", 12), width=30)
        self.security_answer_entry.pack(pady=5)

        # Button frame
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)

        # Register button
        register_button = tk.Button(button_frame, text="Register", font=("Arial", 12), command=self.register_user)
        register_button.grid(row=0, column=0, padx=10)

        # Cancel button
        cancel_button = tk.Button(button_frame, text="Cancel", font=("Arial", 12), command=self.destroy)
        cancel_button.grid(row=0, column=1, padx=10)

    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        security_answer = self.security_answer_entry.get()

        if username and password and security_answer:
            try:
                cursor = self.parent.conn.cursor()
                cursor.execute("INSERT INTO users (username, password, security_answer) VALUES (?, ?, ?)",
                               (username, password, security_answer))
                self.parent.conn.commit()
                messagebox.showinfo("Registration Successful", "You have registered successfully!")

                # Close registration window and focus back on login page
                self.destroy()
                self.parent.focus()  # Brings focus back to the main window
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists!")
        else:
            messagebox.showerror("Error", "All fields are required!")


class ForgotPasswordWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Forgot Password")
        self.geometry("400x200")
        self.parent = parent

        # Username
        tk.Label(self, text="Username:", font=("Arial", 12)).pack(pady=5)
        self.username_entry = tk.Entry(self, font=("Arial", 12), width=30)
        self.username_entry.pack(pady=5)

        # Recover button
        tk.Button(self, text="Recover Password", font=("Arial", 12), command=self.recover_password).pack(pady=20)

    def recover_password(self):
        username = self.username_entry.get()

        if username:
            cursor = self.parent.conn.cursor()
            cursor.execute("SELECT security_answer, password FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()

            if user:
                security_answer, password = user
                answer = simpledialog.askstring("Security Question", "What’s your favourite colour?")

                if answer and answer.lower() == security_answer.lower():
                    messagebox.showinfo("Password Recovered", f"Your password is: {password}")
                else:
                    messagebox.showerror("Error", "Incorrect answer to the security question!")
            else:
                messagebox.showerror("Error", "Username not found!")
        else:
            messagebox.showerror("Error", "Please enter your username!")


if __name__ == "__main__":
    app = App()
    app.mainloop()
