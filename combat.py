import pygame
from joueur import Joueur
import sys
import carte
class Combat:

    def __init__(self, joueur1, joueur2, arriere_plan):
        self.arriere_plan = pygame.image.load("images/"+arriere_plan+".png")
        self.joueur1 = joueur1
        self.joueur2 = joueur2

    def demarrer_combat(self):
        # Initialize Pygame
        pygame.init()

        # Set up the display
        width, height = 550, 800
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Python Royale")


        # self.joueur1.elixir = 10
        # self.joueur2.elixir = 10

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # Clear the screen
            screen.blit(self.arriere_plan, (0, 0))

            # Update the display
            pygame.display.flip()