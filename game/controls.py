"""
Input handling.
polled once per frame (not per physics step)
"""

import pyray as rl

from game.state import GameState


def handle_input(state: GameState) -> None:
    if rl.is_key_pressed(rl.KeyboardKey.KEY_P):
        state.show_grid = not state.show_grid
