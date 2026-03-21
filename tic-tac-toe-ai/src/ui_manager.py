import tkinter as tk
from tkinter import messagebox
from src.game_logic import TicTacToeLogic
from src.ai_engine import TicTacToeAI


class TicTacToeUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe AI")
        self.logic = TicTacToeLogic()
        self.ai = TicTacToeAI()
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_widgets()

    def create_widgets(self):
        # Configure the grid to be responsive
        for i in range(3):
            self.root.grid_rowconfigure(i, weight=1)
            self.root.grid_columnconfigure(i, weight=1)

        for r in range(3):
            for c in range(3):
                self.buttons[r][c] = tk.Button(
                    self.root,
                    text=' ',
                    font=('Arial', 40, 'bold'),
                    width=5,
                    height=2,
                    command=lambda r=r, c=c: self.on_click(r, c)
                )
                # 'sticky="nsew"' ensures the button fills the entire grid cell
                self.buttons[r][c].grid(row=r, column=c, sticky="nsew", padx=2, pady=2)

    def on_click(self, r, c):
        # Human Move
        if self.logic.board[r][c] == ' ' and not self.logic.check_winner():
            self.update_cell(r, c, self.logic.current_player)
            self.logic.make_move(r, c)

            winner = self.logic.check_winner()
            if winner:
                self.end_game(winner)
            else:
                # Disable buttons during AI "thinking" time
                self.toggle_buttons(state="disabled")
                # Let AI move after a 500ms delay for better feel
                self.root.after(500, self.ai_move)

    def ai_move(self):
        move = self.ai.get_best_move(self.logic)
        if move:
            r, c = move
            self.update_cell(r, c, self.logic.current_player)
            self.logic.make_move(r, c)

            winner = self.logic.check_winner()
            if winner:
                self.end_game(winner)
            else:
                self.toggle_buttons(state="normal")

    def update_cell(self, r, c, player):
        color = "#3498db" if player == 'X' else "#e74c3c"
        self.buttons[r][c].config(text=player, fg=color)

    def toggle_buttons(self, state):
        for r in range(3):
            for c in range(3):
                if self.logic.board[r][c] == ' ':
                    self.buttons[r][c].config(state=state)

    def end_game(self, winner):
        if winner == 'Tie':
            msg = "It's a Draw!"
        else:
            msg = f"Player {winner} Wins!"

        messagebox.showinfo("Game Over", msg)
        self.reset_game()

    def reset_game(self):
        # Clear logic and UI for a new round
        self.logic = TicTacToeLogic()
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].config(text=' ', state="normal")
