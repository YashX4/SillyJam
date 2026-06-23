"""Main game loop.

Runs a fixed timestep with a variable rate render:    
"""

import asyncio

import pyray as rl

from game import draw, physics
from game.config import (
    MAX_FRAME_TIME,
    PHYSICS_DT,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TARGET_FPS,
    WINDOW_TITLE,
)
from game.state import GameState


async def run() -> None:
    rl.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_TITLE)
    rl.set_target_fps(TARGET_FPS)

    state = GameState()
    dt_accumulator = 0.0

    while not rl.window_should_close():

        # aka avoid spiral of death.
        dt_accumulator += min(rl.get_frame_time(), MAX_FRAME_TIME)

        while dt_accumulator >= PHYSICS_DT:
            physics.step(state, PHYSICS_DT)
            dt_accumulator -= PHYSICS_DT

        # Fraction of the way into the next physics step, for interpolation.
        alpha = dt_accumulator / PHYSICS_DT
        draw.draw(state, alpha)

        # Yield to the event loop (required for the pygbag web build).
        await asyncio.sleep(0)

    rl.close_window()
