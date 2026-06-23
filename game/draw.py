import pyray as rl

from game.config import SCREEN_WIDTH, SCREEN_HEIGHT
from game.state import GameState


def draw(state: GameState, alpha: float) -> None:
    rl.begin_drawing()
    rl.clear_background(rl.RAYWHITE)

    # example draw using physics loop:
    rl.draw_circle(int(state.x), int(state.y), 20, rl.RED)

    FPS_TEXT_POS_X = SCREEN_WIDTH - 90
    FPS_TEXT_POS_Y = 10
    rl.draw_fps(FPS_TEXT_POS_X, FPS_TEXT_POS_Y)
    rl.end_drawing()
