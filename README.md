# Projet DRL Tic Tac Toe en Ligne

> Projet réalisé dans le cadre du module **Fondements des Réseaux**, École Supérieure d’Économie Numérique, Université de la Manouba  
> **Année universitaire :** 2024-2025  
> **Réalisé par :** Safa Smati , Amal Hammami et Salma Benmahmoud
> **Encadrant :** Dhraief Amine

---

## Objectif

Ce projet consiste à développer un jeu Tic Tac Toe (morpion) en **Python**, jouable :
- **Localement à 2 joueurs**
- **Contre une intelligence artificielle (IA) entraînée par apprentissage par renforcement profond - DRL**
- **En ligne contre un autre joueur via sockets réseau**

Il a pour but de combiner des compétences en **programmation réseau**, **intelligence artificielle**, et **interfaces graphiques**.

---

##  Modes de jeu

-  **Joueur vs Joueur local** : Deux joueurs jouent sur le même écran.
-  **Joueur vs IA (DRL)** : L’IA joue avec un modèle entraîné avec Stable-Baselines3 (DQN).
-  **Joueur vs Joueur en ligne** : Chaque joueur se connecte au serveur via socket.

---

##  Technologies utilisées

| Composant         | Outils/Librairies                     |
|-------------------|---------------------------------------|
| Interface         | `pygame`                              |
| IA (DRL)          | `stable-baselines3`, `gymnasium`      |
| Réseau            | `socket` (TCP client/serveur)         |
| Modèle IA         | `DQN` (Deep Q-Learning Network)       |
| Entraînement      | `train.py` sur environnement custom   |

---

## Installation & Lancement

### 1. Cloner le dépôt
```bash
git clone https://github.com/<ton-utilisateur>/tic-tac-toe-drl.git
cd tic-tac-toe-drl
