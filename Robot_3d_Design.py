# robot 3d
!pip install vpython
from vpython import *

# Création de la scène
scene = canvas(title='Robot 3D', width=800, height=600, center=vector(0,1,0), background=color.gray(0.2))

# Corps du robot (boîte rouge)
corps = box(pos=vector(0,1,0), size=vector(1,2,0.5), color=color.red)

# Tête du robot (sphère jaune)
tete = sphere(pos=vector(0,2.5,0), radius=0.5, color=color.yellow)

# Bras gauche et droit (boîtes vertes)
bras_gauche = box(pos=vector(-0.75,1.5,0), size=vector(0.5,1.2,0.5), color=color.green)
bras_droit  = box(pos=vector(0.75,1.5,0), size=vector(0.5,1.2,0.5), color=color.green)

# Jambes gauche et droite (boîtes bleues)
jambe_gauche = box(pos=vector(-0.3,0,0), size=vector(0.4,1,0.4), color=color.blue)
jambe_droite = box(pos=vector(0.3,0,0), size=vector(0.4,1,0.4), color=color.blue)

# Animation : rotation continue du robot autour de l'axe vertical
while True:
    rate(50)
    for partie in (corps, tete, bras_gauche, bras_droit, jambe_gauche, jambe_droite):
        partie.rotate(angle=0.01, axis=vector(0,1,0), origin=vector(0,1,0))