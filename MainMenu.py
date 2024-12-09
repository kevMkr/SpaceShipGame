import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
import LoginPage as LP
import MainGame as MG

conn = pyodbc.connect(
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=./CyberSafeDatabase.accdb;'
    )

class MainMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Main Menu")
        self.geometry("900x500")  # Increase window width to accommodate leaderboard
        self.setup_widgets()
  
    def setup_widgets(self):
        # Create a frame for the left side of the menu (Game and Settings)
        left_frame = tk.Frame(self, width=500)
        left_frame.pack(side="left", fill="both", expand=True, padx=20)

        # Header Label
        header_label = tk.Label(left_frame, text="Main Menu", font=("Arial", 24, "bold"))
        header_label.pack(pady=20)

        # Play Game button
        play_game_button = tk.Button(
            left_frame,
            text="Play Game",
            font=("Arial", 16),
            command=self.play_game,  # Placeholder function
        )
        play_game_button.pack(pady=20)

        # Profile Settings Button
        profile_button = tk.Button(
            left_frame,
            text="Profile Settings",
            font=("Arial", 16),
            command=self.open_profile_settings,
        )
        profile_button.pack(pady=10)

        # Guide Button
        guide_button = tk.Button(
            left_frame,
            text="Guide",
            font=("Arial", 16),
            command=self.show_guide,
        )
        guide_button.pack(pady=10)

        # Exit Application Button
        exit_button = tk.Button(
            left_frame,
            text="Exit Application",
            font=("Arial", 16),
            command=self.exit_application,
        )
        exit_button.pack(pady=20)

        # Create a frame for the right side (Leaderboard)
        right_frame = tk.Frame(self, width=300, height=400)
        right_frame.pack(side="right", fill="both", expand=False, padx=20)

        # Leaderboard title
        tk.Label(right_frame, text="Leaderboard", font=("Arial", 18, "bold")).pack(pady=20)

        # Table for displaying leaderboard entries
        columns = ("Rank", "Player", "Score")
        leaderboard_tree = ttk.Treeview(right_frame, columns=columns, show="headings")

        # Define columns headers
        leaderboard_tree.heading("Rank", text="Rank")
        leaderboard_tree.heading("Player", text="Player")
        leaderboard_tree.heading("Score", text="Score")

        # Sample data (can be replaced with actual data from a file or database)
        leaderboard_data = [
            (1, "Player1", 150),
            (2, "Player2", 120),
            (3, "Player3", 100),
            (4, "Player4", 80),
            (5, "Player5", 60),
        ]

        # Insert data into the treeview
        for rank, player, score in leaderboard_data:
            leaderboard_tree.insert("", "end", values=(rank, player, score))

        leaderboard_tree.pack(pady=20, padx=20, fill="both", expand=True)

    def play_game(self):
        """Placeholder for Play Game functionality."""
        messagebox.showinfo("Play Game", "This feature is under construction!")

    def open_profile_settings(self):
        """Placeholder for Profile Settings functionality."""
        messagebox.showinfo("Profile Settings", "Profile Settings are under construction!")

    def show_guide(self):
        """Displays the guide information."""
        messagebox.showinfo("Guide", "This is where the game guide will be displayed.")

    def exit_application(self):
        """Exits the application."""
        self.quit()

if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()
