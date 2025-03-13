# 3D Tic-Tac-Toe using Ursina
from ursina import *

class TicTacToe3D:
    def __init__(self, size=3):
        """Initialize the game with a configurable board size."""
        self.size = size
        self.current_player = 1  # 1 for Player 1, 2 for Player 2
        self.game_over = False
        self.board = [[[0 for _ in range(size)] for _ in range(size)] for _ in range(size)]
        self.cells = {}  # Mapping (i, j, k) -> cell entity
        self.create_board()
        self.define_winning_lines()

    def create_board(self):
        """Creates the 3D grid and clickable cells."""
        offset = Vec3(-1, -1, -1)
        for i in range(self.size):
            for j in range(self.size):
                for k in range(self.size):
                    pos = Vec3(i, j, k) + offset
                    cell = Button(
                        parent=scene,
                        model='cube',
                        color=color.white,
                        position=pos,
                        scale=0.9,
                        highlight_color=color.lime,
                        pressed_color=color.azure
                    )
                    self.cells[(i, j, k)] = cell

    def define_winning_lines(self):
        """Defines all possible winning lines in the NxNxN grid."""
        self.winning_lines = []

        # Rows along x-axis
        for j in range(self.size):
            for k in range(self.size):
                self.winning_lines.append([(i, j, k) for i in range(self.size)])

        # Rows along y-axis
        for i in range(self.size):
            for k in range(self.size):
                self.winning_lines.append([(i, j, k) for j in range(self.size)])

        # Rows along z-axis
        for i in range(self.size):
            for j in range(self.size):
                self.winning_lines.append([(i, j, k) for k in range(self.size)])

        # Diagonal lines in xy planes
        for k in range(self.size):
            self.winning_lines.append([(i, i, k) for i in range(self.size)])
            self.winning_lines.append([(i, self.size - 1 - i, k) for i in range(self.size)])

        # Diagonal lines in xz planes
        for j in range(self.size):
            self.winning_lines.append([(i, j, i) for i in range(self.size)])
            self.winning_lines.append([(i, j, self.size - 1 - i) for i in range(self.size)])

        # Diagonal lines in yz planes
        for i in range(self.size):
            self.winning_lines.append([(i, i, i) for i in range(self.size)])
            self.winning_lines.append([(i, i, self.size - 1 - i) for i in range(self.size)])

        # 3D diagonal lines
        self.winning_lines.append([(i, i, i) for i in range(self.size)])
        self.winning_lines.append([(i, i, self.size - 1 - i) for i in range(self.size)])
        self.winning_lines.append([(i, self.size - 1 - i, i) for i in range(self.size)])
        self.winning_lines.append([(i, self.size - 1 - i, self.size - 1 - i) for i in range(self.size)])

    def check_winner_optimized(self, i, j, k):
        """Optimized check for a winner by verifying only affected lines."""
        for line in self.winning_lines:
            if (i, j, k) in line:
                if all(self.board[x][y][z] == self.current_player for x, y, z in line):
                    return self.current_player

        # Check for a draw (if no empty spaces left)
        if all(self.board[i][j][k] != 0 for i in range(self.size) for j in range(self.size) for k in range(self.size)):
            print("It's a draw!")
            self.game_over = True
            return -1  # Indicates a draw
        return 0  # No winner yet

    def draw_marker(self, i, j, k):
        """Draws the marker for the current player at (i, j, k)."""
        pos = self.cells[(i, j, k)].world_position
        if self.current_player == 1:
            Entity(model='cube', color=color.red, scale=(0.7, 0.1, 0.1), position=pos, rotation=Vec3(0,0,45))
            Entity(model='cube', color=color.red, scale=(0.7, 0.1, 0.1), position=pos, rotation=Vec3(0,0,-45))
        else:
            Entity(model='sphere', color=color.blue, scale=0.4, position=pos)

    def highlight_winning_cells(self, winner):
        """Highlights the cells in the winning line."""
        for line in self.winning_lines:
            if all(self.board[x][y][z] == winner for x, y, z in line):
                for cell_pos in line:
                    self.cells[cell_pos].color = color.yellow  # Highlight the winning line

    def handle_input(self, key):
        """Handles user input and updates the game state."""
        if self.game_over and key == 'r':  # Press 'r' to reset the game
            self.reset_game()
            return

        if self.game_over:
            return

        if key == 'left mouse down' and mouse.hovered_entity:
            for coord, cell in self.cells.items():
                if cell == mouse.hovered_entity:
                    i, j, k = coord
                    if self.board[i][j][k] == 0:
                        self.board[i][j][k] = self.current_player
                        self.draw_marker(i, j, k)
                        winner = self.check_winner_optimized(i, j, k)

                        if winner > 0:
                            print(f"Player {winner} wins!")
                            self.highlight_winning_cells(winner)
                            self.game_over = True
                        elif winner == -1:
                            print("It's a draw!")  # Game ends in a draw
                        else:
                            self.current_player = 2 if self.current_player == 1 else 1
                    break

    def reset_game(self):
        """Resets the game for a new round."""
        self.current_player = 1
        self.game_over = False
        self.board = [[[0 for _ in range(self.size)] for _ in range(self.size)] for _ in range(self.size)]

        # Reset cell colors
        for cell in self.cells.values():
            cell.color = color.white

# Initialize the game
app = Ursina()
game = TicTacToe3D()
app.run()
