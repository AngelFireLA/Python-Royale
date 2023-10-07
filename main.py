import pygame
import carte
from carte import Carte
import combat
import joueur
pygame.init()



joueur_bleu =  joueur.Joueur("bleu", "joueur",[])
joueur_rouge = joueur.Joueur("rouge", "bot",[])

cartes_bleu = [
    Carte("golem", "bleu", 2, "troupe", 5120, 312, 10, 2.51),
    Carte("golem", "bleu", 2, "troupe", 5120, 312, 10, 2.51),
    Carte("golem", "bleu", 2, "troupe", 5120, 312, 10, 2.51),
    Carte("golem", "bleu", 2, "troupe", 5120, 312, 10, 2.51),
]

cartes_rouge = [
    Carte("golem", "rouge", 2, "troupe", 5120, 312, 10, 2.51),
    Carte("golem", "rouge", 2, "troupe", 5120, 312, 10, 2.51),
    Carte("golem", "rouge", 2, "troupe", 5120, 312, 10, 2.51),
    Carte("golem", "rouge", 2, "troupe", 5120, 312, 10, 2.51),
]

joueur_bleu.deck = cartes_bleu
joueur_rouge.deck = cartes_rouge

combat1 = combat.Combat(joueur_bleu, joueur_rouge, "arene_herbe")
combat1.demarrer_combat()









