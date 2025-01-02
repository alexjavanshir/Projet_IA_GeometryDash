import os
import pygame
from game_config import GameConfig  # Configuration centralisée

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