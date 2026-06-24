import pyray as rl

from game import grid
from game.config import CELL_SIZE, VIEWPORT_WIDTH, VIEWPORT_HEIGHT
from game.state import GameState
from game.types import PipeSprite


def draw(state: GameState, alpha: float) -> None:
    rl.begin_drawing()
    rl.clear_background(rl.RAYWHITE)

    if state.pipe_sheet is not None:
        draw_pipes(state)

    if state.sprite is not None:
        sprite_x = 40
        sprite_y = 40
        state.sprite.draw(sprite_x, sprite_y)


    if state.grid_state.show_grid:
        mpos = rl.get_mouse_position()
        hover_cell = state.grid_state.get_hover_cell(mpos.x, mpos.y)
        xPos, yPos = grid.cell_to_px(hover_cell)
        rl.draw_circle(int(xPos), int(yPos), 20, rl.RED)
        draw_grid()

    FPS_TEXT_POS_X = VIEWPORT_WIDTH - 90
    FPS_TEXT_POS_Y = 10
    rl.draw_fps(FPS_TEXT_POS_X, FPS_TEXT_POS_Y)
    rl.end_drawing()


def draw_pipes(state: GameState) -> None:
    """Draw each cell's pipe sprite."""
    for  row_num, row in enumerate(state.grid_state.grid):
        for col_num, cell in enumerate(row):
            if cell.pipe is PipeSprite.AIR:
                continue
            x, y = grid.cell_coords_to_top_left_pixel(col_num, row_num)
            if state.pipe_sheet is not None:
                state.pipe_sheet.draw_frame(cell.pipe, x, y)


def draw_grid() -> None:
    """Draw the CELL_SIZE overlay grid across the whole screen."""
    for x in range(0, VIEWPORT_WIDTH + 1, CELL_SIZE):
        rl.draw_line(x, 0, x, VIEWPORT_HEIGHT, rl.LIGHTGRAY)
    for y in range(0, VIEWPORT_HEIGHT + 1, CELL_SIZE):
        rl.draw_line(0, y, VIEWPORT_WIDTH, y, rl.LIGHTGRAY)
