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
        draw_sources(state)
        draw_flow(state)

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
            # Cells with flow use the water-filled variant of the same frame.
            sheet = state.pipe_sheet
            if cell.has_flow and state.water_pipe_sheet is not None:
                sheet = state.water_pipe_sheet
            if sheet is not None:
                sheet.draw_frame(cell.pipe, x, y)


def draw_sources(state: GameState) -> None:
    """Draw a small blue square in each source cell (debug overlay)."""
    SQUARE_SIZE = CELL_SIZE // 4
    offset = (CELL_SIZE - SQUARE_SIZE) // 2
    for row_num, row in enumerate(state.grid_state.grid):
        for col_num, cell in enumerate(row):
            if not cell.is_source:
                continue
            x, y = grid.cell_coords_to_top_left_pixel(col_num, row_num)
            rl.draw_rectangle(x + offset, y + offset, SQUARE_SIZE, SQUARE_SIZE, rl.BLUE)


def draw_flow(state: GameState) -> None:
    """Draw a small green square in each cell that has flow (debug overlay)."""
    SQUARE_SIZE = CELL_SIZE // 4
    offset = CELL_SIZE // 8
    for row_num, row in enumerate(state.grid_state.grid):
        for col_num, cell in enumerate(row):
            if not cell.has_flow:
                continue
            x, y = grid.cell_coords_to_top_left_pixel(col_num, row_num)
            rl.draw_rectangle(x + offset, y + offset, SQUARE_SIZE, SQUARE_SIZE, rl.GREEN)


def draw_grid() -> None:
    """Draw the CELL_SIZE overlay grid across the whole screen."""
    for x in range(0, VIEWPORT_WIDTH + 1, CELL_SIZE):
        rl.draw_line(x, 0, x, VIEWPORT_HEIGHT, rl.LIGHTGRAY)
    for y in range(0, VIEWPORT_HEIGHT + 1, CELL_SIZE):
        rl.draw_line(0, y, VIEWPORT_WIDTH, y, rl.LIGHTGRAY)
