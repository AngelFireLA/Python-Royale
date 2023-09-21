import carte
class Joueur:

    def __init__(self, nom, deck:list):
        self.deck = deck
        self.tours = None
        for c in deck:
            if not isinstance(c, carte.Carte):
                raise ValueError("Un deck ne contient pas que des cartes")
        self.nom = nom
        self.elixir = 10
