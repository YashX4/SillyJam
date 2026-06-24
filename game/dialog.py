"""
Bottom-of-screen dialog box with an animated ballbot speaker.

While a dialog is active the player can only advance/close it (Next button or
any key) — grid interaction is blocked by the caller. Layout constants live
here so the draw code and the click hit-test stay in sync.
"""

from dataclasses import dataclass, field

import pyray as rl

from game.config import VIEWPORT_WIDTH, VIEWPORT_HEIGHT
from game.sprite_data.ballbot import BALLBOT_FRAME_WIDTH, BALLBOT_FRAME_HEIGHT

# --- Layout (shared by draw + input hit-testing) --------------------------
MARGIN = 16
BOX_HEIGHT = 120
BOX_Y = VIEWPORT_HEIGHT - BOX_HEIGHT - MARGIN

BALLBOT_SCALE = 3.0
BALLBOT_W = int(BALLBOT_FRAME_WIDTH * BALLBOT_SCALE)
BALLBOT_H = int(BALLBOT_FRAME_HEIGHT * BALLBOT_SCALE)
BALLBOT_X = MARGIN
# Sit the ballbot on the bottom edge of the dialog box (left side of screen).
BALLBOT_Y = BOX_Y + BOX_HEIGHT - BALLBOT_H

BOX_X = MARGIN + BALLBOT_W + 12
BOX_W = VIEWPORT_WIDTH - BOX_X - MARGIN

TEXT_PADDING = 14
TEXT_FONT_SIZE = 18

NEXT_BTN_W = 90
NEXT_BTN_H = 30
NEXT_BTN_X = BOX_X + BOX_W - NEXT_BTN_W - 12
NEXT_BTN_Y = BOX_Y + BOX_HEIGHT - NEXT_BTN_H - 12


@dataclass
class DialogState:
    """A sequence of sentences shown one at a time at the bottom of the screen."""

    active: bool = False
    sentences: list[str] = field(default_factory=list)
    index: int = 0

    def open(self, sentences: list[str]) -> None:
        """Start showing `sentences` from the first one."""
        self.sentences = sentences
        self.index = 0
        self.active = bool(sentences)

    def current(self) -> str:
        if 0 <= self.index < len(self.sentences):
            return self.sentences[self.index]
        return ""

    def is_last(self) -> bool:
        return self.index >= len(self.sentences) - 1

    def advance(self) -> None:
        """Move to the next sentence, or close the dialog if past the end."""
        self.index += 1
        if self.index >= len(self.sentences):
            self.active = False
            self.index = 0


def _point_in_next_button(pos: rl.Vector2) -> bool:
    return (
        NEXT_BTN_X <= pos.x <= NEXT_BTN_X + NEXT_BTN_W
        and NEXT_BTN_Y <= pos.y <= NEXT_BTN_Y + NEXT_BTN_H
    )


def handle_dialog_input(dialog: DialogState, ignore_keys: tuple[int, ...] = ()) -> None:
    """Advance the dialog on a Next-button click or any key press.

    `ignore_keys` are skipped so the key that opened the dialog this frame does
    not also advance it.
    """
    advance = False

    # Any key advances. Drain the key queue so we catch every press this frame.
    key = rl.get_key_pressed()
    while key != 0:
        if key not in ignore_keys:
            advance = True
        key = rl.get_key_pressed()

    if rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_LEFT):
        if _point_in_next_button(rl.get_mouse_position()):
            advance = True

    if advance:
        dialog.advance()
