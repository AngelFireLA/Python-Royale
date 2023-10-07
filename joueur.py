import carte
import random
class Joueur:

    def __init__(self, nom, type_de_joueur:str, deck:list, ):
        self.deck = deck
        self.tours = []
        self.nom = nom
        self.elixir = 10
        self.type = type_de_joueur
        self.deck = deck

    def jouer_carte(self):
        pass
