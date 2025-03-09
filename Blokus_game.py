import pygame
import sys
import random

# Initialisation de pygame
pygame.init()

# Définition des couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

# Définition des dimensions
CELL_SIZE = 30
GRID_SIZE = 12
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700  # Augmenter la hauteur pour inclure les boutons

# Définition des formes de pièces
PIECES = {
    'blue': [
        [(0, 0)], [(0, 0), (1, 0)], [(0, 0), (1, 0), (2, 0)], [(0, 0), (1, 0), (2, 0), (0, 1)], [(0, 0), (1, 0), (1, 1)],
        [(0, 0), (1, 0), (2, 0), (3, 0)], [(0, 0), (0, 1)], [(0, 0), (1, 0), (2, 0), (2, 1)], [(0, 0), (1, 0), (0, 1), (1, 1)],
        [(0, 0), (1, 0), (1, 1), (2, 1)], [(0, 0), (1, 0), (1, 1), (2, 0)]
    ],
    'red': [
        [(0, 0)], [(0, 0), (1, 0)], [(0, 0), (1, 0), (2, 0)], [(0, 0), (1, 0), (2, 0), (0, 1)], [(0, 0), (1, 0), (1, 1)],
        [(0, 0), (1, 0), (2, 0), (3, 0)], [(0, 0), (0, 1)], [(0, 0), (1, 0), (2, 0), (2, 1)], [(0, 0), (1, 0), (0, 1), (1, 1)],
        [(0, 0), (1, 0), (1, 1), (2, 1)], [(0, 0), (1, 0), (1, 1), (2, 0)]
    ]
}

# Classe pour gérer le plateau de jeu
class Board:
    def __init__(self):
        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    def draw(self, surface):
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                rect = pygame.Rect(x * CELL_SIZE + 200, y * CELL_SIZE + 100, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(surface, WHITE, rect)
                pygame.draw.rect(surface, BLACK, rect, 1)

    def place_piece(self, piece, color, x, y):
        for cell in piece:
            cx, cy = cell
            self.grid[cy + y][cx + x] = color

    def is_valid_position(self, piece, x, y):
        for cell in piece:
            cx, cy = cell
            if not (0 <= cx + x < GRID_SIZE and 0 <= cy + y < GRID_SIZE):
                return False
            if self.grid[cy + y][cx + x] is not None:
                return False
        return True

# Classe pour gérer le jeu Blokus
class BlokusGame:
    def __init__(self, screen, ai_enabled=False):
        self.screen = screen
        self.board = Board()
        self.turn = 'blue'
        self.selected_piece = None
        self.selected_pos = None
        self.piece_dragging = False
        self.piece_rects = {'blue': [], 'red': []}
        self.create_piece_rects()
        self.scores = {'blue': 0, 'red': 0}
        self.ai_enabled = ai_enabled

    def create_piece_rects(self):
        for color in PIECES:
            for i, piece in enumerate(PIECES[color]):
                rect = pygame.Rect(30 if color == 'blue' else SCREEN_WIDTH - 100, 50 + i * 40, 100, 30)
                self.piece_rects[color].append((rect, piece))

    def draw(self):
        self.screen.fill(BLACK)
        self.board.draw(self.screen)
        self.draw_pieces()
        self.draw_scores()
        self.draw_buttons()

    def draw_pieces(self):
        for color in self.piece_rects:
            for rect, piece in self.piece_rects[color]:
                for cell in piece:
                    cx, cy = cell
                    cell_rect = pygame.Rect(rect.x + cx * 20, rect.y + cy * 20, 20, 20)
                    pygame.draw.rect(self.screen, BLUE if color == 'blue' else RED, cell_rect)

        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                color = self.board.grid[y][x]
                if color is not None:
                    rect = pygame.Rect(x * CELL_SIZE + 200, y * CELL_SIZE + 100, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(self.screen, color, rect)

    def draw_scores(self):
        font = pygame.font.Font(None, 36)
        blue_score_text = font.render(f"Player 1 Score: {self.scores['blue']}", True, BLUE)
        red_score_text = font.render(f"Player 2 Score: {self.scores['red']}", True, RED)
        self.screen.blit(blue_score_text, (50, 20))
        self.screen.blit(red_score_text, (SCREEN_WIDTH - 250, 20))

    def draw_buttons(self):
        font = pygame.font.Font(None, 36)
        self.play_ai_button = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 80, 200, 50)
        self.quit_button = pygame.Rect(SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT - 80, 100, 50)

        pygame.draw.rect(self.screen, GRAY, self.play_ai_button)
        pygame.draw.rect(self.screen, GRAY, self.quit_button)

        play_ai_text = font.render("Jouer contre IA", True, BLACK)
        quit_text = font.render("Quitter", True, BLACK)

        self.screen.blit(play_ai_text, (self.play_ai_button.x + 10, self.play_ai_button.y + 10))
        self.screen.blit(quit_text, (self.quit_button.x + 10, self.quit_button.y + 10))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for rect, piece in self.piece_rects[self.turn]:
                if rect.collidepoint(event.pos):
                    self.selected_piece = piece
                    self.selected_pos = (event.pos[0] // CELL_SIZE, event.pos[1] // CELL_SIZE)
                    self.piece_dragging = True
                    break

            if self.play_ai_button.collidepoint(event.pos):
                self.ai_enabled = True
            if self.quit_button.collidepoint(event.pos):
                pygame.quit()
                sys.exit()

        elif event.type == pygame.MOUSEBUTTONUP and self.piece_dragging:
            x, y = self.selected_pos
            if self.board.is_valid_position(self.selected_piece, x - 6, y - 3):
                self.board.place_piece(self.selected_piece, BLUE if self.turn == 'blue' else RED, x - 6, y - 3)
                self.update_score()
                self.next_turn()
            self.selected_piece = None
            self.piece_dragging = False

        elif event.type == pygame.MOUSEMOTION and self.piece_dragging:
            self.selected_pos = (event.pos[0] // CELL_SIZE, event.pos[1] // CELL_SIZE)

    def update_score(self):
        self.scores['blue'] = sum(row.count(BLUE) for row in self.board.grid)
        self.scores['red'] = sum(row.count(RED) for row in self.board.grid)

    def next_turn(self):
        self.turn = 'red' if self.turn == 'blue' else 'blue'
        if self.turn == 'red' and self.ai_enabled:
            self.ai_move()

    def ai_move(self):
        valid_moves = []
        for piece in PIECES['red']:
            for x in range(GRID_SIZE):
                for y in range(GRID_SIZE):
                    if self.board.is_valid_position(piece, x, y):
                        valid_moves.append((piece, x, y))
        if valid_moves:
            piece, x, y = random.choice(valid_moves)
            self.board.place_piece(piece, RED, x, y)
            self.update_score()
            self.next_turn()

    def is_game_over(self):
        return not any(self.board.is_valid_position(piece, x, y)
                       for piece in PIECES[self.turn]
                       for x in range(GRID_SIZE)
                       for y in range(GRID_SIZE))

    def declare_winner(self):
        if self.scores['blue'] > self.scores['red']:
            return "Blue wins!"
        elif self.scores['red'] > self.scores['blue']:
            return "Red wins!"
        else:
            return "It's a tie!"

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Blokus")

    game = BlokusGame(screen)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            game.handle_event(event)

        if game.is_game_over():
            winner = game.declare_winner()
            print(winner)
            pygame.quit()
            sys.exit()

        game.draw()
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
