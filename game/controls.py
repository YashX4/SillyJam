"""
Input handling.
polled once per frame (not per physics step)
"""

import pyray as rl

from game import grid
from game.config import GRID_COLS, GRID_ROWS
from game.state import GridState
from game.types import PipeSprite


def handle_input(gridstate: GridState) -> None:
    # handle_mouse_move(gridstate)
    handle_mouse_click(gridstate)
    if rl.is_key_pressed(rl.KeyboardKey.KEY_P):
        gridstate.show_grid = not gridstate.show_grid
    if rl.is_key_pressed(rl.KeyboardKey.KEY_C):
        mouse_pos = rl.get_mouse_position()
        hover_cell = gridstate.get_hover_cell(mouse_pos.x, mouse_pos.y)
        if hover_cell.pipe != PipeSprite.AIR:
            res = grid.connected_neighbors(gridstate, hover_cell)
            print("connected_neighbors = ", res)

def handle_mouse_click(gridstate: GridState) -> None:
    """Cycle the clicked cell's pipe sprite to the next frame in the enum."""
    if not rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_LEFT):
        return

    mouse_pos = rl.get_mouse_position()
    cell = gridstate.get_hover_cell(mouse_pos.x, mouse_pos.y)
    if not (0 <= cell.x < GRID_COLS and 0 <= cell.y < GRID_ROWS):
        return

    current_pipe = gridstate.grid[cell.y][cell.x].pipe
    next_pipe: PipeSprite = current_pipe.next()
    print("setpipe:", next_pipe)
    gridstate.set_pipe(cell.x, cell.y, next_pipe)

def handle_mouse_move(gridstate: GridState) -> None:
    mouse_pos = rl.get_mouse_position()
    pass