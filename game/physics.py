"""
Physics step.
"""

from time import time

from game import grid
from game.config import VIEWPORT_WIDTH, VIEWPORT_HEIGHT
from game.state import GameState


def step(state: GameState, dt: float) -> None:
    """Advance the game state by one fixed timestep of `dt` seconds."""
    # Snapshot the pre-step position so the renderer can interpolate toward it.
    start_step_time = time()
    
    if state.initial_game_time == 0.0:
        state.initial_game_time = start_step_time

    if start_step_time - state.last_flow_step_time > 0.5:
        grid.compute_flow(state.grid_state)
        state.last_flow_step_time = start_step_time

    # state.prev_x = state.x
    # state.prev_y = state.y

    # state.x += state.move_speed * dt

    # if state.x < 0:
    #     state.x = 0
    #     state.move_speed = -state.move_speed
    # elif state.x > VIEWPORT_WIDTH:
    #     state.x = VIEWPORT_WIDTH
    #     state.move_speed = -state.move_speed