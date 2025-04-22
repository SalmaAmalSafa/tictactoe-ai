import socket
import pickle
import pygame
import sys

# Configuration du client
HOST = 'localhost'
PORT = 12345

# Connexion au serveur
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Initialisation de Pygame
pygame.init()
TAILLE = 300
SCREEN = pygame.display.set_mode((TAILLE, TAILLE))
pygame.display.set_caption("Tic Tac Toe")
LIGNE_WIDTH = 5
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)

# Recevoir la grille initiale
grille = pickle.loads(client_socket.recv(1024))

# Dessiner la grille
def dessiner_grille():
    SCREEN.fill(BLANC)
    for i in range(1, 3):
        pygame.draw.line(SCREEN, NOIR, (i*100, 0), (i*100, 300), LIGNE_WIDTH)
        pygame.draw.line(SCREEN, NOIR, (0, i*100), (300, i*100), LIGNE_WIDTH)

# Dessiner les X et O
def dessiner_symboles():
    for ligne in range(3):
        for col in range(3):
            if grille[ligne][col] == 1:
                pygame.draw.line(SCREEN, NOIR, (col*100 + 20, ligne*100 + 20), (col*100 + 80, ligne*100 + 80), 5)
                pygame.draw.line(SCREEN, NOIR, (col*100 + 80, ligne*100 + 20), (col*100 + 20, ligne*100 + 80), 5)
            elif grille[ligne][col] == -1:
                pygame.draw.circle(SCREEN, NOIR, (col*100 + 50, ligne*100 + 50), 35, 5)

# Gérer le clic joueur
def clic_utilisateur(pos):
    ligne = pos[1] // 100
    col = pos[0] // 100
    if grille[ligne][col] == 0:
        client_socket.send(pickle.dumps((ligne, col)))

# Afficher le message de fin
def afficher_resultat(message):
    font = pygame.font.SysFont(None, 40)
    texte = font.render(message, True, NOIR)
    SCREEN.fill(BLANC)
    SCREEN.blit(texte, (TAILLE // 2 - texte.get_width() // 2, 130))
    pygame.display.update()
    pygame.time.wait(3000)

# Boucle principale du jeu
def jeu():
    global grille
    en_cours = True

    while en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clic_utilisateur(pygame.mouse.get_pos())

        dessiner_grille()
        dessiner_symboles()
        pygame.display.update()

        try:
            message = pickle.loads(client_socket.recv(1024))
            if isinstance(message, str):
                afficher_resultat(message)
                en_cours = False
            else:
                grille = message
        except:
            pass

# Point d’entrée du programme
if __name__ == "__main__":
    jeu()


