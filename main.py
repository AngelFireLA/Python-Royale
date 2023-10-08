import pygame
import carte
from carte import Carte, Troupe
import combat
import joueur
pygame.init()


while True:
    joueur_bleu =  joueur.Joueur("bleu", "joueur",[])
    joueur_rouge = joueur.Joueur("rouge", "bot",[])
    #vraie attaque du golem = 312
    cartes_bleu = [
        Troupe("golem", "bleu", 2, "troupe", 5120, 1000, 8, 2.51, 4),
        Troupe("golem", "bleu", 2, "troupe", 5120, 1000, 8, 2.51, 4),
        Troupe("golem", "bleu", 2, "troupe", 5120, 1000, 8, 2.51, 4),
        Troupe("golem", "bleu", 2, "troupe", 5120, 1000, 8, 2.51, 4),
    ]

    cartes_rouge = [
        Troupe("golem", "rouge", 2, "troupe", 5120, 312, 8, 2.51, 4),
        Troupe("golem", "rouge", 2, "troupe", 5120, 312, 8, 2.51, 4),
        Troupe("golem", "rouge", 2, "troupe", 5120, 312, 8, 2.51, 4),
        Troupe("golem", "rouge", 2, "troupe", 5120, 312, 8, 2.51, 4),
    ]

    joueur_bleu.deck = cartes_bleu
    joueur_rouge.deck = cartes_rouge

    combat1 = combat.Combat(joueur_bleu, joueur_rouge, "arene_herbe")
    combat1.demarrer_combat()









