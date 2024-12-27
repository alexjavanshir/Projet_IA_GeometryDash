from dataclasses import dataclass

@dataclass
class Obstacle:
    """Represents an obstacle in the game."""
    x: float
    y: float
    width: int
    height: int
    obstacle_type: str  # 'triangle' or 'square'


# Define the level layout
level_obstacles = [
    Obstacle(1300, 0, 70, 70, 'triangle'),
    Obstacle(1800, 0, 70, 70, 'triangle'),
    Obstacle(1870, 0, 70, 70, 'triangle'),
    Obstacle(1940, 0, 70, 70, 'triangle'),


    Obstacle(3000, 0, 70, 70, 'square'),
    Obstacle(3000, 70, 70, 70, 'square'),

    
]
