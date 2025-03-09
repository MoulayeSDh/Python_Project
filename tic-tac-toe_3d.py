# tik tac toe 3d
from ursina import *

app = Ursina()

# Variables globales de gestion du jeu
current_player = 1   # 1 pour le joueur 1, 2 pour le joueur 2
game_over = False

# Création du plateau 3D (3x3x3)
board = [[[0 for _ in range(3)] for _ in range(3)] for _ in range(3)]
cells = {}  # Association : (i,j,k) -> cellule (Entity)

# Décalage pour centrer le plateau autour de l'origine
offset = Vec3(-1, -1, -1)

# Création des cases (cellules) cliquables
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
            cells[(i, j, k)] = cell

# Construction de la liste des lignes gagnantes (toutes les combinaisons possibles de 3 cases alignées)
winning_lines = []

# Lignes selon x (pour chaque j et k)
for j in range(3):
    for k in range(3):
        winning_lines.append([(0,j,k), (1,j,k), (2,j,k)])
# Lignes selon y (pour chaque i et k)
for i in range(3):
    for k in range(3):
        winning_lines.append([(i,0,k), (i,1,k), (i,2,k)])
# Lignes selon z (pour chaque i et j)
for i in range(3):
    for j in range(3):
        winning_lines.append([(i,j,0), (i,j,1), (i,j,2)])
# Diagonales dans les plans xy (pour chaque k)
for k in range(3):
    winning_lines.append([(0,0,k), (1,1,k), (2,2,k)])
    winning_lines.append([(0,2,k), (1,1,k), (2,0,k)])
# Diagonales dans les plans xz (pour chaque j)
for j in range(3):
    winning_lines.append([(0,j,0), (1,j,1), (2,j,2)])
    winning_lines.append([(0,j,2), (1,j,1), (2,j,0)])
# Diagonales dans les plans yz (pour chaque i)
for i in range(3):
    winning_lines.append([(i,0,0), (i,1,1), (i,2,2)])
    winning_lines.append([(i,0,2), (i,1,1), (i,2,0)])
# Diagonales spatiales (3D)
winning_lines.append([(0,0,0), (1,1,1), (2,2,2)])
winning_lines.append([(0,0,2), (1,1,1), (2,2,0)])
winning_lines.append([(0,2,0), (1,1,1), (2,0,2)])
winning_lines.append([(0,2,2), (1,1,1), (2,0,0)])

def check_win():
    """Vérifie si un joueur a gagné. Renvoie 0 si aucun, 1 ou 2 sinon."""
    for line in winning_lines:
        a, b, c = line
        if board[a[0]][a[1]][a[2]] != 0 and board[a[0]][a[1]][a[2]] == board[b[0]][b[1]][b[2]] == board[c[0]][c[1]][c[2]]:
            return board[a[0]][a[1]][a[2]]
    return 0

def draw_marker(i, j, k, player):
    """Dessine le marqueur dans la case (i,j,k) en fonction du joueur."""
    pos = cells[(i, j, k)].world_position
    if player == 1:
        # Pour le joueur 1 : dessiner un "X" avec deux entités fines
        Entity(model='cube', color=color.red, scale=(0.7, 0.1, 0.1), position=pos, rotation=Vec3(0,0,45))
        Entity(model='cube', color=color.red, scale=(0.7, 0.1, 0.1), position=pos, rotation=Vec3(0,0,-45))
    else:
        # Pour le joueur 2 : dessiner un "O" sous forme de sphère bleue
        Entity(model='sphere', color=color.blue, scale=0.4, position=pos)

def input(key):
    """Gestion des clics de souris."""
    global current_player, game_over
    if game_over:
        return
    if key == 'left mouse down' and mouse.hovered_entity:
        # Identification de la cellule cliquée
        for coord, cell in cells.items():
            if cell == mouse.hovered_entity:
                i, j, k = coord
                if board[i][j][k] == 0:
                    board[i][j][k] = current_player
                    draw_marker(i, j, k, current_player)
                    winner = check_win()
                    if winner:
                        print(f"Le joueur {winner} a gagné !")
                        game_over = True
                    else:
                        current_player = 2 if current_player == 1 else 1
                break

app.run()