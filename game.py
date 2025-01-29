import pygame
from player import Player
from obstacles import Obstacle
from game_config import GameConfig
from level_data import level_obstacles
from typing import List



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
        
        # Creation du niveau
        self.obstacles = level_obstacles


        self.scroll_offset = 0

    def draw_ground(self) -> None:
        """Draw the ground at the bottom of the screen."""
        pygame.draw.rect(
            self.screen, 
            GameConfig.GROUND_COLOR, 
            pygame.Rect(0, GameConfig.SCREEN_HEIGHT - GameConfig.GROUND_HEIGHT, 
                        GameConfig.SCREEN_WIDTH, GameConfig.GROUND_HEIGHT)
        )
        # Texte qui suit le joueur
        font = pygame.font.Font(None, 160)  # Police
        text_surface = font.render("IA Geometry Dash", True, (0, 2, 110))  #Couleur
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

    def get_visible_obstacles(self) -> List[Obstacle]:
        """Filtre les obstacles visibles sur l'écran."""
        visible_obstacles = [
            obstacle for obstacle in self.obstacles
            if 0 <= self.scroll_offset + obstacle.x <= GameConfig.SCREEN_WIDTH
        ]
        return visible_obstacles

    def check_collisions(self) -> bool:
        """Check for collisions between player and obstacles using previous position."""
        visible_obstacles = self.get_visible_obstacles()
        player_rect = pygame.Rect(self.player.pos.x, self.player.pos.y, *self.player.size)
        prev_player_rect = pygame.Rect(self.player.prev_pos.x, self.player.prev_pos.y, *self.player.size)
        
        for obstacle in visible_obstacles:
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