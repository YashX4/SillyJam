"""
Input handling.
polled once per frame (not per physics step)
"""

import pyray as rl

from game.state import GridState


def handle_input(gridstate: GridState) -> None:
    if rl.is_key_pressed(rl.KeyboardKey.KEY_P):
        gridstate.show_grid = not gridstate.show_grid

def handle_mouse_move(gridstate: GridState) -> None:
    """Update the state.x and state.y based on the mouse position."""
    gridstate.curr_hovered_cell = rl.get_mouse_position()