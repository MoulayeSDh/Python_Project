# 3D Tic-Tac-Toe using Ursina
from ursina import *

class TicTacToe3D:
    def __init__(self):
        """Initialize game variables and create the 3D board."""
        self.current_player = 1  # 1 for Player 1, 2 for Player 2
        self.game_over = False
        self.board = [[[0 for _ in range(3)] for _ in range(3)] for _ in range(3)]
        self.cells = {}  # Mapping (i, j, k) -> cell entity
        self.create_board()
        self.define_winning_lines()

    def create_board(self):
        """Creates the 3D grid and clickable cells."""
        offset = Vec3(-1, -1, -1)
        for i in range(3):
            for j in range(3):
                for k in range(3):
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
        """Defines all possible winning lines in a 3x3x3 grid."""
        self.winning_lines = []

        # Rows along x-axis
        for j in range(3):
            for k in range(3):
                self.winning_lines.append([(0, j, k), (1, j, k), (2, j, k)])
        
        # Rows along y-axis
        for i in range(3):
            for k in range(3):
                self.winning_lines.append([(i, 0, k), (i, 1, k), (i, 2, k)])
        
        # Rows along z-axis
        for i in range(3):
            for j in range(3):
                self.winning_lines.append([(i, j, 0), (i, j, 1), (i, j, 2)])
        
        # Diagonal lines in xy planes
        for k in range(3):
            self.winning_lines.append([(0, 0, k), (1, 1, k), (2, 2, k)])
            self.winning_lines.append([(0, 2, k), (1, 1, k), (2, 0, k)])
        
        # Diagonal lines in xz planes
        for j in range(3):
            self.winning_lines.append([(0, j, 0), (1, j, 1), (2, j, 2)])
            self.winning_lines.append([(0, j, 2), (1, j, 1), (2, j, 0)])
        
        # Diagonal lines in yz planes
        for i in range(3):
            self.winning_lines.append([(i, 0, 0), (i, 1, 1), (i, 2, 2)])
            self.winning_lines.append([(i, 0, 2), (i, 1, 1), (i, 2, 0)])
        
        # 3D diagonal lines
        self.winning_lines.append([(0, 0, 0), (1, 1, 1), (2, 2, 2)])
        self.winning_lines.append([(0, 0, 2), (1, 1, 1), (2, 2, 0)])
        self.winning_lines.append([(0, 2, 0), (1, 1, 1), (2, 0, 2)])
        self.winning_lines.append([(0, 2, 2), (1, 1, 1), (2, 0, 0)])

    def check_winner(self):
        """Checks if a player has won the game."""
        for line in self.winning_lines:
            a, b, c = line
            if self.board[a[0]][a[1]][a[2]] != 0 and \
               self.board[a[0]][a[1]][a[2]] == self.board[b[0]][b[1]][b[2]] == self.board[c[0]][c[1]][c[2]]:
                return self.board[a[0]][a[1]][a[2]]

        # Check for a draw (if no empty spaces left)
        if all(self.board[i][j][k] != 0 for i in range(3) for j in range(3) for k in range(3)):
            print("It's a draw!")
            self.game_over = True
            return -1  # Indicates a draw
        return 0  # No winner yet

    def draw_marker(self, i, j, k):
        """Draws the symbol for the current player at (i, j, k)."""
        pos = self.cells[(i, j, k)].world_position
        if self.current_player == 1:
            Entity(model='cube', color=color.red, scale=(0.7, 0.1, 0.1), position=pos, rotation=Vec3(0,0,45))
            Entity(model='cube', color=color.red, scale=(0.7, 0.1, 0.1), position=pos, rotation=Vec3(0,0,-45))
        else:
            Entity(model='sphere', color=color.blue, scale=0.4, position=pos)

    def handle_input(self, key):
        """Handles user input and updates the game state."""
        if self.game_over:
            return
        if key == 'left mouse down' and mouse.hovered_entity:
            for coord, cell in self.cells.items():
                if cell == mouse.hovered_entity:
                    i, j, k = coord
                    if self.board[i][j][k] == 0:
                        self.board[i][j][k] = self.current_player
                        self.draw_marker(i, j, k)
                        winner = self.check_winner()
                        if winner > 0:
                            print(f"Player {winner} wins!")
                            self.game_over = True
                        elif winner == -1:
                            print("It's a draw!")  # Game ends in a draw
                        else:
                            self.current_player = 2 if self.current_player == 1 else 1
                    break

# Initialize the game
app = Ursina()
game = TicTacToe3D()
app.run()
