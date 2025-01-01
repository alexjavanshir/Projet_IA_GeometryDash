from pickle import TRUE
import pygame
import gym
from gym import spaces
import numpy as np
from geometry_dash import Game, GameConfig, Player

class GeometryDashEnv(gym.Env):
    def __init__(self):
        super(GeometryDashEnv, self).__init__()

        self.game = Game()
        self.clock = pygame.time.Clock()

        self.observation_space = spaces.Box( 
            low=np.array([0, 0]),
            high=np.array([8000, 720]),
            dtype=np.float32
        )
        self.action_space = spaces.Discrete(2)  # 0 = rien faire, 1 = sauter

    def step(self, action):
            # Gestion du temps
            self.game.dt = self.clock.tick(GameConfig.FPS) / 1000.0  # Mise à jour du dt
            
            # Gestion des événements Pygame pour éviter le blocage
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            
            # Fait l'action dans le jeu
            if action == 1:
                print("SAUT!")
                self.game.player.handle_jump({pygame.K_SPACE: True}, GameConfig.GROUND_HEIGHT, GameConfig.SCREEN_HEIGHT)

            self.game.player.update_position()
            self.game.scroll_offset -= GameConfig.SCROLL_SPEED * self.game.dt
            self.game.player.apply_gravity(self.game.dt, GameConfig.GROUND_HEIGHT, GameConfig.SCREEN_HEIGHT)
            
            reward = 0
            collision = self.game.check_collisions()

            # Attribuer une récompense
            if collision:
                print("Collision !")
                reward = -100
                done = True
            else:
                print("Pas de collision.")
                reward = 1
                done = False

            state = np.array([self.game.player.pos.y, self.game.player.vertical_velocity], dtype=np.float32)
            print(f"Reward : {reward}")

            return state, reward, done, {}


    def reset(self):
        # Réinitialiser l'état du jeu
        self.game.reset()
        state = np.array([self.game.player.pos.y, self.game.player.vertical_velocity], dtype=np.float32)
        return state


    def render(self, mode="human"):
            """Rendu du jeu"""
            self.game.screen.fill(GameConfig.BG_COLOR)
            self.game.draw_ground()
            self.game.draw_obstacles()
            self.game.player.draw(self.game.screen)
            
            # Afficher des informations de debug
            font = pygame.font.Font(None, 36)
            debug_info = [
                f"Position X: {self.game.player.pos.x-self.game.scroll_offset:.1f}",
                f"Position Y: {self.game.player.pos.y:.1f}",
                f"Vitesse: {self.game.player.vertical_velocity:.1f}",
                f"Scroll: {self.game.scroll_offset:.1f}"
            ]
            
            for i, text in enumerate(debug_info):
                text_surface = font.render(text, True, (255, 255, 255))
                self.game.screen.blit(text_surface, (10, 10 + i * 30))
            
            pygame.display.flip()

    def close(self):
        #Ferme Pygame correctement lorsque l'environnement est terminé.
        pygame.quit()