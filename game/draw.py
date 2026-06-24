import pyray as rl

from game import dialog, grid
from game.config import (
    CELL_SIZE,
    WORLD_WIDTH,
    WORLD_HEIGHT,
)
from game.state import GameState
from game.types import PipeSprite


def draw(state: GameState, alpha: float) -> None:
    rl.begin_drawing()
    rl.clear_background(rl.RAYWHITE)

    # Parallax skyline backdrop, drawn in screen space behind the world.
    if state.background is not None:
        state.background.draw(state.camera)

    # World-space rendering: everything on the grid is drawn through the camera.
    rl.begin_mode_2d(state.camera)

    if state.pipe_sheet is not None:
        draw_pipes(state)

    if state.boiler_sprite is not None:
        draw_boilers(state)

    if state.sprite is not None:
        sprite_x = 40
        sprite_y = 40
        state.sprite.draw(sprite_x, sprite_y)

    if state.grid_state.show_grid:
        world = rl.get_screen_to_world_2d(rl.get_mouse_position(), state.camera)
        hover_cell = state.grid_state.get_hover_cell(world.x, world.y)
        xPos, yPos = grid.cell_to_px(hover_cell)
        rl.draw_circle(int(xPos), int(yPos), 20, rl.RED)
        draw_grid()
        draw_sources(state)
        draw_flow(state)

    rl.end_mode_2d()

    if state.dialog.active:
        draw_dialog(state)

    FPS_TEXT_POS_X = rl.get_screen_width() - 90
    FPS_TEXT_POS_Y = 10
    rl.draw_fps(FPS_TEXT_POS_X, FPS_TEXT_POS_Y)
    rl.end_drawing()


def draw_pipes(state: GameState) -> None:
    """Draw each cell's pipe sprite."""
    for  row_num, row in enumerate(state.grid_state.grid):
        for col_num, cell in enumerate(row):
            x, y = grid.cell_coords_to_top_left_pixel(col_num, row_num)
            if cell.is_source and state.pump_sprite is not None:
                state.pump_sprite.draw(x, y)
                continue
            if cell.pipe is PipeSprite.AIR:
                continue
            # Cells with flow use the water-filled variant of the same frame.
            sheet = state.pipe_sheet
            if cell.has_flow and state.water_pipe_sheet is not None:
                sheet = state.water_pipe_sheet
            if sheet is not None:
                sheet.draw_frame(cell.pipe, x, y)


def draw_boilers(state: GameState) -> None:
    """Draw the animated boiler over its 2x2 footprint at each placed origin."""
    for col, row in state.grid_state.boilers:
        x, y = grid.cell_coords_to_top_left_pixel(col, row)
        # The boiler texture is 64x64 == 2x2 cells, so scale 1.0 fits exactly.
        if state.boiler_sprite is not None:
            state.boiler_sprite.draw(x, y)


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


def _wrap_text(text: str, font_size: int, max_width: int) -> list[str]:
    """Greedy word-wrap `text` to fit within `max_width` pixels per line."""
    lines: list[str] = []
    line = ""
    for word in text.split():
        candidate = word if not line else f"{line} {word}"
        if rl.measure_text(candidate, font_size) <= max_width or not line:
            line = candidate
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_dialog(state: GameState) -> None:
    """Draw the modal bottom dialog: dim overlay, ballbot, text box, Next button."""
    layout = dialog.compute_layout()

    # Dim the rest of the screen to signal it's non-interactive.
    rl.draw_rectangle(
        0, 0, rl.get_screen_width(), rl.get_screen_height(), rl.Color(0, 0, 0, 90)
    )

    # Animated ballbot speaker on the left.
    if state.ballbot is not None:
        state.ballbot.draw(layout.ballbot_x, layout.ballbot_y, scale=dialog.BALLBOT_SCALE)

    # Dialog box.
    rl.draw_rectangle(
        layout.box_x, layout.box_y, layout.box_w, layout.box_h, rl.Color(20, 20, 30, 235)
    )
    rl.draw_rectangle_lines(
        layout.box_x, layout.box_y, layout.box_w, layout.box_h, rl.RAYWHITE
    )

    # Wrapped sentence text.
    text_x = layout.box_x + dialog.TEXT_PADDING
    text_y = layout.box_y + dialog.TEXT_PADDING
    max_text_width = layout.box_w - 2 * dialog.TEXT_PADDING
    line_height = dialog.TEXT_FONT_SIZE + 6
    for i, line in enumerate(_wrap_text(state.dialog.current(), dialog.TEXT_FONT_SIZE, max_text_width)):
        rl.draw_text(line, text_x, text_y + i * line_height, dialog.TEXT_FONT_SIZE, rl.RAYWHITE)

    # Next / Close button.
    mouse = rl.get_mouse_position()
    hovered = (
        layout.next_btn_x <= mouse.x <= layout.next_btn_x + dialog.NEXT_BTN_W
        and layout.next_btn_y <= mouse.y <= layout.next_btn_y + dialog.NEXT_BTN_H
    )
    btn_color = rl.Color(90, 110, 160, 255) if hovered else rl.Color(60, 75, 120, 255)
    rl.draw_rectangle(
        layout.next_btn_x, layout.next_btn_y, dialog.NEXT_BTN_W, dialog.NEXT_BTN_H, btn_color
    )
    rl.draw_rectangle_lines(
        layout.next_btn_x, layout.next_btn_y, dialog.NEXT_BTN_W, dialog.NEXT_BTN_H, rl.RAYWHITE
    )
    label = "Close" if state.dialog.is_last() else "Next"
    label_size = 18
    label_w = rl.measure_text(label, label_size)
    rl.draw_text(
        label,
        layout.next_btn_x + (dialog.NEXT_BTN_W - label_w) // 2,
        layout.next_btn_y + (dialog.NEXT_BTN_H - label_size) // 2,
        label_size,
        rl.RAYWHITE,
    )


def draw_grid() -> None:
    """Draw the CELL_SIZE overlay grid across the whole world."""
    for x in range(0, WORLD_WIDTH + 1, CELL_SIZE):
        rl.draw_line(x, 0, x, WORLD_HEIGHT, rl.LIGHTGRAY)
    for y in range(0, WORLD_HEIGHT + 1, CELL_SIZE):
        rl.draw_line(0, y, WORLD_WIDTH, y, rl.LIGHTGRAY)
