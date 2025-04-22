import pygame
import sys
import numpy as np
from stable_baselines3 import DQN
import subprocess

pygame.init()

TAILLE = 300
LIGNE_WIDTH = 5
SCREEN = pygame.display.set_mode((TAILLE, TAILLE))
pygame.display.set_caption("Tic Tac Toe")

BLANC = (255, 255, 255)
NOIR = (0, 0, 0)

grille = [[0 for _ in range(3)] for _ in range(3)]
JOUEUR = 1
contre_ia = False
model = DQN.load("dqn_tictactoe")

def dessiner_grille():
    SCREEN.fill(BLANC)
    pygame.draw.line(SCREEN, NOIR, (100, 0), (100, 300), LIGNE_WIDTH)
    pygame.draw.line(SCREEN, NOIR, (200, 0), (200, 300), LIGNE_WIDTH)
    pygame.draw.line(SCREEN, NOIR, (0, 100), (300, 100), LIGNE_WIDTH)
    pygame.draw.line(SCREEN, NOIR, (0, 200), (300, 200), LIGNE_WIDTH)

def dessiner_symboles():
    for ligne in range(3):
        for col in range(3):
            if grille[ligne][col] == 1:
                pygame.draw.line(SCREEN, NOIR, (col*100 + 20, ligne*100 + 20), (col*100 + 80, ligne*100 + 80), 5)
                pygame.draw.line(SCREEN, NOIR, (col*100 + 80, ligne*100 + 20), (col*100 + 20, ligne*100 + 80), 5)
            elif grille[ligne][col] == -1:
                pygame.draw.circle(SCREEN, NOIR, (col*100 + 50, ligne*100 + 50), 35, 5)

def clic_utilisateur(pos):
    global JOUEUR
    ligne = pos[1] // 100
    col = pos[0] // 100
    if grille[ligne][col] == 0:
        grille[ligne][col] = JOUEUR
        JOUEUR *= -1

def verifier_victoire():
    for ligne in grille:
        if sum(ligne) == 3: return 1
        elif sum(ligne) == -3: return -1
    for col in range(3):
        somme_col = grille[0][col] + grille[1][col] + grille[2][col]
        if somme_col == 3: return 1
        elif somme_col == -3: return -1
    diag1 = grille[0][0] + grille[1][1] + grille[2][2]
    diag2 = grille[0][2] + grille[1][1] + grille[2][0]
    if diag1 == 3 or diag2 == 3: return 1
    elif diag1 == -3 or diag2 == -3: return -1
    if not any(0 in ligne for ligne in grille): return 0
    return None

def afficher_resultat(message):
    font = pygame.font.SysFont(None, 40)
    texte = font.render(message, True, NOIR)
    bouton_rejouer = pygame.Rect(50, 200, 100, 40)
    bouton_menu = pygame.Rect(160, 200, 100, 40)

    while True:
        SCREEN.fill(BLANC)
        SCREEN.blit(texte, (TAILLE//2 - texte.get_width()//2, 100))

        pygame.draw.rect(SCREEN, (200, 200, 200), bouton_rejouer)
        pygame.draw.rect(SCREEN, (200, 200, 200), bouton_menu)
        texte1 = font.render("Rejouer", True, NOIR)
        texte2 = font.render("Menu", True, NOIR)
        SCREEN.blit(texte1, (60, 205))
        SCREEN.blit(texte2, (175, 205))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_rejouer.collidepoint(event.pos):
                    reset_jeu()
                    return
                elif bouton_menu.collidepoint(event.pos):
                    reset_jeu()
                    main()
                    return

def reset_jeu():
    global grille, JOUEUR
    grille = [[0 for _ in range(3)] for _ in range(3)]
    JOUEUR = 1

def afficher_menu():
    global contre_ia
    font = pygame.font.SysFont(None, 36)
    bouton_ia = pygame.Rect(50, 60, 200, 50)
    bouton_2j = pygame.Rect(50, 120, 200, 50)
    bouton_online = pygame.Rect(50, 180, 200, 50)
    bouton_quitter = pygame.Rect(50, 240, 200, 50)

    while True:
        SCREEN.fill(BLANC)
        titre = font.render("Choisissez un mode :", True, NOIR)
        SCREEN.blit(titre, (TAILLE//2 - titre.get_width()//2, 20))

        pygame.draw.rect(SCREEN, (180, 180, 180), bouton_ia)
        texte_ia = font.render("Jouer contre IA", True, NOIR)
        SCREEN.blit(texte_ia, (TAILLE//2 - texte_ia.get_width()//2, 70))

        pygame.draw.rect(SCREEN, (180, 180, 180), bouton_2j)
        texte_2j = font.render("2 Joueurs local", True, NOIR)
        SCREEN.blit(texte_2j, (TAILLE//2 - texte_2j.get_width()//2, 130))

        pygame.draw.rect(SCREEN, (180, 180, 180), bouton_online)
        texte_online = font.render("Jouer en ligne", True, NOIR)
        SCREEN.blit(texte_online, (TAILLE//2 - texte_online.get_width()//2, 190))

        pygame.draw.rect(SCREEN, (200, 100, 100), bouton_quitter)
        texte_quitter = font.render("Quitter", True, NOIR)
        SCREEN.blit(texte_quitter, (TAILLE//2 - texte_quitter.get_width()//2, 250))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_ia.collidepoint(event.pos):
                    contre_ia = True
                    return "ia"
                elif bouton_2j.collidepoint(event.pos):
                    contre_ia = False
                    return "local"
                elif bouton_online.collidepoint(event.pos):
                    return "online"
                elif bouton_quitter.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

def jeu():
    global JOUEUR, contre_ia
    en_cours = True
    while en_cours:
        dessiner_grille()
        dessiner_symboles()

        if not contre_ia:
            message = "X (J1)" if JOUEUR == 1 else "O (J2)"
        else:
            message = "Votre tour" if JOUEUR == 1 else "IA joue..."

        font = pygame.font.SysFont(None, 28)
        texte = font.render(message, True, NOIR)
        SCREEN.blit(texte, (TAILLE//2 - texte.get_width()//2, 270))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and JOUEUR == 1:
                clic_utilisateur(pygame.mouse.get_pos())

        # IA
        if contre_ia and JOUEUR == -1:
            observation = np.array([cell for row in grille for cell in row], dtype=np.float32).reshape(1, -1)
            action, _ = model.predict(observation)
            ligne, col = divmod(int(action), 3)
            if grille[ligne][col] == 0:
                grille[ligne][col] = -1
                JOUEUR *= -1

        # Résultat ?
        resultat = verifier_victoire()
        if resultat is not None:
            if resultat == 1:
                afficher_resultat("X a gagné !")
            elif resultat == -1:
                afficher_resultat("O a gagné !")
            else:
                afficher_resultat("Égalité !")

def main():
    choix = afficher_menu()
    pygame.event.clear()

    if choix in ["ia", "local"]:
        jeu()
    elif choix == "online":
        subprocess.Popen(["python", "client.py"])

if __name__ == "__main__":
    main()
