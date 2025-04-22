from stable_baselines3 import DQN

# Charger le modèle entraîné
model = DQN.load("dqn_tictactoe")

print("✅ Le modèle a bien été chargé !")
