from dataclasses import dataclass

@dataclass
class Obstacle:
    """Represents an obstacle in the game."""
    x: float
    y: float
    width: int
    height: int
    obstacle_type: str  # 'triangle' or 'square'