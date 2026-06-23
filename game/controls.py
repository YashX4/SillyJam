"""
Input handling.
polled once per frame (not per physics step)
"""

import pyray as rl

from game import grid
from game.config import CELL_SIZE
from game.state import GridState


def handle_input(gridstate: GridState) -> None:
    handle_mouse_move(gridstate)
    if rl.is_key_pressed(rl.KeyboardKey.KEY_P):
        gridstate.show_grid = not gridstate.show_grid

def handle_mouse_move(gridstate: GridState) -> None:
    """Update the state.x and state.y based on the mouse position."""
    
    mouse_pos = rl.get_mouse_position()
    cell = grid.pixel_to_cell(mouse_pos.x, mouse_pos.y)
    gridstate.curr_hovered_cell = cell