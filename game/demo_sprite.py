"""
Test wrapper for the example sheet at test.png.

This is the asset-specific glue: it knows test.png is one row of 5 frames,
32x32 each, and hands that layout to the generalized SpriteSheet loader.
Use it as a template for real game sprites later.
"""

from game.spritesheet import AnimatedSprite, SpriteSheet

TEST_SHEET_PATH = "test.png"
TEST_FRAME_SIZE = 32
TEST_FRAME_COUNT = 5


def load_demo_sprite(fps: float = 10.0) -> AnimatedSprite:
    """Load test.png as an animated sprite. Call after rl.init_window()."""
    sheet = SpriteSheet(
        TEST_SHEET_PATH,
        frame_width=TEST_FRAME_SIZE,
        frame_height=TEST_FRAME_SIZE,
        frame_count=TEST_FRAME_COUNT,
    )
    return AnimatedSprite(sheet, fps=fps)
