"""
Physics step.
"""

from game.config import SCREEN_WIDTH, SCREEN_HEIGHT
from game.state import GameState


def step(state: GameState, dt: float) -> None:
    """Advance the game state by one fixed timestep of `dt` seconds."""
    state.x += state.some_increase_speed * dt

    if state.x < 0:
        state.x = 0
        state.some_increase_speed = -state.some_increase_speed
    elif state.x > SCREEN_WIDTH:
        state.x = SCREEN_WIDTH
        state.some_increase_speed = -state.some_increase_speed