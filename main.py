import pygame
import carte
import combat
import joueur
pygame.init()



joueur_bleu =  joueur.Joueur("bleu", "joueur",[])
joueur_rouge = joueur.Joueur("rouge", "bot",[])

combat1 = combat.Combat(joueur_bleu, joueur_rouge, "arene")
combat1.demarrer_combat()









