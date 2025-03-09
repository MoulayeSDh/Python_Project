import pygame
import math
import sys
import random
from pygame.math import Vector2

# -------------------- Configuration Générale --------------------

WIDTH, HEIGHT = 800, 600
FPS = 60

# -------------------- Définition du Joueur --------------------

class Player:
    def __init__(self):
        self.radius = 15
        self.color = (255, 255, 255)  # blanc
        self.pos = Vector2(WIDTH / 2, HEIGHT - 50)
        self.speed = 5  # Déplacement progressif
        self.moving = False  # État du toucher

    def handle_input(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.moving = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.moving = False
        
        if self.moving:
            target = Vector2(pygame.mouse.get_pos())
            direction = target - self.pos
            if direction.length() > self.speed:
                direction = direction.normalize() * self.speed
            self.pos += direction

        # Empêcher de sortir de l'écran
        self.pos.x = max(self.radius, min(WIDTH - self.radius, self.pos.x))
        self.pos.y = max(self.radius, min(HEIGHT - self.radius, self.pos.y))

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)

# -------------------- Définition des Obstacles --------------------

class Obstacle:
    def __init__(self, center, sides, radius, color, angular_velocity, base_speed):
        self.center = Vector2(center)
        self.sides = sides
        self.radius = radius
        self.color = color
        self.rotation = 0.0
        self.angular_velocity = angular_velocity
        self.base_speed = base_speed  # Vitesse initiale
        self.speed = base_speed  # Vitesse actuelle

    def get_vertices(self):
        return [
            (
                self.center.x + self.radius * math.cos(self.rotation + i * (2 * math.pi / self.sides)),
                self.center.y + self.radius * math.sin(self.rotation + i * (2 * math.pi / self.sides))
            ) for i in range(self.sides)
        ]

    def update(self):
        self.center.x -= self.speed
        self.rotation += self.angular_velocity
        if self.center.x + self.radius < 0:
            self.recycle()

    def recycle(self):
        self.center.x = WIDTH + self.radius
        self.center.y = random.randint(self.radius, HEIGHT - self.radius)
        self.speed = self.base_speed  # Réinitialiser la vitesse de l'obstacle

    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, [(int(x), int(y)) for x, y in self.get_vertices()], 2)

# -------------------- Gestion des Collisions --------------------

def point_in_polygon(point, polygon):
    x, y = point
    inside = False
    n = len(polygon)
    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def circle_polygon_collision(circle_center, circle_radius, polygon):
    poly_center = sum((Vector2(x, y) for x, y in polygon), Vector2()) / len(polygon)
    
    if (circle_center - poly_center).length() > circle_radius + max(Vector2(x, y).length() for x, y in polygon):
        return False  

    return point_in_polygon((circle_center.x, circle_center.y), polygon) or any(
        (circle_center - Vector2(x, y)).length() < circle_radius for x, y in polygon
    )

# -------------------- Score & Difficulté --------------------

class Score:
    def __init__(self):
        self.start_time = pygame.time.get_ticks()

    def get_score(self):
        return (pygame.time.get_ticks() - self.start_time) // 1000  

    def draw(self, screen):
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {self.get_score()}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

class DifficultyManager:
    def __init__(self):
        self.last_update_time = pygame.time.get_ticks()
        self.multiplier = 1.0

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > 5000:  # Mise à jour toutes les 5 secondes
            self.multiplier += 0.1  # Augmentation progressive
            self.last_update_time = current_time

    def get_multiplier(self):
        return self.multiplier

# -------------------- Boucle Principale --------------------

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Évitez les formes (Contrôle tactile)")
    clock = pygame.time.Clock()

    player = Player()
    score = Score()
    difficulty = DifficultyManager()

    obstacles = [
        Obstacle((WIDTH + 100, random.randint(50, HEIGHT - 50)), 3, 30, (255, 0, 0), 0.03, 3),
        Obstacle((WIDTH + 300, random.randint(50, HEIGHT - 50)), 4, 40, (0, 255, 0), 0.02, 4),
        Obstacle((WIDTH + 500, random.randint(50, HEIGHT - 50)), 5, 50, (0, 0, 255), 0.04, 2)
    ]

    game_over = False
    font = pygame.font.SysFont(None, 48)

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not game_over:
            player.handle_input(events)
            difficulty.update()  # Met à jour la difficulté

            for obs in obstacles:
                obs.speed = obs.base_speed * difficulty.get_multiplier()  # Applique la difficulté correctement
                obs.update()
                if circle_polygon_collision(player.pos, player.radius, obs.get_vertices()):
                    game_over = True
                    break

        # Affichage
        screen.fill((100, 0, 0) if game_over else (30, 30, 30))
        player.draw(screen)
        for obs in obstacles:
            obs.draw(screen)
        
        if game_over:
            text = font.render("GAME OVER", True, (255, 255, 255))
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        else:
            score.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    main()