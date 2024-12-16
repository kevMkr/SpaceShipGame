import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
import MainGame as MG

# Establish connection to the database
conn = pyodbc.connect(
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=./CyberSafeDatabase.accdb;'
)
cursor = conn.cursor()

class MainMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CyberSafe")
        self.geometry("1400x600")  # Increase window width to accommodate leaderboard
        self.setup_widgets()
  
    def setup_widgets(self):
        # Main container frame
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill="both", expand=True)

        # Create a frame for the left side of the menu (Game and Settings)
        self.left_frame = tk.Frame(self.main_frame, width=500)
        self.left_frame.pack(side="left", fill="both", expand=True, padx=20)

        # Center buttons in the frame
        self.left_frame.pack_propagate(False)
        button_frame = tk.Frame(self.left_frame)
        button_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Header Label
        header_label = tk.Label(self.left_frame, text="CyberSafe", font=("Arial", 24, "bold"))
        header_label.pack(pady=20)

        # Play Game button
        play_game_button = tk.Button(
            button_frame,
            text="Play Game",
            font=("Arial", 16),
            command=self.play_game,
        )
        play_game_button.pack(pady=20)

        # Guide Button
        guide_button = tk.Button(
            button_frame,
            text="Guide",
            font=("Arial", 16),
            command=self.show_guide_frame,
        )
        guide_button.pack(pady=10)

        # Exit Application Button
        exit_button = tk.Button(
            button_frame,
            text="Exit Application",
            font=("Arial", 16),
            command=self.exit_application,
        )
        exit_button.pack(pady=20)

        # Create a frame for the right side (Leaderboard)
        self.right_frame = tk.Frame(self.main_frame, width=300, height=400)
        self.right_frame.pack(side="right", fill="both", expand=False, padx=20)

        # Leaderboard title
        tk.Label(self.right_frame, text="Leaderboard", font=("Arial", 18, "bold")).pack(pady=20)

        # Table for displaying leaderboard entries
        columns = ("Rank", "Player", "Score")
        self.leaderboard_tree = ttk.Treeview(self.right_frame, columns=columns, show="headings")

        # Define columns headers
        self.leaderboard_tree.heading("Rank", text="Rank")
        self.leaderboard_tree.heading("Player", text="Player")
        self.leaderboard_tree.heading("Score", text="Score")

        self.leaderboard_tree.pack(pady=20, padx=20, fill="both", expand=True)

        # Load leaderboard data from the database
        self.load_leaderboard()

        # Create a guide frame (hidden initially)
        self.guide_frame = tk.Frame(self)

        # Guide header
        tk.Label(self.guide_frame, text="Game Guide", font=("Arial", 24, "bold")).pack(pady=20)

        # Add game instructions
        game_instructions = (
            "Welcome to the game!\n\n"
            "Controls:\n"
            "- Use the arrow keys for movement:\n"
            "  • UP arrow to move up.\n"
            "  • DOWN arrow to move down.\n"
            "  • LEFT arrow to move left.\n"
            "  • RIGHT arrow to move right.\n\n"
            "- Press the 'U' key to activate upgrades.\n\n"
            "Tip: Collect points to increase your score and become the top player on the leaderboard!"
        )
        tk.Label(
            self.guide_frame,
            text=game_instructions,
            font=("Arial", 14),
            justify="left",
            wraplength=600,  # Wrap text for readability
        ).pack(pady=10)

        # Back button to return to the main menu
        tk.Button(
            self.guide_frame,
            text="Back to Main Menu",
            font=("Arial", 16),
            command=self.show_main_menu,
        ).pack(pady=20)

    def load_leaderboard(self):
        try:
            cursor.execute("""
                SELECT TOP 10 Username, Score
                FROM Leaderboard
                ORDER BY Score DESC
            """)
            results = cursor.fetchall() # Fetch all rows from the query result

            # Clear existing data in the treeview
            for item in self.leaderboard_tree.get_children():
                self.leaderboard_tree.delete(item)

            # Insert data into the treeview
            rank = 1
            for row in results:
                # Insert a new row into the treeview with rank, username, and score
                self.leaderboard_tree.insert("", "end", values=(rank, row.Username, row.Score))
                rank += 1
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load leaderboard: {e}")

    def show_main_menu(self):
        """Switches back to the main menu frame."""
        self.guide_frame.pack_forget()  # Hide the guide frame
        self.main_frame.pack(fill="both", expand=True)  # Show the main menu frame

    def show_guide_frame(self):
        """Displays the guide frame."""
        self.main_frame.pack_forget()  # Hide the main menu frame
        self.guide_frame.pack(fill="both", expand=True)  # Show the guide frame

    def play_game(self):
        """Navigate to the Main Game."""
        self.destroy()  # Close the MainMenu window.
        MG.actual_game()  # Call the MainGame function or class from the MG module.

    def exit_application(self):
        """Exits the application."""
        self.quit()

if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()