import pygame
class Carte:
    def __init__(self, nom, couleur, cout_elixir, type_de_carte, pv, degats, reach, cooldown, projectile=None,x=None, y=None):
        self.nom = nom
        self.couleur = couleur
        self.x = x
        self.y = y
        self.cout_elixir = cout_elixir
        #troupe, batiment ou sort
        self.type_de_carte = type_de_carte
        self.pv = pv
        self.degats = degats
        self.reach = reach
        self.projectile = projectile
        self.cooldown = cooldown
        #normal ou attaque
        self.state = "normal"
        self.fenetre = None
        self.icone = None
        self.image = None
        self.image_attaquant = None

    def copy(self, coords):
        if coords:
            new_carte = Carte(self.nom, self.couleur, self.cout_elixir, self.type_de_carte, self.pv, self.degats, self.reach, self.cooldown, self.projectile, x=coords[0], y=coords[1])
        else:
            new_carte = Carte(self.nom, self.couleur, self.cout_elixir, self.type_de_carte, self.pv, self.degats, self.reach, self.cooldown, self.projectile)

        new_carte.initialize(self.fenetre)
        return new_carte

    def initialize(self, fenetre):
        self.fenetre = fenetre
        self.icone = pygame.image.load("images/cartes/icones/" + self.nom + ".png").convert_alpha()
        self.image = pygame.image.load("images/cartes/textures/" + self.nom + f"_{self.couleur}.png").convert_alpha()
        try:
            self.image_attaquant = pygame.image.load(f"images/cartes/textures/{self.nom}_{self.couleur}_attaquant.png").convert_alpha()
        except FileNotFoundError:
            self.image_attaquant = None
    def show_icone(self,x,y):
        self.fenetre.blit(self.icone, (x, y))

    def draw(self,x=None, y=None, transparent=False):
        if x is not None and y is not None:
            self.x = x
            self.y = y
        rect = self.image.get_rect()
        rect.centerx = self.x
        rect.centery = self.y
        if transparent:
            transparent_image = self.image.copy()
            transparent_image.set_alpha(50)
            self.fenetre.blit(transparent_image, rect)
        else:
            self.fenetre.blit(self.image, rect)

    def closest_tour(self, tours):
        closest_tour = None
        closest_distance = 999999
        for tour in tours:
            distance = (self.x - tour.x) ** 2 + (self.y - tour.y) ** 2
            if distance < closest_distance:
                closest_tour = tour
                closest_distance = distance
        return closest_tour

class Tour:
    def __init__(self, couleur, x, y, type_de_tour, pv, degats, reach, cooldown, fenetre: pygame.display, projectile=None):
        self.type_de_tour = type_de_tour
        self.x = x
        self.y = y
        self.fenetre = fenetre
        self.pv = pv
        self.degats = degats
        self.reach = reach
        self.projectile = projectile
        self.cooldown = cooldown
        #normal ou attaque
        self.state = "normal"
        self.couleur = couleur
        self.image = pygame.image.load(f"images/tours/{self.couleur}_{self.type_de_tour}_tour.png").convert_alpha()
        self.active = False
    def draw(self):
        rect = self.image.get_rect()
        rect.centerx = self.x
        rect.centery = self.y
        self.fenetre.blit(self.image, rect)

    def __repr__(self):
        return f"Tour {self.couleur} {self.type_de_tour} x={self.x} y={self.y}"

class Projectile:
    def __init__(self, image, fenetre, vitesse, degats):
        self.image = image
        self.fenetre = fenetre
        self.vitesse = vitesse
        self.degats = degats
        self.image = pygame.image.load("images/" + image + ".png").convert_alpha()
