"""
Mutable game state.
- set by physics loop
- read by draw loop 
"""

from dataclasses import dataclass
from game.spritesheet import AnimatedSprite

@dataclass
class GameState:
    some_increase_speed: float = 150.0
    x: float = 400.0
    y: float = 225.0
    show_grid: bool = False

    # Loaded after init_window (needs a GL context), so it starts as None.
    sprite: AnimatedSprite | None = None
    