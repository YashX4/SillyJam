"""Main game loop.

Runs a fixed timestep with a variable rate render:    
"""

import asyncio
import os

import pyray as rl

from game import controls, dialog, draw, menu, physics
from game.menu import MenuAction
from game.sprite_data import ballbot, boiler, demo_sprite, parallax, pipes
from game.config import (
    MAX_FRAME_TIME,
    PHYSICS_DT,
    VIEWPORT_HEIGHT,
    VIEWPORT_WIDTH,
    TARGET_FPS,
    WINDOW_TITLE,
)
from game.state import GameState, Scene


async def run() -> None:
    # Force GLFW onto its X11 backend (via XWayland). The pyray wheel ships both
    os.environ.pop("WAYLAND_DISPLAY", None)

    rl.init_window(VIEWPORT_WIDTH, VIEWPORT_HEIGHT, WINDOW_TITLE)
    rl.set_target_fps(TARGET_FPS)

    state = GameState()
    state.background = parallax.load_background()
    state.sprite = demo_sprite.load_demo_sprite()
    state.pipe_sheet = pipes.load_pipe_sheet()
    state.water_pipe_sheet = pipes.load_water_pipe_sheet()
    state.ballbot = ballbot.load_ballbot()
    state.pump_sprite = pipes.load_pump_pipe_sprite()
    state.boiler_sprite = boiler.load_boiler_sprite()
    dt_accumulator = 0.0

    # Test dialogs (see prompt): "[" opens a 3-sentence one, "]" a simple one.
    TEST_DIALOG_LONG = [
        "Hello! I'm ballbot, here to show you the ropes.",
        "Click pipes to place them and route water from the sources.",
        "Press the Next button or any key to dismiss me. Good luck!",
    ]
    TEST_DIALOG_SHORT = ["This is a quick test message."]
    DIALOG_OPEN_KEYS = (
        rl.KeyboardKey.KEY_LEFT_BRACKET,
        rl.KeyboardKey.KEY_RIGHT_BRACKET,
    )

    while not rl.window_should_close():

        if state.scene is Scene.MENU:
            action = menu.handle_menu_input()
            if action is MenuAction.NEW_GAME:
                state.scene = Scene.PLAYING
            elif action is MenuAction.EXIT:
                break
            # LOAD_GAME and SETTINGS are not wired up yet.

            menu.draw_menu()
            await asyncio.sleep(0)
            continue

        # Open the test dialogs (allowed even while one is showing).
        if rl.is_key_pressed(rl.KeyboardKey.KEY_LEFT_BRACKET):
            state.dialog.open(TEST_DIALOG_LONG)
        if rl.is_key_pressed(rl.KeyboardKey.KEY_RIGHT_BRACKET):
            state.dialog.open(TEST_DIALOG_SHORT)

        if state.dialog.active:
            # Dialog is modal: only advancing input, no grid interaction.
            dialog.handle_dialog_input(state.dialog, ignore_keys=DIALOG_OPEN_KEYS)
            if state.ballbot is not None:
                state.ballbot.update(rl.get_frame_time())
        else:
            controls.handle_input(state)

        state.sprite.update(rl.get_frame_time())
        if state.pump_sprite is not None:
            state.pump_sprite.update(rl.get_frame_time())
        if state.boiler_sprite is not None:
            state.boiler_sprite.update(rl.get_frame_time())

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
    if state.background is not None:
        state.background.unload()
    state.pipe_sheet.unload()
    state.water_pipe_sheet.unload()
    if state.ballbot is not None:
        state.ballbot.unload()
    if state.pump_sprite is not None:
        state.pump_sprite.unload()
    if state.boiler_sprite is not None:
        state.boiler_sprite.unload()
    rl.close_window()
