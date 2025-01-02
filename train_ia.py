import random
from geometry_dash_env import GeometryDashEnv

def train_ai():
    env = GeometryDashEnv()
    total_episode = 10

    # Boucle principale
    for episode in range(1, total_episode + 1):
        state = env.reset()  # Réinitialise l'environnement
        done = False
        score = 0

        print(f"--- Épisode {episode} ---")

        while not done:
            action = random.choice([0, 0, 0, 0, 0, 1])  # 0 = pas de saut, 1 = saut

            # Avancer d'une étape
            next_state, reward, done, _ = env.step(action)
            score += reward
            state = next_state
            env.render(episode, total_episode)

        print(f"Score de l'épisode {episode} : {score}\n")

    env.close()

if __name__ == "__main__":
    train_ai()
