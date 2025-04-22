from stable_baselines3 import DQN
from stable_baselines3.common.env_checker import check_env
from tictactoe_env import TicTacToeEnv

# ✅ Créer l'environnement
env = TicTacToeEnv()

# ✅ Vérifier s'il est conforme aux standards de stable_baselines3
check_env(env, warn=True)

# ✅ Créer et entraîner le modèle
model = DQN("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10000)

# ✅ Sauvegarder le modèle entraîné
model.save("dqn_tictactoe")

print("✅ Modèle sauvegardé avec succès !")








