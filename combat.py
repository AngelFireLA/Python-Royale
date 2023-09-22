import sys
import time

import pygame

import carte
from joueur import Joueur


def update_elixir(joueur, last_time):
    current_time = time.time()
    if current_time - last_time >= 1:
        joueur.elixir += 1
        last_time = current_time
    return last_time


class Combat:

    def __init__(self, joueur1, joueur2, arriere_plan):
        self.arriere_plan = pygame.image.load("images/" + arriere_plan + ".png")
        self.joueur1: Joueur = joueur1
        self.joueur2: Joueur = joueur2

    def demarrer_combat(self):
        # Initialize Pygame
        pygame.init()

        # Set up the display
        width, height = 550, 800
        fenetre = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Python Royale")

        self.joueur1.elixir = 0
        self.joueur2.elixir = 10
        self.joueur1.tours.append(carte.Tour("bleu", 275, 650, "roi", 1000, 100, 50, 1, fenetre))
        self.joueur1.tours.append(carte.Tour("bleu", 100, 550, "princesse", 500, 50, 50, 1, fenetre))
        self.joueur1.tours.append(carte.Tour("bleu", 450, 550, "princesse", 500, 50, 50, 1, fenetre))
        self.joueur2.tours.append(carte.Tour("rouge", 275, 50, "roi", 1000, 100, 50, 1, fenetre))
        self.joueur2.tours.append(carte.Tour("rouge", 100, 150, "princesse", 500, 50, 50, 1, fenetre))
        self.joueur2.tours.append(carte.Tour("rouge", 450, 150, "princesse", 500, 50, 50, 1, fenetre))

        last_time_j1 = time.time()
        last_time_j2 = time.time()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # print coordinates of left clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(event.pos)
            # Clear the screen
            fenetre.blit(self.arriere_plan, (0, 0))
            elixir = pygame.image.load(f"images/elixirbar_{self.joueur1.elixir}.png")
            #elixir = pygame.transform.scale_by(elixir, 0.5)
            fenetre.blit(elixir, (0, 760))

            for tour in self.joueur1.tours:
                tour.draw()
            for tour in self.joueur2.tours:
                tour.draw()

            last_time_j1 = update_elixir(self.joueur1, last_time_j1)
            last_time_j2 = update_elixir(self.joueur2, last_time_j2)
            if self.joueur1.elixir > 10:
                self.joueur1.elixir = 10
            if self.joueur2.elixir > 10:
                self.joueur2.elixir = 10

            # Update the display
            pygame.display.flip()
