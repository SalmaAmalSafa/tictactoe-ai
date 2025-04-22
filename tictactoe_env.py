import gymnasium as gym
from gymnasium import spaces
import numpy as np

class TicTacToeEnv(gym.Env):
    def __init__(self):
        super(TicTacToeEnv, self).__init__()

        # Observation: 9 cases avec des valeurs -1 (O), 0 (vide), ou 1 (X)
        self.observation_space = spaces.Box(low=-1, high=1, shape=(9,), dtype=np.float32)

        # Actions: choisir une case (0 à 8)
        self.action_space = spaces.Discrete(9)

        self.done = False
        self.board = np.zeros(9, dtype=np.float32)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.done = False
        self.board = np.zeros(9, dtype=np.float32)

        if seed is not None:
            np.random.seed(seed)

        return self.board.copy(), {}  # ✅ Le reset retourne un tuple (obs, info)

    def step(self, action):
        if self.done:
            raise ValueError("Le jeu est terminé. Veuillez réinitialiser.")

        if self.board[action] != 0:
            self.done = True
            return self.board.copy(), -10.0, True, False, {}

        self.board[action] = 1  # Joueur (X)

        winner = self.check_winner()
        if winner != 0:
            self.done = True
            return self.board.copy(), float(winner), True, False, {}

        available_moves = np.where(self.board == 0)[0]
        if len(available_moves) > 0:
            ai_move = np.random.choice(available_moves)
            self.board[ai_move] = -1

            winner = self.check_winner()
            if winner != 0:
                self.done = True
                return self.board.copy(), float(winner), True, False, {}

        if np.all(self.board != 0):
            self.done = True
            return self.board.copy(), 0.0, True, False, {}

        return self.board.copy(), 0.0, False, False, {}

    def render(self):
        symbols = {1: 'X', -1: 'O', 0: ' '}
        board_display = [symbols[int(i)] for i in self.board]
        for i in range(0, 9, 3):
            print('|'.join(board_display[i:i+3]))
            if i < 6:
                print('-' * 5)
        print()

    def check_winner(self):
        b = self.board.reshape(3, 3)
        for i in range(3):
            if np.all(b[i, :] == 1) or np.all(b[:, i] == 1):
                return 1
            if np.all(b[i, :] == -1) or np.all(b[:, i] == -1):
                return -1
        if np.all(np.diag(b) == 1) or np.all(np.diag(np.fliplr(b)) == 1):
            return 1
        if np.all(np.diag(b) == -1) or np.all(np.diag(np.fliplr(b)) == -1):
            return -1
        return 0
