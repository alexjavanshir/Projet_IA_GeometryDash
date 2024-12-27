import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
import pygame
from dataclasses import dataclass
from typing import List, Tuple
from level_data import level_obstacles

#from level_test import level_obstacles


class GameConfig:
    """Centralized game configuration."""
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    FPS = 60
    BG_COLOR = "#2117d4"
    GROUND_COLOR = "#0a047a"
    GROUND_HEIGHT = 200

    # Physics constants
    GRAVITY =3000
    PLAYER_SPEED = 300
    JUMP_FORCE = 1000
    SCROLL_SPEED = 500
    ROTATION_SPEED = -127

@dataclass
class Obstacle:
    """Represents an obstacle in the game."""
    x: float
    y: float
    width: int
    height: int
    obstacle_type: str  # 'triangle' or 'square'

class Player:
    """Manages player state and behavior."""
    def __init__(self, x: float, y: float):
        """Initialize player with starting position and load image."""
        self.pos = pygame.Vector2(x, y)
        self.prev_pos = pygame.Vector2(x, y)
        self.size = (70, 70)
        self.vertical_velocity = 0
        self.is_jumping = False
        self.angle = 0
        self.jump_start_time = 0
        
        # Load and scale player image
        self.image = pygame.image.load(self._get_asset_path("Player.png"))
        self.image = pygame.transform.scale(self.image, self.size)

    def update_position(self):
        """Store previous position before any movement."""
        self.prev_pos = pygame.Vector2(self.pos)

    @staticmethod
    def _get_asset_path(filename: str) -> str:
        """Construct a path to assets, handling different potential paths."""
        # Add multiple potential paths
        possible_paths = [
            os.path.join(os.path.dirname(__file__), "assets", filename),
            os.path.join(r"C:\Users\alexa\Documents\ISEP\Garage\Projet_IA_GD\assets", filename)
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
        raise FileNotFoundError(f"Could not find asset: {filename}")

    def handle_jump(self, keys, ground_height: int, screen_height: int) -> None:
        """Handle player jumping mechanics."""
        if (keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]) and not self.is_jumping:
            self.vertical_velocity = -GameConfig.JUMP_FORCE
            self.is_jumping = True
            self.jump_start_time = pygame.time.get_ticks()

    def apply_gravity(self, dt: float, ground_height: int, screen_height: int) -> None:
        """Apply gravity to player movement."""
        self.vertical_velocity += GameConfig.GRAVITY * dt
        self.pos.y += self.vertical_velocity * dt
        
        # Ground collision
        if self.pos.y + self.size[1] >= screen_height - ground_height:
            self.pos.y = screen_height - ground_height - self.size[1]
            self.vertical_velocity = 0
            self.is_jumping = False

    def rotate(self) -> float:
        """Calculate player rotation during jump."""
        if self.is_jumping:
            elapsed_time = (pygame.time.get_ticks() - self.jump_start_time) / 1000
            return min(elapsed_time * GameConfig.ROTATION_SPEED, 360)
        return 0

    def draw(self, screen: pygame.Surface) -> None:
        """Draw rotated player on screen."""
        rotated_player = pygame.transform.rotate(self.image, self.angle)
        rotated_rect = rotated_player.get_rect(center=(
            self.pos.x + self.size[0] // 2, 
            self.pos.y + self.size[1] // 2
        ))
        screen.blit(rotated_player, rotated_rect.topleft)

class Game:
    """Main game class to manage game state and logic."""
    def __init__(self):
        """Initialize Pygame and game components."""
        pygame.init()
        self.screen = pygame.display.set_mode((GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))
        pygame.display.set_caption("Geometry Dash IA")
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
        
        # Load assets
        self.triangle_image = pygame.image.load(Player._get_asset_path("Spike.png"))
        self.triangle_image = pygame.transform.scale(self.triangle_image, (70, 70))
        
        # Initialize game objects
        self.player = Player(
            100, 
            GameConfig.SCREEN_HEIGHT - GameConfig.GROUND_HEIGHT - 70
        )
        
        #---------------------------CREATION DU NIVEAU---------------------------#

        self.obstacles = level_obstacles

        #---------------------------CREATION DU NIVEAU---------------------------#

        
        # Scrolling
        self.scroll_offset = 0

    def draw_ground(self) -> None:
        """Draw the ground at the bottom of the screen."""
        pygame.draw.rect(
            self.screen, 
            GameConfig.GROUND_COLOR, 
            pygame.Rect(0, GameConfig.SCREEN_HEIGHT - GameConfig.GROUND_HEIGHT, 
                        GameConfig.SCREEN_WIDTH, GameConfig.GROUND_HEIGHT)
        )
        # Dessiner le texte qui suit le joueur
        font = pygame.font.Font(None, 160)  # Police par défaut, taille 36
        text_surface = font.render("IA Geometry Dash", True, (0, 2, 110))  # Texte en rouge
        text_x = 150 #Suivre la position du joueur sur l'axe X
        text_y = GameConfig.SCREEN_HEIGHT - GameConfig.GROUND_HEIGHT + 40  # Position verticale au-dessus du sol
        self.screen.blit(text_surface, (text_x, text_y))

    def draw_obstacles(self) -> None:
        """Draw all obstacles with appropriate rendering."""
        for obstacle in self.obstacles:
            x = self.scroll_offset + obstacle.x
            y = GameConfig.SCREEN_HEIGHT - GameConfig.GROUND_HEIGHT - obstacle.height - obstacle.y  # Inclure obstacle.y
            
            if obstacle.obstacle_type == 'triangle':
                self.screen.blit(self.triangle_image, (x, y))
            elif obstacle.obstacle_type == 'square':
                square_rect = pygame.Rect(x, y, obstacle.width, obstacle.height)
                pygame.draw.rect(self.screen, "black", square_rect)
                pygame.draw.rect(self.screen, "gray", square_rect, width=3)


    def check_collisions(self) -> bool:
        """Check for collisions between player and obstacles using previous position."""
        player_rect = pygame.Rect(self.player.pos.x, self.player.pos.y, *self.player.size)
        prev_player_rect = pygame.Rect(self.player.prev_pos.x, self.player.prev_pos.y, *self.player.size)
        
        for obstacle in self.obstacles:
            obstacle_x = self.scroll_offset + obstacle.x
            obstacle_y = GameConfig.SCREEN_HEIGHT - GameConfig.GROUND_HEIGHT - obstacle.height - obstacle.y
            
            if obstacle.obstacle_type == 'triangle':
                triangle_hitbox = pygame.Rect(
                    obstacle_x + obstacle.width * 0.25,
                    obstacle_y + obstacle.height * 0.25,
                    obstacle.width * 0.5,
                    obstacle.height * 0.75
                )
                if player_rect.colliderect(triangle_hitbox):
                    return True
            elif obstacle.obstacle_type == 'square':
                block_rect = pygame.Rect(obstacle_x, obstacle_y, obstacle.width, obstacle.height)
                if player_rect.colliderect(block_rect):
                    # If player was above the block in previous frame
                    if prev_player_rect.bottom <= block_rect.top + 5:  # 5px tolerance
                        self.player.pos.y = block_rect.top - self.player.size[1]
                        self.player.vertical_velocity = 0
                        self.player.is_jumping = False
                        return False
                    return True
        return False

    def reset(self) -> None:
        """Reset the game to its initial state."""
        self.player.pos = pygame.Vector2(
            100, 
            GameConfig.SCREEN_HEIGHT - GameConfig.GROUND_HEIGHT - 70
        )
        self.player.vertical_velocity = 0
        self.player.is_jumping = False
        self.player.angle = 0
        self.scroll_offset = 0

    def run(self) -> None:
        """Main game loop."""
        while self.running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Clear screen
            self.screen.fill(GameConfig.BG_COLOR)

            # Update game state
            keys = pygame.key.get_pressed()

            #Update Player position
            self.player.update_position()

            # Update scroll and jump
            self.scroll_offset -= GameConfig.SCROLL_SPEED * self.dt
            self.player.handle_jump(keys, GameConfig.GROUND_HEIGHT, GameConfig.SCREEN_HEIGHT)
            self.player.apply_gravity(self.dt, GameConfig.GROUND_HEIGHT, GameConfig.SCREEN_HEIGHT)
            
            # Rotate player
            self.player.angle = self.player.rotate()

            # Check for collisions
            if self.check_collisions():
                self.reset()

            # Draw game elements
            self.draw_ground()
            self.draw_obstacles()
            self.player.draw(self.screen)

            # Update display
            pygame.display.flip()

            # Control frame rate
            self.dt = self.clock.tick(GameConfig.FPS) / 1000

        pygame.quit()

def main():
    """Entry point of the game."""
    game = Game()
    game.run()

if __name__ == "__main__":
    main()