import tkinter as tk
import random

class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic-Tac-Toe")

        # Initialize the board and symbols
        self.board = [" "] * 9
        self.player_symbol = "X"
        self.computer_symbol = "O"
        self.game_over = False

        # Create a status label
        self.status_label = tk.Label(self.master, text="Your turn (X)")
        self.status_label.grid(row=0, column=0, columnspan=3, pady=5)

        # Create the 3x3 buttons for the board
        self.buttons = []
        for i in range(9):
            btn = tk.Button(self.master, text=" ", font=("Helvetica", 20), width=5, height=2,
                            command=lambda index=i: self.player_move(index))
            btn.grid(row=(i // 3) + 1, column=i % 3, padx=5, pady=5)
            self.buttons.append(btn)

    def player_move(self, index):
        """
        Handles the player's move if the game isn't over and if the chosen cell is empty.
        """
        if not self.game_over and self.board[index] == " ":
            self.board[index] = self.player_symbol
            self.update_buttons()
            if self.check_win(self.player_symbol):
                self.status_label.config(text="You win! Congratulations!")
                self.game_over = True
                return
            if self.check_draw():
                self.status_label.config(text="It's a draw!")
                self.game_over = True
                return

            self.status_label.config(text="Computer is thinking...")
            self.master.after(500, self.computer_move)  # Wait half a second for effect

    def computer_move(self):
        """
        Basic computer strategy:
        1. Check if the computer can win on this move.
        2. Block the player's winning move if possible.
        3. Otherwise, choose a random empty spot.
        """
        if self.game_over:
            return

        # 1. Check for a winning move
        for i in range(9):
            if self.board[i] == " ":
                self.board[i] = self.computer_symbol
                if self.check_win(self.computer_symbol):
                    self.update_buttons()
                    self.status_label.config(text="Computer wins! Better luck next time.")
                    self.game_over = True
                    return
                else:
                    self.board[i] = " "

        # 2. Block player's winning move
        for i in range(9):
            if self.board[i] == " ":
                self.board[i] = self.player_symbol
                if self.check_win(self.player_symbol):
                    self.board[i] = self.computer_symbol
                    self.update_buttons()
                    if self.check_win(self.computer_symbol):
                        self.status_label.config(text="Computer wins! Better luck next time.")
                        self.game_over = True
                    return
                else:
                    self.board[i] = " "

        # 3. Otherwise, pick a random available cell
        available_moves = [i for i, v in enumerate(self.board) if v == " "]
        if available_moves:
            move = random.choice(available_moves)
            self.board[move] = self.computer_symbol
            self.update_buttons()
            if self.check_win(self.computer_symbol):
                self.status_label.config(text="Computer wins! Better luck next time.")
                self.game_over = True
                return
            if self.check_draw():
                self.status_label.config(text="It's a draw!")
                self.game_over = True
                return

        if not self.game_over:
            self.status_label.config(text="Your turn (X)")

    def check_win(self, symbol):
        """
        Checks if the given symbol (X or O) has won.
        """
        win_positions = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
            (0, 4, 8), (2, 4, 6)             # diagonals
        ]
        for a, b, c in win_positions:
            if self.board[a] == symbol and self.board[b] == symbol and self.board[c] == symbol:
                return True
        return False

    def check_draw(self):
        """
        Returns True if the board is full and there's no winner.
        """
        return " " not in self.board

    def update_buttons(self):
        """
        Update the text of each button to reflect the current board state.
        """
        for i in range(9):
            self.buttons[i].config(text=self.board[i])

def main():
    root = tk.Tk()
    app = TicTacToe(root)
    root.mainloop()

if __name__ == "__main__":
    main()