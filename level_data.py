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

    Obstacle(2360, 0, 70, 70, 'triangle'),

    Obstacle(2430, 0, 70, 70, 'square'),
    Obstacle(2500, 0, 70, 70, 'square'),
    Obstacle(2570, 0, 70, 70, 'square'),
    Obstacle(2640, 0, 70, 70, 'square'),

    Obstacle(3270, 0, 70, 70, 'triangle'),
    Obstacle(3340, 0, 70, 70, 'triangle'),


    ##############################################----RAMPE
    Obstacle(4140, 0, 70, 70, 'square'),

    Obstacle(4210, 0, 70, 70, 'triangle'),
    Obstacle(4280, 0, 70, 70, 'triangle'),

    Obstacle(4350, 0, 70, 70, 'square'),
    Obstacle(4350, 70, 70, 70, 'square'),

    Obstacle(4420, 0, 70, 70, 'triangle'),
    Obstacle(4490, 0, 70, 70, 'triangle'),


    Obstacle(4560, 0, 70, 70, 'square'),
    Obstacle(4560, 70, 70, 70, 'square'),
    Obstacle(4560, 140, 70, 70, 'square'),
    ###############################################----RAMPE

    Obstacle(5300, 0, 70, 70, 'square'),
    Obstacle(5370, 0, 70, 70, 'square'),
    Obstacle(5440, 0, 70, 70, 'square'),
    Obstacle(5510, 0, 70, 70, 'square'),
    Obstacle(5510, 70, 70, 70, 'triangle'),
    Obstacle(5580, 0, 70, 70, 'triangle'),

    ###############################################----DOUBLE BLOC
    Obstacle(6000, 0, 70, 70, 'square'),
    Obstacle(6000, 70, 70, 70, 'square'),
    Obstacle(6070, 0, 70, 70, 'square'),
    Obstacle(6070, 70, 70, 70, 'square'),

    Obstacle(6140, 0, 70, 70, 'triangle'),
    Obstacle(6210, 0, 70, 70, 'triangle'),

    Obstacle(6280, 0, 70, 70, 'square'),
    Obstacle(6280, 70, 70, 70, 'square'),
    Obstacle(6350, 0, 70, 70, 'square'),
    Obstacle(6350, 70, 70, 70, 'square'),
    ################################################----DOUBLE BLOC
    Obstacle(6420, 70, 70, 70, 'square'),
    Obstacle(6490, 70, 70, 70, 'square'),
    Obstacle(6560, 70, 70, 70, 'square'),
    Obstacle(6630, 70, 70, 70, 'square'),
    Obstacle(6630, 0, 70, 70, 'square'),
    Obstacle(6700, 0, 70, 70, 'triangle'),
    Obstacle(6770, 0, 70, 70, 'triangle'),


    Obstacle(6900, 0, 70, 70, 'square'),
    Obstacle(6970, 0, 70, 70, 'square'),
    Obstacle(6970, 70, 70, 70, 'square'),
    Obstacle(7040, 0, 70, 70, 'square'),
    Obstacle(7040, 70, 70, 70, 'square'),
    Obstacle(7110, 0, 70, 70, 'square'),

    Obstacle(7540, 0, 70, 70, 'triangle'),
    Obstacle(7610, 0, 70, 70, 'triangle'),
    Obstacle(7680, 0, 70, 70, 'triangle'),
]
