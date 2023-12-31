import math
import time

import pygame


class Carte:
    def __init__(self, nom, couleur, cout_elixir, type_de_carte, pv, degats, reach, cooldown, speed, projectile=None,
                 x=None, y=None):
        self.nom = nom
        self.couleur = couleur
        self.x = x
        self.y = y
        self.cout_elixir = cout_elixir
        # troupe, batiment ou sort
        self.type_de_carte = type_de_carte
        self.max_pv = pv
        self.pv = pv
        self.degats = degats
        self.reach = reach
        self.projectile = projectile
        self.cooldown = cooldown
        # normal ou attaque
        self.state = "normal"
        self.fenetre = None
        self.icone = None
        self.image = None
        self.image_attaquant = None
        self.direction = 0
        self.speed = speed
        self.current_cooldown = time.time()

    def copy(self, coords):
        if coords:
            new_carte = Carte(self.nom, self.couleur, self.cout_elixir, self.type_de_carte, self.pv, self.degats,
                              self.reach, self.cooldown, self.speed, self.projectile, x=coords[0], y=coords[1])
        else:
            new_carte = Carte(self.nom, self.couleur, self.cout_elixir, self.type_de_carte, self.pv, self.degats,
                              self.reach, self.cooldown, self.speed, self.projectile)

        new_carte.initialize(self.fenetre)
        return new_carte

    def initialize(self, fenetre):
        self.fenetre = fenetre
        self.icone = pygame.image.load("images/cartes/icones/" + self.nom + ".png").convert_alpha()
        self.image = pygame.image.load("images/cartes/textures/" + self.nom + f"_{self.couleur}.png").convert_alpha()
        try:
            self.image_attaquant = pygame.image.load(
                f"images/cartes/textures/{self.nom}_{self.couleur}_attaquant.png").convert_alpha()
        except FileNotFoundError:
            self.image_attaquant = None

    def show_icone(self, x, y):
        self.fenetre.blit(self.icone, (x, y))

    def draw(self, x=None, y=None, transparent=False, tours=None, cartes_en_jeux=None):
        if x is not None and y is not None:
            self.x = x
            self.y = y
        rect = self.image.get_rect()
        rect.centerx = self.x
        rect.centery = self.y

        if (self.type_de_carte == "troupe" or self.type_de_carte == "wincondition") and not transparent:
            self.move(rect, tours, cartes_en_jeux)

        if transparent:
            transparent_image = self.image.copy()
            transparent_image.set_alpha(50)
            self.fenetre.blit(transparent_image, rect)
        else:
            rotated_image = pygame.transform.rotate(self.image, -self.direction)
            self.fenetre.blit(rotated_image, rect)


class Troupe(Carte):

    def __init__(self, nom, couleur, cout_elixir, pv, degats, reach, cooldown, speed, projectile=None, x=None, y=None,
                 type_de_carte="troupe"):
        super().__init__(nom, couleur, cout_elixir, type_de_carte, pv, degats, reach, cooldown, speed, projectile, x, y)
        self.closest_target_distance = 99999999
        self.closest_target = None
        self.visual_reach = 10

    def copy(self, coords):
        if coords:
            new_carte = Troupe(self.nom, self.couleur, self.cout_elixir, self.pv, self.degats, self.reach,
                               self.cooldown, self.speed, self.projectile, x=coords[0], y=coords[1],
                               type_de_carte=self.type_de_carte)
        else:
            new_carte = Troupe(self.nom, self.couleur, self.cout_elixir, self.pv, self.degats, self.reach,
                               self.cooldown, self.speed, self.projectile, type_de_carte=self.type_de_carte)

        new_carte.initialize(self.fenetre)
        return new_carte

    def closest_tour(self, tours):
        closest_tour = None
        closest_distance = 99999999
        for tour in tours:
            distance_entre_les_tours = distance(self, tour)
            if distance_entre_les_tours < closest_distance:
                closest_tour = tour
                closest_distance = distance_entre_les_tours
        self.closest_target_distance = closest_distance
        self.closest_target = closest_tour

    def find_closest_target(self, tours, cartes_en_jeux):
        target = None
        for carte in cartes_en_jeux:
            if not target:
                target = carte
            else:
                if distance(self, carte) < distance(self, target):
                    target = carte
        if not target:
            self.closest_tour(tours)
        else:
            self.closest_target = target
            self.closest_target_distance = distance(self, target)

    def update_direction(self, tours, cartes_en_jeux):
        # update direction based on the closest tour
        self.find_closest_target(tours, cartes_en_jeux)
        if self.closest_target:
            dx = self.closest_target.x - self.x
            if isinstance(self.closest_target, Tour) and((self.couleur == "rouge" and self.y < (400 - self.speed)) or (
                    self.couleur == "bleu" and self.y > (400 + self.speed))):
                dy = 400 - self.y
            else:
                dy = self.closest_target.y - self.y
            rad = math.atan2(dy, dx)  # In radians
            theta_deg = math.degrees(rad)  # Converts to degrees
            # rotate 90 degrees
            theta_deg_rotated = theta_deg + 90

            # ensure degrees are in 0-360 range

            self.direction = ((theta_deg_rotated + 360) % 360)

    def move(self, rect, tours, cartes_en_jeux):
        self.find_closest_target(tours, cartes_en_jeux)

        if self.closest_target_distance > (self.reach + self.visual_reach):
            self.update_direction(tours, cartes_en_jeux)
            radian_direction = math.radians(90 - self.direction)
            dx = self.speed * math.cos(radian_direction)
            dy = -self.speed * math.sin(radian_direction)  # minus here because pygame's y increases as we go down

            # Apply the changes to the x and y coordinates
            rect.centerx += dx
            rect.centery += dy
            self.x = rect.centerx
            self.y = rect.centery
        else:
            if time.time() > self.current_cooldown + self.cooldown and self.closest_target_distance <= (
                    self.visual_reach + self.reach):
                self.state = "normal"
                self.closest_target.pv -= self.degats
                print(self.closest_target.pv)
                if self.closest_target.pv <= 0:
                    self.closest_target_distance = 99999999
                # restart cooldown
                self.current_cooldown = time.time()


class WinCondition(Troupe):
    def __init__(self, nom, couleur, cout_elixir, pv, degats, reach, cooldown, speed, projectile=None, x=None, y=None):
        super().__init__(nom, couleur, cout_elixir, pv, degats, reach, cooldown, speed, projectile, x, y,
                         "wincondition")
        self.closest_building_distance = 99999999
        self.closest_building = None

    def copy(self, coords):
        if coords:
            new_carte = WinCondition(self.nom, self.couleur, self.cout_elixir, self.pv, self.degats, self.reach,
                                     self.cooldown, self.speed, self.projectile, x=coords[0], y=coords[1])
        else:
            new_carte = WinCondition(self.nom, self.couleur, self.cout_elixir, self.pv, self.degats, self.reach,
                                     self.cooldown, self.speed, self.projectile)

        new_carte.initialize(self.fenetre)
        return new_carte

    def closest_tour(self, tours):
        closest_tour = None
        closest_distance = 99999999
        for tour in tours:
            distance_entre_les_tours = distance(self, tour)
            if distance_entre_les_tours < closest_distance:
                closest_tour = tour
                closest_distance = distance_entre_les_tours
        self.closest_building_distance = closest_distance
        self.closest_building = closest_tour

    def find_closest_building(self, tours, cartes_en_jeux):
        batiment = None
        for carte in cartes_en_jeux:
            if carte.type_de_carte == "batiment":
                if not batiment:
                    batiment = carte
                else:
                    if distance(self, carte) < distance(self, batiment):
                        batiment = carte
        if not batiment:
            self.closest_tour(tours)
        else:
            self.closest_building = batiment
            self.closest_building_distance = distance(self, batiment)

    def update_direction(self, tours, cartes_en_jeux):
        # update direction based on the closest tour
        self.find_closest_building(tours, cartes_en_jeux)
        if self.closest_building:
            dx = self.closest_building.x - self.x
            if (self.couleur == "rouge" and self.y < (400 - self.speed)) or (
                    self.couleur == "bleu" and self.y > (400 + self.speed)):
                dy = 400 - self.y
            else:
                dy = self.closest_building.y - self.y
            rad = math.atan2(dy, dx)  # In radians
            theta_deg = math.degrees(rad)  # Converts to degrees
            # rotate 90 degrees
            theta_deg_rotated = theta_deg + 90

            # ensure degrees are in 0-360 range

            self.direction = ((theta_deg_rotated + 360) % 360)

    def move(self, rect, tours, cartes_en_jeux):
        self.find_closest_building(tours, cartes_en_jeux)

        if self.closest_building_distance > (self.reach + 50):
            self.update_direction(tours, cartes_en_jeux)
            radian_direction = math.radians(90 - self.direction)
            dx = self.speed * math.cos(radian_direction)
            dy = -self.speed * math.sin(radian_direction)  # minus here because pygame's y increases as we go down

            # Apply the changes to the x and y coordinates
            rect.centerx += dx
            rect.centery += dy
            self.x = rect.centerx
            self.y = rect.centery
        else:
            if time.time() > self.current_cooldown + self.cooldown and self.closest_building_distance <= (
                    self.reach + 50):
                self.state = "normal"
                self.closest_building.pv -= self.degats
                if self.closest_building.pv <= 0:
                    self.closest_building_distance = 99999999
                # restart cooldown
                self.current_cooldown = time.time()


class Tour:
    def __init__(self, couleur, x, y, type_de_tour, pv, degats, reach, cooldown, fenetre: pygame.display,
                 projectile=None):
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
        # normal ou attaque
        self.state = "normal"
        self.couleur = couleur
        self.image = pygame.image.load(f"images/tours/{self.couleur}_{self.type_de_tour}_tour.png").convert_alpha()
        self.active = False

    def draw(self):
        rect = self.image.get_rect()
        rect.centerx = self.x
        rect.centery = self.y
        self.fenetre.blit(self.image, rect)
        if not self.type_de_tour == "roi" or self.max_pv != self.pv:
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

            pygame.draw.rect(self.fenetre, couleur,
                             pygame.Rect(self.x - (tower_width / 2), self.y - tower_height, tower_width * health_ratio,
                                         health_bar_height))  # Blocking health
            pygame.draw.rect(self.fenetre, "black",
                             pygame.Rect(self.x - (tower_width / 2) + tower_width * health_ratio, self.y - tower_height,
                                         tower_width * (1 - health_ratio),
                                         health_bar_height))
            text = font.render(str(self.pv), True, "white")
            text_rect = text.get_rect()
            text_rect.centerx = self.x
            text_rect.y = self.y - tower_height

            self.fenetre.blit(text, text_rect)  # Put the text in center of health bar

    def __repr__(self):
        return f"Tour {self.couleur} {self.type_de_tour} x={self.x} y={self.y}"


class Projectile:
    def __init__(self, image, fenetre, vitesse, degats):
        self.image = image
        self.fenetre = fenetre
        self.vitesse = vitesse
        self.degats = degats
        self.image = pygame.image.load("images/" + image + ".png").convert_alpha()


def distance(object1, object2):
    x1 = object1.x
    x2 = object2.x
    y1 = object1.y
    y2 = object2.y
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def couleur_oppose(couleur: str):
    if couleur == "bleu":

        return "rouge"
    elif couleur == "rouge":
        return "bleu"
    elif couleur == "blue":
        return "red"
    elif couleur == "red":
        return "blue"
    else:
        raise ValueError("Couleur inconnue")
