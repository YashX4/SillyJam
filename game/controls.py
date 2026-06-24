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
    handle_mouse_move(gridstate)
    handle_mouse_click(gridstate)
    if rl.is_key_pressed(rl.KeyboardKey.KEY_P):
        gridstate.show_grid = not gridstate.show_grid
    if rl.is_key_pressed(rl.KeyboardKey.KEY_C):
        res = grid.connected_neighbors(gridstate, gridstate.curr_hovered_cell)
        print("connected_neighbors = ", res)
        
def handle_mouse_click(gridstate: GridState) -> None:
    """Cycle the clicked cell's pipe sprite to the next frame in the enum."""
    if not rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_LEFT):
        return

    cell = gridstate.curr_hovered_cell
    if not (0 <= cell.x < GRID_COLS and 0 <= cell.y < GRID_ROWS):
        return

    current_pipe = gridstate.grid[cell.y][cell.x].pipe
    next_pipe: PipeSprite = current_pipe.next()
    
    gridstate.set_pipe(cell.x, cell.y, next_pipe)

def handle_mouse_move(gridstate: GridState) -> None:
    """Update the state.x and state.y based on the mouse position."""
    
    mouse_pos = rl.get_mouse_position()
    cell = grid.pixel_to_cell(mouse_pos.x, mouse_pos.y)
    gridstate.curr_hovered_cell = cell