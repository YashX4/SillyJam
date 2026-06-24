"""Start menu shown on launch.

Drawn and polled once per frame while the game is in the MENU scene.
"""

from dataclasses import dataclass
from enum import Enum, auto

import pyray as rl

from game.config import VIEWPORT_WIDTH, VIEWPORT_HEIGHT


class MenuAction(Enum):
    """What the player asked for by clicking a menu button this frame."""

    NONE = auto()
    LOAD_GAME = auto()
    NEW_GAME = auto()
    SETTINGS = auto()
    EXIT = auto()


@dataclass
class Button:
    label: str
    action: MenuAction


BUTTONS = [
    Button("Load Game", MenuAction.LOAD_GAME),
    Button("New Game", MenuAction.NEW_GAME),
    Button("Settings", MenuAction.SETTINGS),
    Button("Exit", MenuAction.EXIT),
]

TITLE = "SPIN TO WIN"
TITLE_SIZE = 40
LABEL_SIZE = 22

BUTTON_WIDTH = 240
BUTTON_HEIGHT = 48
BUTTON_SPACING = 16


def _button_rect(index: int) -> rl.Rectangle:
    """Pixel rectangle for the button at `index`, vertically centred as a block."""
    count = len(BUTTONS)
    block_height = count * BUTTON_HEIGHT + (count - 1) * BUTTON_SPACING
    # Nudge the block down so the title has room above it.
    start_y = (VIEWPORT_HEIGHT - block_height) // 2 + 30
    x = (VIEWPORT_WIDTH - BUTTON_WIDTH) // 2
    y = start_y + index * (BUTTON_HEIGHT + BUTTON_SPACING)
    return rl.Rectangle(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)


def draw_menu() -> None:
    rl.begin_drawing()
    rl.clear_background(rl.RAYWHITE)

    title_width = rl.measure_text(TITLE, TITLE_SIZE)
    rl.draw_text(TITLE, (VIEWPORT_WIDTH - title_width) // 2, 70, TITLE_SIZE, rl.DARKGRAY)

    mouse = rl.get_mouse_position()
    for index, button in enumerate(BUTTONS):
        rect = _button_rect(index)
        hovered = rl.check_collision_point_rec(mouse, rect)
        rl.draw_rectangle_rec(rect, rl.SKYBLUE if hovered else rl.LIGHTGRAY)
        rl.draw_rectangle_lines_ex(rect, 2, rl.DARKGRAY)

        label_width = rl.measure_text(button.label, LABEL_SIZE)
        text_x = int(rect.x + (rect.width - label_width) / 2)
        text_y = int(rect.y + (rect.height - LABEL_SIZE) / 2)
        rl.draw_text(button.label, text_x, text_y, LABEL_SIZE, rl.BLACK)

    rl.end_drawing()


def handle_menu_input() -> MenuAction:
    """Return the action for whichever button was clicked this frame."""
    if not rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_LEFT):
        return MenuAction.NONE

    mouse = rl.get_mouse_position()
    for index, button in enumerate(BUTTONS):
        if rl.check_collision_point_rec(mouse, _button_rect(index)):
            return button.action
    return MenuAction.NONE
