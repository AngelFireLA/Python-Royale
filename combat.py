import random
import sys
import time

import pygame

import carte
from joueur import Joueur
from carte import Carte

#Affiche un texte selon des paramètres
def afficher_text(fenetre, texte: str, x: int, y: int, taille, font_choisi: str, couleur=(0, 0, 0), center=False):
  fontt = pygame.font.SysFont(font_choisi, taille)
  text_surface = fontt.render(texte, True, couleur)
  if center:
    text_x = (fenetre.get_width() - text_surface.get_width()) // 2
    text_y = (fenetre.get_height() - text_surface.get_height()) // 2
  else:
    text_x = x
    text_y = y

  return text_surface, (text_x, text_y)


def update_elixir(joueur, last_time, elixir_cooldown):
    current_time = time.time()
    if current_time - last_time >= elixir_cooldown:
        joueur.elixir += 1
        last_time = current_time
    return last_time


class Combat:

    def __init__(self, joueur1, joueur2, arriere_plan):
        self.arriere_plan = pygame.image.load("images/arenes/" + arriere_plan + ".png")
        self.joueur1: Joueur = joueur1
        self.joueur2: Joueur = joueur2
        self.elixir_cooldown = 2.8
        self.card_placement_bounds_bleu = [(0, 550), (400, 800)]
        self.card_placement_bounds_rouge = [(0, 550), (0, 400)]
        self.card_slots = []
        self.cards_on_the_field = []

    def demarrer_combat(self):
        # Créer la fenêtre
        pygame.init()


        width, height = 550, 950
        fenetre = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Python Royale")
        clock = pygame.time.Clock()

        # place les tours de chaque joueur
        self.joueur1.tours.append(carte.Tour("bleu", 275, 700, "roi", 4824, 109, 100, 1, fenetre))
        self.joueur1.tours.append(carte.Tour("bleu", 100, 600, "princesse", 3052, 109, 200, 0.8, fenetre))
        self.joueur1.tours.append(carte.Tour("bleu", 450, 600, "princesse", 3052, 109, 200, 0.8, fenetre))
        self.joueur2.tours.append(carte.Tour("rouge", 275, 100, "roi", 4824, 109, 100, 1, fenetre))
        self.joueur2.tours.append(carte.Tour("rouge", 100, 200, "princesse", 3052, 109, 200, 0.8, fenetre))
        self.joueur2.tours.append(carte.Tour("rouge", 450, 200, "princesse", 3052, 109, 200, 0.8, fenetre))

        # créer les emplacements vides de cartes
        self.card_slots.append(EmplacementDeCarte(0, 800, "images/battle_misc/empty_card_slot.png", fenetre, 0))
        self.card_slots.append(EmplacementDeCarte(138, 800, "images/battle_misc/empty_card_slot.png", fenetre, 1))
        self.card_slots.append(EmplacementDeCarte(276, 800, "images/battle_misc/empty_card_slot.png", fenetre, 2))
        self.card_slots.append(EmplacementDeCarte(413, 800, "images/battle_misc/empty_card_slot.png", fenetre, 3))

        # démarre l'elixir de chaque joueur, et sa recharge
        self.joueur1.elixir = 5
        self.joueur2.elixir = 5
        last_time_elixir_recharged_player1 = time.time()
        last_time_elixir_recharged_player2 = time.time()
        selected_card_slot = None

        # randomisation des decks
        random.shuffle(self.joueur1.deck)
        random.shuffle(self.joueur2.deck)

        for c in self.joueur1.deck:
            c.initialize(fenetre)
        for c in self.joueur2.deck:
            c.initialize(fenetre)


        combat_en_cours = True
        while combat_en_cours:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # print coordinates of left clicked
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # check if mouse y is below 800 and before 910
                    if 800 < event.pos[1] < 910:
                        card_slot_number = event.pos[0] // 138
                        if card_slot_number < 4:
                            if self.card_slots[card_slot_number].carte is not None:
                                if self.card_slots[card_slot_number].selected:
                                    self.card_slots[card_slot_number].selected = False
                                    selected_card_slot = None
                                else:
                                    for c in self.card_slots:
                                        c.selected = False
                                    self.card_slots[card_slot_number].selected = True
                                    selected_card_slot = self.card_slots[card_slot_number]

                    #vérifie si l'utilisateur place une carte dans de bonnes conditions
                    elif selected_card_slot and selected_card_slot.carte and self.is_mouse_in_bound() and self.joueur1.elixir >= selected_card_slot.carte.cout_elixir:
                        self.cards_on_the_field.append(selected_card_slot.carte.copy((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])))
                        self.joueur1.elixir -= selected_card_slot.carte.cout_elixir
                        selected_card_slot.carte = None
                        selected_card_slot.last_time_card_was_placed = time.time()
                        print("placed card")
                        selected_card_slot.selected = False
                        selected_card_slot = None

            # Clear the screen
            fenetre.blit(self.arriere_plan, (0, 0))
            elixir = pygame.image.load(f"images/elixir/elixirbar_{self.joueur1.elixir}.png").convert_alpha()
            # elixir = pygame.transform.scale_by(elixir, 0.5)
            fenetre.blit(elixir, (0, 910))

            for card_slot in self.card_slots:
                card_slot: EmplacementDeCarte
                if not card_slot.carte and card_slot.last_time_card_was_placed + 0.5 < time.time():
                    card_slot.carte = self.joueur1.deck[card_slot.numero]
                card_slot.draw()


            #essaye de recharger l'elixir
            last_time_elixir_recharged_player1 = update_elixir(self.joueur1, last_time_elixir_recharged_player1, self.elixir_cooldown)
            last_time_elixir_recharged_player2 = update_elixir(self.joueur2, last_time_elixir_recharged_player2, self.elixir_cooldown)

            if self.joueur1.elixir > 10:
                self.joueur1.elixir = 10
            if self.joueur2.elixir > 10:
                self.joueur2.elixir = 10

            # dessine les tours
            for tour in self.joueur1.tours:
                if tour.pv <=0:
                    if tour.type_de_tour == "roi":
                        print("roi mort")
                        return
                    self.joueur1.tours.remove(tour)
                    continue
                tour.draw()
            for tour in self.joueur2.tours:
                if tour.pv <=0:
                    if tour.type_de_tour == "roi":
                        print("roi mort")
                        new_game_text = afficher_text(fenetre,
                                                      f"Partie terminée!",
                                                      fenetre.get_width(),
                                                      fenetre.get_height(), 60, "Impact", center=True,
                                                      couleur=(255, 255, 255))
                        fenetre.blit(new_game_text[0], new_game_text[1])
                        pygame.display.flip()
                        pygame.time.delay(3000)
                        combat_en_cours = False
                        continue
                    else:
                        self.joueur2.tours.remove(tour)
                        continue
                tour.draw()

            # dessine les cartes sur le terrain
            for card in self.cards_on_the_field:
                if card.couleur == "bleu":
                    card.draw(tours=self.joueur2.tours, cartes_en_jeux=self.cards_on_the_field)
                else:
                    card.draw(tours=self.joueur1.tours, cartes_en_jeux=self.cards_on_the_field)





            # check if mouse is in card_placement_bounds_bleu
            if selected_card_slot and selected_card_slot.carte and self.is_mouse_in_bound():
                selected_card_slot: EmplacementDeCarte
                selected_card_slot.carte.draw(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], True)

            # Update the display
            pygame.display.flip()
            clock.tick(30)

    def is_mouse_in_bound(self):
        if self.card_placement_bounds_bleu[0][0] < pygame.mouse.get_pos()[0] < self.card_placement_bounds_bleu[0][1] and \
                self.card_placement_bounds_bleu[1][0] < pygame.mouse.get_pos()[1] < self.card_placement_bounds_bleu[1][1]:
            return True
        return False


class EmplacementDeCarte:
    def __init__(self, x, y, image, fenetre, numero):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)
        self.fenetre = fenetre
        self.carte: Carte = None
        self.numero = numero
        self.selected = False
        self.last_time_card_was_placed = 0

    def draw(self):
        self.fenetre.blit(self.image, (self.x, self.y))
        if self.carte is not None:
            self.carte.show_icone(self.x, self.y)
            elixir = pygame.image.load(f"images/elixir/elixir_{self.carte.cout_elixir}.png").convert_alpha()
            self.fenetre.blit(elixir, (self.x, self.y))
            if self.selected:
                selected_image = pygame.image.load("images/battle_misc/selected_card_slot.png").convert_alpha()
                self.fenetre.blit(selected_image, (self.x, self.y))
