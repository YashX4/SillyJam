"""
Bottom-of-screen dialog box with an animated ballbot speaker.

While a dialog is active the player can only advance/close it (Next button or
any key) — grid interaction is blocked by the caller. Layout constants live
here so the draw code and the click hit-test stay in sync.
"""

from dataclasses import dataclass, field

import pyray as rl

from game.sprite_data.ballbot import BALLBOT_FRAME_WIDTH, BALLBOT_FRAME_HEIGHT

# --- Fixed layout pieces (screen-size independent) ------------------------
MARGIN = 16
BOX_HEIGHT = 120

BALLBOT_SCALE = 3.0
BALLBOT_W = int(BALLBOT_FRAME_WIDTH * BALLBOT_SCALE)
BALLBOT_H = int(BALLBOT_FRAME_HEIGHT * BALLBOT_SCALE)
BALLBOT_X = MARGIN

TEXT_PADDING = 14
TEXT_FONT_SIZE = 18

NEXT_BTN_W = 90
NEXT_BTN_H = 30


@dataclass(frozen=True)
class DialogLayout:
    """Screen-size-dependent positions, recomputed each frame.

    The dialog anchors to the bottom edge of the *current* window (which may be
    larger than the design viewport), so it must be derived from the live
    screen size rather than baked-in viewport constants.
    """

    box_x: int
    box_y: int
    box_w: int
    box_h: int
    ballbot_x: int
    ballbot_y: int
    next_btn_x: int
    next_btn_y: int


def compute_layout() -> DialogLayout:
    """Lay the dialog out against the current window dimensions."""
    screen_w = rl.get_screen_width()
    screen_h = rl.get_screen_height()

    box_y = screen_h - BOX_HEIGHT - MARGIN
    box_x = MARGIN + BALLBOT_W + 12
    box_w = screen_w - box_x - MARGIN
    return DialogLayout(
        box_x=box_x,
        box_y=box_y,
        box_w=box_w,
        box_h=BOX_HEIGHT,
        ballbot_x=BALLBOT_X,
        # Sit the ballbot on the bottom edge of the dialog box.
        ballbot_y=box_y + BOX_HEIGHT - BALLBOT_H,
        next_btn_x=box_x + box_w - NEXT_BTN_W - 12,
        next_btn_y=box_y + BOX_HEIGHT - NEXT_BTN_H - 12,
    )


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

    def advance(self) -> bool:
        """Move to the next sentence, or close the dialog if past the end.

        Returns True if a new sentence is now showing, False if the dialog
        just closed (so callers can play the talk blip only on a real advance).
        """
        self.index += 1
        if self.index >= len(self.sentences):
            self.active = False
            self.index = 0
            return False
        return True


def _point_in_next_button(pos: rl.Vector2, layout: DialogLayout) -> bool:
    return (
        layout.next_btn_x <= pos.x <= layout.next_btn_x + NEXT_BTN_W
        and layout.next_btn_y <= pos.y <= layout.next_btn_y + NEXT_BTN_H
    )


def handle_dialog_input(dialog: DialogState, ignore_keys: tuple[int, ...] = ()) -> bool:
    """Advance the dialog on a Next-button click or any key press.

    `ignore_keys` are skipped so the key that opened the dialog this frame does
    not also advance it.

    Returns True when the input advanced the dialog to a new sentence (so the
    caller can play the talk blip), False otherwise.
    """
    advance = False

    # Any key advances. Drain the key queue so we catch every press this frame.
    key = rl.get_key_pressed()
    while key != 0:
        if key not in ignore_keys:
            advance = True
        key = rl.get_key_pressed()

    if rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_LEFT):
        if _point_in_next_button(rl.get_mouse_position(), compute_layout()):
            advance = True

    if advance:
        return dialog.advance()
    return False
