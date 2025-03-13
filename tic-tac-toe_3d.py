# 3D Tic-Tac-Toe using Ursina
from ursina import *

class TicTacToe3D(Entity):
    """3D Tic-Tac-Toe game using Ursina."""

    def __init__(self, size=3):
        """Initialize the game board and UI."""
        super().__init__()
        self.size = size
        self.current_player = 1  # 1 for Player 1 (X), 2 for Player 2 (O)
        self.game_over = False
        self.board = [[[0 for _ in range(size)] for _ in range(size)] for _ in range(size)]
        self.cells = {}  # Maps (i, j, k) to cell entity
        self.markers = []  # Stores all placed markers for reset
        self.scores = {1: 0, 2: 0}  # Score tracking

        self.create_board()
        self.create_ui()

    def create_board(self):
        """Create the 3D grid and clickable cells."""
        offset = Vec3(-1, -1, -1)  # Adjust position to center board
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

    def create_ui(self):
        """Create the UI elements (score and reset instructions)."""
        self.score_text = Text(
            text=f"Player 1: {self.scores[1]} - Player 2: {self.scores[2]}",
            position=(-0.5, 0.45),
            scale=2,
            color=color.white
        )
        self.info_text = Text(
            text="Press 'R' to reset the game",
            position=(-0.5, 0.35),
            scale=1.5,
            color=color.yellow
        )

    def check_winner(self, i, j, k):
        """Dynamically check if the last move creates a winning condition."""
        directions = [
            [(1, 0, 0), (-1, 0, 0)],  # x-axis
            [(0, 1, 0), (0, -1, 0)],  # y-axis
            [(0, 0, 1), (0, 0, -1)],  # z-axis
            [(1, 1, 0), (-1, -1, 0)],  # diagonal in xy-plane
            [(1, -1, 0), (-1, 1, 0)],  # diagonal in xy-plane
            [(1, 0, 1), (-1, 0, -1)],  # diagonal in xz-plane
            [(1, 0, -1), (-1, 0, 1)],  # diagonal in xz-plane
            [(0, 1, 1), (0, -1, -1)],  # diagonal in yz-plane
            [(0, 1, -1), (0, -1, 1)],  # diagonal in yz-plane
            [(1, 1, 1), (-1, -1, -1)],  # 3D diagonal
            [(1, -1, 1), (-1, 1, -1)],  # 3D diagonal
            [(1, 1, -1), (-1, -1, 1)],  # 3D diagonal
            [(1, -1, -1), (-1, 1, 1)]   # 3D diagonal
        ]

        for direction in directions:
            count = 1  # Start with current cell
            cells_to_highlight = [(i, j, k)]

            for dx, dy, dz in direction:
                x, y, z = i, j, k
                while 0 <= (x := x + dx) < self.size and 0 <= (y := y + dy) < self.size and 0 <= (z := z + dz) < self.size:
                    if self.board[x][y][z] == self.current_player:
                        count += 1
                        cells_to_highlight.append((x, y, z))
                    else:
                        break

            if count >= self.size:  # A player wins
                self.highlight_winning_cells(cells_to_highlight)
                return self.current_player

        # Check for draw (if no empty spaces left)
        if all(self.board[i][j][k] != 0 for i in range(self.size) for j in range(self.size) for k in range(self.size)):
            print("It's a draw!")
            self.game_over = True
            return -1  # Indicates a draw

        return 0  # No winner yet

    def draw_marker(self, i, j, k):
        """Place the marker for the current player."""
        pos = self.cells[(i, j, k)].world_position

        if self.current_player == 1:
            marker = Entity(model='cube', color=color.red, scale=(0.7, 0.1, 0.1), position=pos, rotation=Vec3(0,0,45))
            self.markers.append(marker)
            marker2 = Entity(model='cube', color=color.red, scale=(0.7, 0.1, 0.1), position=pos, rotation=Vec3(0,0,-45))
            self.markers.append(marker2)
        else:
            marker = Entity(model='sphere', color=color.blue, scale=0.4, position=pos)
            self.markers.append(marker)

    def highlight_winning_cells(self, cells):
        """Highlight the winning cells in yellow."""
        for cell_pos in cells:
            self.cells[cell_pos].color = color.yellow

    def handle_input(self, key):
        """Handle user input and update the game state."""
        if self.game_over and key == 'r':  # Press 'r' to reset
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
                        winner = self.check_winner(i, j, k)

                        if winner > 0:
                            print(f"Player {winner} wins!")
                            self.scores[winner] += 1
                            self.score_text.text = f"Player 1: {self.scores[1]} - Player 2: {self.scores[2]}"
                            self.game_over = True
                        elif winner == -1:
                            print("It's a draw!")  # Game ends in a draw
                        else:
                            self.current_player = 2 if self.current_player == 1 else 1
                    break

    def reset_game(self):
        """Reset the game board and clear markers."""
        self.current_player = 1
        self.game_over = False
        self.board = [[[0 for _ in range(self.size)] for _ in range(self.size)] for _ in range(self.size)]

        # Reset cell colors
        for cell in self.cells.values():
            cell.color = color.white

        # Remove all markers
        for marker in self.markers:
            destroy(marker)
        self.markers.clear()

# Initialize the game
app = Ursina()
game = TicTacToe3D()
app.run()       
