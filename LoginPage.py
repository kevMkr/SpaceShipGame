import tkinter as tk
from tkinter import messagebox, ttk
import pyodbc
import MainMenu as mm

conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ= ./CyberSafeDatabase.accdb;')
cursor = conn.cursor()

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CyberSafe")
        self.geometry("400x300") 
        self.resizable(0,0) # Increased window size
        self.create_widgets() 

    def create_widgets(self):
        def mainmenuwindow():
            cursor.execute('select Password from Logins where Username = ?', self.username_entry.get)
            passwordtemp=cursor.fetchone()
            if passwordtemp == None:
                messagebox.showinfo("Message","Username doesn't exist")
            elif self.password_entry.get() == str(passwordtemp).strip("(),'"):
                f = open("Session.txt","w")
                f.write(self.username_entry.get())
                f.close()
                self.destroy()
                mm.mainmenu()
            else:
                messagebox.showinfo("Message","Wrong password")

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

    def registerwindow(self):
        def createlogin():
            if passwordvar.get() == passwordreentryvar.get():
                cursor.execute('insert into Logins(Username,Password,Security) values (?,?,?)',
                                usernamevar.get(),passwordvar.get(), answervar.get())
                var2= cursor.execute('select max(UserID) from Logins').fetchone()
                cursor.execute('select Username from Logins where UserID= ?', var2)
                usernamevar1= cursor.fetchone()
                cursor.execute('insert into User(UserID,Username) values(?,?)',int(var2[0]), usernamevar1[0])
                conn.commit()
                messagebox.showinfo("Message", "Saved!")
                registerframe.destroy()
            else:
                messagebox.showinfo("Message","Password is no match")

            registerframe=tk.Frame(self)
            registerframe.grid(row=0,column=0,columnspan=2,rowspan=5,sticky="NEWS")
            registerframe.rowconfigure((0,1,2,3,4,5,6),weight=1)
            registerframe.columnconfigure(0,weight=2)
            registerframe.columnconfigure(1,weight=3)
            tk.Label(registerframe,text="Create new account").grid(row=0,column=0,columnspan=2,sticky="NW",padx=5,pady=5)
            tk.Label(registerframe, text="Username").grid(row=1, column=0, columnspan=2, sticky="NWS", padx=5,
                                                            pady=5)
            tk.Label(registerframe, text="Password").grid(row=2, column=0, columnspan=2, sticky="NWS", padx=5,
                                                            pady=5)
            tk.Label(registerframe, text="Re-enter password").grid(row=3, column=0, columnspan=2, sticky="NWS", padx=5,
                                                                    pady=5)
            tk.Label(registerframe, text="Security").grid(row=4, column=0, columnspan=2, sticky="NWS", padx=5,
                                                            pady=5)
            tk.Label(registerframe, text="Answer").grid(row=5, column=0, columnspan=2, sticky="NWS", padx=5,
                                                        pady=5)
            tk.Label(registerframe, text="What is your favourite colour?").grid(row=4,column=1,columnspan=2,sticky="NWS",
                                                                                padx=5, pady=5)

            usernamevar=tk.StringVar()
            username_entry = ttk.Entry(registerframe,textvariable=usernamevar)
            username_entry.grid(column=1, row=1, sticky="EW", padx=5, pady=5)
            passwordvar=tk.StringVar()
            passwordcreate_entry = ttk.Entry(registerframe,show="*",textvariable=passwordvar)
            passwordcreate_entry.grid(column=1, row=2, sticky="EW", padx=5, pady=5)
            passwordreentryvar=tk.StringVar()
            passwordreentry_entry = ttk.Entry(registerframe,show="*",textvariable=passwordreentryvar)
            passwordreentry_entry.grid(column=1, row=3, sticky="EW", padx=5, pady=5)
            answervar=tk.StringVar()
            answer_entry = ttk.Entry(registerframe,textvariable=answervar)
            answer_entry.grid(column=1, row=5, sticky="EW", padx=5, pady=5)

            ttk.Button(registerframe,text="Cancel",command=lambda :registerframe.destroy()).grid(column=1,row=6,sticky="NEWS",pady=5,padx=5)
            ttk.Button(registerframe, text="Create", command=createlogin).grid(
                column=0, row=6, sticky="NEWS", pady=5, padx=5)

        def forgotwindow(self):
            def changepass():
                cursor.execute('select Security from Logins where Username = ?',username_entry.get())
                answertemp=cursor.fetchone()
                if answertemp == None:
                    messagebox.showinfo("message","Username doesn't exist")
                elif answer_entry.get() == answertemp[0]:
                    cursor.execute('update Logins set Password = ? where Username = ?', (newpassword_entry.get(),username_entry.get()))
                    conn.commit()
                    forgotframe.destroy()
                    messagebox.showinfo("Message","Password changed!")
                else:
                    messagebox.showinfo("Message","Color no match")

            forgotframe= tk.Frame(self)
            forgotframe.grid(row=0, column=0, rowspan=5, columnspan=2, sticky="NEWS")
            forgotframe.rowconfigure((0,1,2,3,4,5), weight=1)
            forgotframe.columnconfigure(0, weight=2)
            forgotframe.columnconfigure(1, weight=3)
            tk.Label(forgotframe, text="Forgot Password").grid(row=0, column= 0, columnspan=2,sticky ="NW",padx=5, pady=5)
            tk.Label(forgotframe, text="Username").grid(row=1, column=0, columnspan=2, sticky="NWS", padx=5,
                                                        pady=5)
            tk.Label(forgotframe, text="Security").grid(row=2, column=0, columnspan=2, sticky="NWS", padx=5,
                                                        pady=5)
            tk.Label(forgotframe, text="Question").grid(row=2, column=1, columnspan=2, sticky="NWS", padx=5,
                                                        pady=5)
            tk.Label(forgotframe, text="Answer").grid(row=3, column=0, columnspan=2, sticky="NWS", padx=5,
                                                      pady=5)
            tk.Label(forgotframe, text="New Password").grid(row=4, column=0, columnspan=2, sticky="NWS", padx=5,
                                                            pady=5)
            tk.Label(forgotframe, text="Re-Enter Password").grid(row=5, column=0, columnspan=2, sticky="NWS", padx=5,
                                                                 pady=5)
            usernamevar=tk.StringVar()
            username_entry = ttk.Entry(forgotframe)
            username_entry.grid(column=1, row=1, sticky="EW",padx=5, pady=5)
            answervar=tk.StringVar()
            answer_entry = ttk.Entry(forgotframe)
            answer_entry.grid(column=1, row=3, sticky="EW", padx=5, pady=5)
            newpassword_entry = ttk.Entry(forgotframe)
            newpassword_entry.grid(column=1, row=4, sticky="EW", padx=5, pady=5)
            repassword_entry = ttk.Entry(forgotframe)
            repassword_entry.grid(column=1, row=5, sticky="EW", padx=5, pady=5)

            cancelbutton = ttk.Button(forgotframe, text="Cancel", command=lambda: forgotframe.destroy()).grid(
                column=1, row=6, sticky="NEWS", pady=4, padx=4)
            forgotbutton = ttk.Button(forgotframe, text="Change", command=changepass).grid(
                column=0, row=6, sticky="NEWS", pady=4, padx=4)

class User():
    def __init__(self):
        session=open("Session.txt","r").read()
        cursor.execute('select UserID from User where Username=?', session)
        self.UserID = cursor.fetchone()[0]
        self.Username = session

if __name__ == "__main__":
    app = App()
    app.mainloop()
