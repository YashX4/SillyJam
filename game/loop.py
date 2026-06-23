"""Main game loop.

Runs a fixed timestep with a variable rate render:    
"""

import asyncio
import os

import pyray as rl

from game import controls, draw, physics
from game.animated_sprites import demo_sprite
from game.config import (
    MAX_FRAME_TIME,
    PHYSICS_DT,
    VIEWPORT_HEIGHT,
    VIEWPORT_WIDTH,
    TARGET_FPS,
    WINDOW_TITLE,
)
from game.state import GameState


async def run() -> None:
    # Force GLFW onto its X11 backend (via XWayland). The pyray wheel ships both
    os.environ.pop("WAYLAND_DISPLAY", None)

    rl.init_window(VIEWPORT_WIDTH, VIEWPORT_HEIGHT, WINDOW_TITLE)
    rl.set_target_fps(TARGET_FPS)

    state = GameState()
    state.sprite = demo_sprite.load_demo_sprite()
    dt_accumulator = 0.0

    while not rl.window_should_close():

        controls.handle_input(state.grid_state)

        state.sprite.update(rl.get_frame_time())

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

    state.sprite.unload()
    rl.close_window()
