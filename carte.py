import math
import time

import pygame
class Carte:
    def __init__(self, nom, couleur, cout_elixir, type_de_carte, pv, degats, reach, cooldown, speed, target, projectile=None,x=None, y=None):
        self.nom = nom
        self.couleur = couleur
        self.x = x
        self.y = y
        self.cout_elixir = cout_elixir
        #troupe, batiment ou sort
        self.type_de_carte = type_de_carte
        self.max_pv = pv
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
        self.direction = 0
        self.speed = speed
        self.closest_tower_distance = 99999999
        self.closest_tower = None
        self.current_cooldown = time.time()
        self.target = target

    def copy(self, coords):
        if coords:
            new_carte = Carte(self.nom, self.couleur, self.cout_elixir, self.type_de_carte, self.pv, self.degats, self.reach, self.cooldown, self.speed, self.projectile, self.target, x=coords[0], y=coords[1])
        else:
            new_carte = Carte(self.nom, self.couleur, self.cout_elixir, self.type_de_carte, self.pv, self.degats, self.reach, self.cooldown, self.speed, self.target, self.projectile)

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

    def draw(self,x=None, y=None, transparent=False, tours=None, cartes_en_jeux=None):
        if not tours and not transparent:
            raise ValueError("oublié de donner les tours")
        if not cartes_en_jeux and not transparent:
            raise ValueError("oublié de donner les cartes")
        if x is not None and y is not None:
            self.x = x
            self.y = y
        rect = self.image.get_rect()
        rect.centerx = self.x
        rect.centery = self.y

        if self.type_de_carte == "troupe" and not transparent:
            self.move(rect, tours)


        if transparent:
            transparent_image = self.image.copy()
            transparent_image.set_alpha(50)
            self.fenetre.blit(transparent_image, rect)
        else:
            rotated_image = pygame.transform.rotate(self.image, -self.direction)
            self.fenetre.blit(rotated_image, rect)

    def move(self, rect, tours):
        if self.closest_tower_distance > self.reach+50:
            radian_direction = math.radians(90 - self.direction)
            dx = self.speed * math.cos(radian_direction)
            dy = -self.speed * math.sin(radian_direction) # minus here because pygame's y increases as we go down

            # Apply the changes to the x and y coordinates
            rect.centerx += dx
            rect.centery += dy
            self.x  = rect.centerx
            self.y = rect.centery
        else:
            self.direction = 0



class Troupe(Carte):

    def __init__(self, nom, couleur, cout_elixir, type_de_carte, pv, degats, reach, cooldown, speed, target, projectile=None,x=None, y=None):
        super().__init__(nom, couleur, cout_elixir, type_de_carte, pv, degats, reach, cooldown, speed, projectile, target, x, y)

    def copy(self, coords):
        if coords:
            new_carte = Troupe(self.nom, self.couleur, self.cout_elixir, self.type_de_carte, self.pv, self.degats, self.reach, self.cooldown, self.speed, self.target, self.projectile, x=coords[0], y=coords[1])
        else:
            new_carte = Troupe(self.nom, self.couleur, self.cout_elixir, self.type_de_carte, self.pv, self.degats, self.reach, self.cooldown, self.speed, self.target, self.projectile)

        new_carte.initialize(self.fenetre)
        return new_carte

    def closest_tour(self, tours):
        closest_tour = None
        closest_distance = 99999999
        for tour in tours:
            distance = (self.x - tour.x) ** 2 + (self.y - tour.y) ** 2
            if distance < closest_distance:
                closest_tour = tour
                closest_distance = distance
        self.closest_tower_distance = closest_distance
        self.closest_tower = closest_tour

    def closest_bat(self, cartes_en_jeux, tours):
        batiment = None
        for carte in cartes_en_jeux:
            if carte.type_de_carte == "batiment":
                batiment = carte
        if not batiment:
            return self.closest_tour(tours)

    def update_direction(self, tours):
        #update direction based on the closest tour
        self.closest_tour(tours)
        if self.closest_tower:
            dx = self.closest_tower.x - self.x
            if (self.couleur == "rouge" and self.y < (400-self.speed)) or (self.couleur == "bleu" and self.y > (400+self.speed)):
                dy = 400 - self.y
            else:
                dy = self.closest_tower.y - self.y
            rad = math.atan2(dy, dx)  # In radians
            theta_deg = math.degrees(rad)  # Converts to degrees
            # rotate 90 degrees
            theta_deg_rotated = theta_deg + 90

            # ensure degrees are in 0-360 range

            self.direction = ((theta_deg_rotated + 360) % 360)

    def move(self, rect, tours):
        if self.closest_tower_distance > (self.reach+50)**2:
            self.update_direction(tours)
            radian_direction = math.radians(90 - self.direction)
            dx = self.speed * math.cos(radian_direction)
            dy = -self.speed * math.sin(radian_direction) # minus here because pygame's y increases as we go down

            # Apply the changes to the x and y coordinates
            rect.centerx += dx
            rect.centery += dy
            self.x  = rect.centerx
            self.y = rect.centery
        else:
            self.direction = 0
            # check if the attack cooldown is finished, if true, remove hp from nearest tower and then restart cooldown
            self.closest_tour(tours)

            if time.time() > self.current_cooldown + self.cooldown and self.closest_tower_distance <= (self.reach+50)**2:
                self.state = "normal"
                self.closest_tower.pv -= self.degats
                if self.closest_tower.pv <=0:
                    self.closest_tower_distance = 99999999
                #restart cooldown
                self.current_cooldown = time.time()
class Tour:
    def __init__(self, couleur, x, y, type_de_tour, pv, degats, reach, cooldown, fenetre: pygame.display, projectile=None):
        self.type_de_tour = type_de_tour
        self.x = x
        self.y = y
        self.fenetre = fenetre
        self.max_pv = pv
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
        if not self.type_de_tour == "roi" or self.max_pv!=self.pv:
            font = pygame.font.Font(None, 22)
            health_ratio = self.pv / self.max_pv
            if self.couleur == "rouge":
                tower_height = 65
                tower_width = 70
                couleur = "red"
            else:
                tower_height = -50
                tower_width = 70
                couleur = "blue"
            health_bar_height = 15

            pygame.draw.rect(self.fenetre, couleur, pygame.Rect(self.x-(tower_width/2), self.y-tower_height, tower_width * health_ratio, health_bar_height))  # Blocking health
            pygame.draw.rect(self.fenetre, "black",
                             pygame.Rect(self.x-(tower_width/2) + tower_width * health_ratio, self.y-tower_height, tower_width * (1 - health_ratio),
                                         health_bar_height))
            text = font.render(str(self.pv), True, "white")
            text_rect = text.get_rect()
            text_rect.centerx = self.x
            text_rect.y = self.y-tower_height

            self.fenetre.blit(text, text_rect) # Put the text in center of health bar

    def __repr__(self):
        return f"Tour {self.couleur} {self.type_de_tour} x={self.x} y={self.y}"

class Projectile:
    def __init__(self, image, fenetre, vitesse, degats):
        self.image = image
        self.fenetre = fenetre
        self.vitesse = vitesse
        self.degats = degats
        self.image = pygame.image.load("images/" + image + ".png").convert_alpha()

def distance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)