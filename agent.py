import datetime
import dis
from math import log
from tracemalloc import start

from matplotlib.pylab import f
from geometry_dash_env import GeometryDashEnv
from dqn import DQN
from experience_replay import ReplayBuffer
import random
import torch
import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from datetime import timedelta
import argparse


#Création d'un dossier pour stocker les données des runs#

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

RUNS_DIR = "runs"
os.makedirs(RUNS_DIR, exist_ok=True)

matplotlib.use("Agg")

#########################################################

class Agent:
    def __init__(self, hyperparameter_set="default_run"):
        self.replay_buffer_size = 100000
        self.mini_batch_size = 32
        self.epsilon_init = 1
        self.epsilon_decay = 0.99995#0.9995
        self.epsilon_min = 0.01#0.05
        self.network_sync_rate = 20#10
        self.learning_rate_a = 0.0001
        self.discount_factor_g = 0.99
        self.stop_on_score = 100000
        self.fc1_nodes = 512
        self.env_make_params = {"use_lidar": False} #{"width": 8000, "height": 720}

        self.loss_fn = torch.nn.MSELoss()
        self.optimizer = None

        self.hyperparameter_set = hyperparameter_set
        self.LOG_FILE = os.path.join(RUNS_DIR, f"{self.hyperparameter_set}.log") 
        self.MODEL_FILE = os.path.join(RUNS_DIR, f"{self.hyperparameter_set}.pt")
        self.GRAPH_FILE = os.path.join(RUNS_DIR, f"{self.hyperparameter_set}.png")



    def train_ai(self, is_training=True):
        env = GeometryDashEnv()
        total_episode = 1000
        num_states = env.observation_space.shape[0]
        num_actions = env.action_space.n
        rewards_per_episode = []

        policy_dqn = DQN(num_states, num_actions, self.fc1_nodes)  # Création du model DQN

        if is_training:
            start_time = datetime.datetime.now()

            log_message = f"{start_time.strftime(DATE_FORMAT)} : Debut de l'entrainement...\n"
            print(log_message)
            with open(self.LOG_FILE, "a") as log_file:
                log_file.write(log_message)

            replay_buffer = ReplayBuffer(self.replay_buffer_size)

            epsilon = self.epsilon_init

            target_dqn = DQN(num_states, num_actions, self.fc1_nodes)  # Création du model DQN target
            target_dqn.load_state_dict(policy_dqn.state_dict())  # Copier les parametres du model policy_dqn dans target_dqn
            step_counter = 0

            self.optimizer = torch.optim.Adam(policy_dqn.parameters(), lr=self.learning_rate_a)

            
            best_score = -9999999
        else:
            # Charger le model deja entrainé
            policy_dqn.load_state_dict(torch.load(self.MODEL_FILE))
            policy_dqn.eval()

        epsilon_history = []
        # Boucle principale
        for episode in range(1, total_episode + 1):
            state = env.reset()  # Réinitialise l'environnement
            state = torch.tensor(state, dtype=torch.float32)
            done = False
            score = 0
            #epsilon_history = []

            print(f"--- Épisode {episode} ---")

            while(not done):# and score < self.stop_on_score):
                    
                if is_training and random.random() < epsilon:
                    action = env.action_space.sample()
                    action = torch.tensor(action, dtype=torch.int64)
                else:
                    with torch.no_grad(): #etre sur que pytorch ne fasse pas de calcul de gradient, juste le max
                        action = policy_dqn(state.unsqueeze(dim=0)).squeeze().argmax() #ajoute une dimension pour passer a 2

                # Avancer d'une étape
                next_state, reward, done, _ = env.step(action.item())

                score += reward
                
                next_state = torch.tensor(next_state, dtype=torch.float32)
                reward = torch.tensor(reward, dtype=torch.float32)

                if is_training:
                    replay_buffer.append((state, action, next_state, score, done))

                    step_counter += 1 

                state = next_state
                env.render(episode, total_episode)
            
            rewards_per_episode.append(score)

            if is_training:
                if score > best_score:
                    log_message = f"{datetime.datetime.now().strftime(DATE_FORMAT)}: Nouveau meilleur score {score:0.1f} ({((score - best_score) / best_score) * 100:+0.1f}%) a l'episode {episode}, sauvegarder le model..."
                    print(log_message)
                    with open(self.LOG_FILE, "a") as f:
                        f.write(log_message + "\n")
                    torch.save(policy_dqn.state_dict(), self.MODEL_FILE)
                    best_score = score

                    self.save_graph(rewards_per_episode, epsilon_history)

                print(f"Score de l'épisode {episode} : {score}\n")
                epsilon = max(epsilon * self.epsilon_decay, self.epsilon_min) #baisser epsilon en le multilpliant par 0.9995
                epsilon_history.append(epsilon)

                if len(replay_buffer) >= self.mini_batch_size:
                    mini_batch = replay_buffer.sample(self.mini_batch_size)
                    self.optimise(mini_batch,policy_dqn, target_dqn)

                    epsilon = max(epsilon * self.epsilon_decay, self.epsilon_min)
                    epsilon_history.append(epsilon)

                    if step_counter > self.network_sync_rate:
                        target_dqn.load_state_dict(policy_dqn.state_dict())
                        step_counter = 0

            self.save_graph(rewards_per_episode, epsilon_history)


        env.close()

    def save_graph(self, rewards_per_episode, epsilon_history):
        """Sauvegarde du graphe de l'evolution des rewards et de l'evolution de l'epsilon."""
        fig = plt.figure(1)
        mean_rewards = np.zeros(len(rewards_per_episode))
        for x in range(len(mean_rewards)):
            mean_rewards[x] = np.mean(rewards_per_episode[max(0, x-99):(x+1)])
        
        plt.subplot(121)
        plt.ylabel('Mean Rewards')
        plt.plot(mean_rewards)

        plt.subplot(122)
    
        plt.ylabel('Epsilon Decay')
        plt.plot(epsilon_history)

        plt.subplots_adjust(wspace=1.0, hspace=1.0)

        fig.savefig(self.GRAPH_FILE)
        plt.close(fig)

        
    def optimise(self, mini_batch, policy_dqn, target_dqn):
        """Mise à jour des poids du model policy_dqn en utilisant un mini-batch de transitions."""
        states, actions, new_states, rewards, terminations = zip(*mini_batch)

        states = torch.stack(states)

        actions = torch.stack(actions)

        new_states = torch.stack(new_states)

        rewards = torch.tensor(rewards, dtype=torch.float32)
        terminations = torch.tensor(terminations, dtype=torch.float32)

        with torch.no_grad():
            target_q = rewards + (1 - terminations)* self.discount_factor_g * target_dqn(new_states).max(dim=1)[0]
        

        current_g = policy_dqn(states).gather(dim=1, index=actions.unsqueeze(dim=1)).squeeze()

        loss = self.loss_fn(current_g, target_q)    

        #optimisation du model
        self.optimizer.zero_grad() #supprime le gradient
        loss.backward() #calcule le gradient
        self.optimizer.step() #mise à jour


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train or test model.')
    parser.add_argument('hyperparameters', help='')
    parser.add_argument('--train', help='Training mode', action='store_true')
    args = parser.parse_args()

    dql = Agent(args.hyperparameters)

    if args.train:
        dql.train_ai(is_training=True)
    else:
        dql.train_ai(is_training=False)
