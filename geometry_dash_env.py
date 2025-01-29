import pygame
import gym
from gym import spaces
import numpy as np
from game import Game
from game_config import GameConfig

class GeometryDashEnv(gym.Env):
    def __init__(self):
        super(GeometryDashEnv, self).__init__()

        self.game = Game()
        self.clock = pygame.time.Clock()

        self.observation_space = spaces.Box( 
            low=np.array([0, 0, 0, 0]), #2 ou 4 dimensions?
            high=np.array([8000, 720, 8000, 720]),
            dtype=np.float32
        )
        self.action_space = spaces.Discrete(2)  # 0 = rien faire, 1 = sauter

    import numpy as np

    def step(self, action):
        # Gestion du temps
        self.game.dt = self.clock.tick(GameConfig.FPS) / 1000.0  # Mise à jour du dt

        # Gestion des événements Pygame pour éviter le blocage
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Fait l'action dans le jeu
        if action == 1:
            self.game.player.handle_jump({pygame.K_SPACE: True}, GameConfig.GROUND_HEIGHT, GameConfig.SCREEN_HEIGHT)

        self.game.player.update_position()
        self.game.scroll_offset -= GameConfig.SCROLL_SPEED * self.game.dt
        self.game.player.apply_gravity(self.game.dt, GameConfig.GROUND_HEIGHT, GameConfig.SCREEN_HEIGHT)
        self.game.player.angle = self.game.player.rotate()

        reward = 0
        collision = self.game.check_collisions()

        # Attribuer une récompense
        if collision:
            reward = -150
            done = True
        else:
            reward = 1
            done = False

        # Obtenir les obstacles visibles
        visible_obstacles = self.game.get_visible_obstacles()

        # Si des obstacles sont visibles, trouver celui qui est le plus proche du joueur
        if visible_obstacles:
            # Calculer la distance Euclidienne entre le joueur et chaque obstacle
            for obstacle in visible_obstacles:
                distances = np.sqrt((self.game.player.pos.x - obstacle.x) ** 2 + (self.game.player.pos.y - obstacle.y) ** 2)
         
            # Trouver l'obstacle avec la distance minimale (le plus proche)
            closest_obstacle = visible_obstacles[np.argmin(distances)]
            next_obstacle_pos = np.array([closest_obstacle.x, closest_obstacle.y], dtype=np.float32)
        else:
            next_obstacle_pos = np.array([8000, 720], dtype=np.float32)  # Valeurs par défaut (si aucun obstacle visible)

        # L'état à retourner, incluant la position du joueur et la position de l'obstacle
        state = np.array([self.game.player.pos.x, self.game.player.pos.y, next_obstacle_pos[0], next_obstacle_pos[1]], dtype=np.float32)

        return state, reward, done, {}



    def reset(self):
        # Réinitialiser l'état du jeu
        self.game.reset()
        state = np.array([self.game.player.pos.y, self.game.player.vertical_velocity, 8000, 720], dtype=np.float32)
        return state


    def render(self, episode, total_episode, mode="human"):
            """Rendu du jeu"""
            self.game.screen.fill(GameConfig.BG_COLOR)
            self.game.draw_ground()
            self.game.draw_obstacles()
            self.game.player.draw(self.game.screen)

            
            # Afficher des informations de debug
            font = pygame.font.Font(None, 36)
            debug_info = [
                "<---- Mode IA Activé ---->",
                f"Episode : {episode} / {total_episode}",
                f"Position X: {self.game.player.pos.x-self.game.scroll_offset:.0f}",
                f"Position Y: {450-self.game.player.pos.y:.0f}",
                f"Vitesse: {self.game.player.vertical_velocity:.0f}"
            ]
            
            for i, text in enumerate(debug_info):
                text_surface = font.render(text, True, (255, 255, 255))
                self.game.screen.blit(text_surface, (10, 10 + i * 30))
            
            pygame.display.flip()

    def close(self):
        #Ferme Pygame correctement lorsque l'environnement est terminé.
        pygame.quit()