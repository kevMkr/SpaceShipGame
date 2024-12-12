import tkinter as tk
from tkinter import messagebox, ttk
import pyodbc
import MainMenu as mm

# Establish database connection with error handling
try:
    conn = pyodbc.connect(
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=./CyberSafeDatabase.accdb;'
    )
    cursor = conn.cursor()
except Exception as e:
    messagebox.showerror("Database Error", f"Could not connect to database: {e}")
    exit()

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CyberSafe")
        self.geometry("400x300")
        self.resizable(0, 0)
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

        # Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Login", font=("Arial", 12), command=self.login).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Register", font=("Arial", 12), command=self.open_register_window).grid(row=0, column=1, padx=10)
        tk.Button(button_frame, text="Forgot Password", font=("Arial", 12), command=self.open_forgot_window).grid(row=1, column=0, columnspan=2, pady=10)
        tk.Button(button_frame, text="Exit", font=("Arial", 12), command=self.exit_app).grid(row=2, column=0, columnspan=2, pady=10)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showinfo("Error", "Please enter both username and password.")
            return

        try:
            cursor.execute("SELECT Password FROM LoginUser WHERE Username = ?", username)
            result = cursor.fetchone()
            if result is None:
                messagebox.showinfo("Error", "Username does not exist.")
            elif password == result[0]:  # Check password match
                with open("Session.txt", "w") as f:
                    f.write(username)
                messagebox.showinfo("Success", "Login successful!")
                self.destroy()
                mm.MainMenu()
            else:
                messagebox.showinfo("Error", "Incorrect password.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during login: {e}")

    def open_register_window(self):
        RegisterWindow(self)

    def open_forgot_window(self):
        ForgotPasswordWindow(self)

    def exit_app(self):
        self.destroy()


class RegisterWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Register")
        self.geometry("400x400")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Register", font=("Arial", 16, "bold")).pack(pady=10)

        # Fields for registration
        tk.Label(self, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self, width=30)
        self.username_entry.pack(pady=5)

        tk.Label(self, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*", width=30)
        self.password_entry.pack(pady=5)

        tk.Label(self, text="Re-enter Password:").pack(pady=5)
        self.repassword_entry = tk.Entry(self, show="*", width=30)
        self.repassword_entry.pack(pady=5)

        tk.Label(self, text="Security Question Answer (Favourite Colour):").pack(pady=5)
        self.security_entry = tk.Entry(self, width=30)
        self.security_entry.pack(pady=5)

        tk.Button(self, text="Register", command=self.register).pack(pady=10)
        tk.Button(self, text="Cancel", command=self.destroy).pack(pady=10)

    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        repassword = self.repassword_entry.get().strip()
        security_answer = self.security_entry.get().strip()

        if not username or not password or not security_answer:
            messagebox.showinfo("Error", "All fields are required.")
            return

        if password != repassword:
            messagebox.showinfo("Error", "Passwords do not match.")
            return

        try:
            cursor.execute("INSERT INTO LoginUser(Username, Password, Security) VALUES (?, ?, ?)",
                           username, password, security_answer)
            var2= cursor.execute("SELECT max(UserID) from LoginUser").fetchone()
            cursor.execute("SELECT Username from LoginUser where UserID = ?", var2)
            usernamevar1= cursor.fetchone()
            cursor.execute("INSERT INTO User(UserID,Username) values(?,?)", int(var2[0]), usernamevar1[0])
            conn.commit()
            messagebox.showinfo("Success", "Registration successful!")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during registration: {e}")


class ForgotPasswordWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Forgot Password")
        self.geometry("400x300")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Forgot Password", font=("Arial", 16, "bold")).pack(pady=10)

        tk.Label(self, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self, width=30)
        self.username_entry.pack(pady=5)

        tk.Label(self, text="Answer to Security Question:").pack(pady=5)
        self.security_entry = tk.Entry(self, width=30)
        self.security_entry.pack(pady=5)

        tk.Label(self, text="New Password:").pack(pady=5)
        self.newpassword_entry = tk.Entry(self, show="*", width=30)
        self.newpassword_entry.pack(pady=5)

        tk.Label(self, text="Re-enter New Password:").pack(pady=5)
        self.repassword_entry = tk.Entry(self, show="*", width=30)
        self.repassword_entry.pack(pady=5)

        tk.Button(self, text="Reset Password", command=self.reset_password).pack(pady=10)
        tk.Button(self, text="Cancel", command=self.destroy).pack(pady=10)

    def reset_password(self):
        username = self.username_entry.get().strip()
        security_answer = self.security_entry.get().strip()
        new_password = self.newpassword_entry.get().strip()
        re_password = self.repassword_entry.get().strip()

        if not username or not security_answer or not new_password:
            messagebox.showinfo("Error", "All fields are required.")
            return

        if new_password != re_password:
            messagebox.showinfo("Error", "Passwords do not match.")
            return

        try:
            cursor.execute("SELECT Security FROM LoginUser WHERE Username = ?", username)
            result = cursor.fetchone()  
            if result is None:
                messagebox.showinfo("Error", "Username does not exist.")
            elif result[0] == security_answer:
                cursor.execute("UPDATE LoginUser SET Password = ? WHERE Username = ?", new_password, username)
                conn.commit()
                messagebox.showinfo("Success", "Password reset successful!")
                self.destroy()
            else:
                messagebox.showinfo("Error", "Security answer is incorrect.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during password reset: {e}")

class User():
    def __init__(self):
        session=open("Session.txt","r").read()
        cursor.execute("SELECT UserID from User where Username = ?", session)
        self.UserID = cursor.fetchone()[0]
        self.Username = session


if __name__ == "__main__":
    app = App()
    app.mainloop()
