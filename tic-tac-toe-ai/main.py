import tkinter as tk
from src.ui_manager import TicTacToeUI


def main():
    # Initialize the main window
    root = tk.Tk()

    # Set the window title
    root.title("Tic-Tac-Toe AI")

    # We remove root.geometry() so the window auto-adjusts
    # to the size of your 3x3 grid buttons.

    # Optional: Prevent the window from being smaller than the grid
    root.minsize(300, 300)

    # Initialize the UI Manager
    # Ensure src/ui_manager.py is using .grid(sticky="nsew")
    # as discussed to prevent layout issues.
    app = TicTacToeUI(root)

    # Start the application
    root.mainloop()


if __name__ == "__main__":
    main()