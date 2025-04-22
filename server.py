import socket
import threading
import pickle
import numpy as np
from stable_baselines3 import DQN
from stable_baselines3 import DQN
model = DQN.load("dqn_tictactoe")
from stable_baselines3 import DQN
model = DQN.load("dqn_tictactoe")

HOST = 'localhost'
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(2)

clients = []
grille = [[0 for _ in range(3)] for _ in range(3)]
JOUEUR = 1

model = DQN.load("dqn_tictactoe")

def check_victory():
    for ligne in grille:
        if sum(ligne) == 3 or sum(ligne) == -3:
            return True
    for col in range(3):
        if sum([grille[i][col] for i in range(3)]) in (3, -3):
            return True
    if (grille[0][0] + grille[1][1] + grille[2][2]) in (3, -3) or (grille[0][2] + grille[1][1] + grille[2][0]) in (3, -3):
        return True
    return False

def handle_client(client_socket, player):
    global JOUEUR
    client_socket.send(pickle.dumps(grille))

    while True:
        try:
            if player == 1:
                move = pickle.loads(client_socket.recv(1024))
                ligne, col = move
                if grille[ligne][col] == 0:
                    grille[ligne][col] = 1
                    JOUEUR *= -1

                    if check_victory():
                        for c in clients:
                            c.send(pickle.dumps("X a gagné !"))
                        break
            else:
                # IA joue
                flat_board = np.array(grille).flatten().astype(np.float32)
                action, _ = model.predict(flat_board, deterministic=True)
                ligne, col = divmod(action, 3)
                if grille[ligne][col] == 0:
                    grille[ligne][col] = -1
                    JOUEUR *= -1

                    if check_victory():
                        for c in clients:
                            c.send(pickle.dumps("O (IA) a gagné !"))
                        break

            for c in clients:
                c.send(pickle.dumps(grille))
        except Exception as e:
            print(f"Erreur: {e}")
            break

    client_socket.close()

print(f"Le serveur écoute sur {HOST}:{PORT}")

while len(clients) < 1:  # Un seul joueur humain
    client_socket, _ = server_socket.accept()
    clients.append(client_socket)
    threading.Thread(target=handle_client, args=(client_socket, 1)).start()
