import pyray as rl

from game.config import CELL_SIZE, VIEWPORT_WIDTH, VIEWPORT_HEIGHT
from game.state import GameState


def draw(state: GameState, alpha: float) -> None:
    rl.begin_drawing()
    rl.clear_background(rl.RAYWHITE)

    # example draw using physics loop:
    rl.draw_circle(int(state.x), int(state.y), 20, rl.RED)

    if state.sprite is not None:
        sprite_x = 40
        sprite_y = 40
        state.sprite.draw(sprite_x, sprite_y, scale=4.0)

    if state.show_grid:
        draw_grid()

    FPS_TEXT_POS_X = VIEWPORT_WIDTH - 90
    FPS_TEXT_POS_Y = 10
    rl.draw_fps(FPS_TEXT_POS_X, FPS_TEXT_POS_Y)
    rl.end_drawing()


def draw_grid() -> None:
    """Draw the CELL_SIZE overlay grid across the whole screen."""
    for x in range(0, VIEWPORT_WIDTH + 1, CELL_SIZE):
        rl.draw_line(x, 0, x, VIEWPORT_HEIGHT, rl.LIGHTGRAY)
    for y in range(0, VIEWPORT_HEIGHT + 1, CELL_SIZE):
        rl.draw_line(0, y, VIEWPORT_WIDTH, y, rl.LIGHTGRAY)
