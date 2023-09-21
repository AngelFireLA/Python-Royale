import pygame
class Carte:
    def __init__(self, x, y, cout_elixir, type_de_carte, pv, degats, reach, cooldown, image, projectile=None):
        self.x = x
        self.y = y
        self.cout_elixir = cout_elixir
        self.type_de_carte = type_de_carte
        self.pv = pv
        self.degats = degats
        self.reach = reach
        self.projectile = projectile
        self.cooldown = cooldown
        #normal ou attaque
        self.state = "normal"
        self.image = pygame.image.load("images/"+image+".png").convert_alpha()
        self.image_attaquant = pygame.image.load(f"images/{image}_attaquant.png").convert_alpha()


class Tour:
    def __init__(self, x, y, type_de_tour, pv, degats, reach, cooldown, image, projectile=None):
        self.type_de_tour = type_de_tour
        self.x = x
        self.y = y
        self.pv = pv
        self.degats = degats
        self.reach = reach
        self.projectile = projectile
        self.cooldown = cooldown
        #normal ou attaque
        self.state = "normal"
        self.image = pygame.image.load("images/"+image+".png").convert_alpha()

class Projectile:
    def __init__(self, image, fenetre, vitesse, degats):
        self.image = image
        self.fenetre = fenetre
        self.vitesse = vitesse
        self.degats = degats
        self.image = pygame.image.load("images/" + image + ".png").convert_alpha()




