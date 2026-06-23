"""
Sprite sheet loading and rendering (generalized).

A sprite sheet is one texture holding a grid of equally sized frames. This
module is asset-agnostic: callers describe the frame layout and it slices the
sheet into source rectangles and draws individual frames.

Note: the texture is loaded on construction, so a SpriteSheet must be created
AFTER rl.init_window() (raylib needs a GL context to upload textures).
"""

from dataclasses import dataclass, field

import pyray as rl


class SpriteSheet:
    """A texture split into a grid of fixed-size frames."""

    def __init__(
        self,
        path: str,
        frame_width: int,
        frame_height: int,
        frame_count: int,
        columns: int | None = None,
    ) -> None:
        """
        path:        image file to load.
        frame_width / frame_height: size of one frame, in pixels.
        frame_count: total number of frames to expose.
        columns:     frames per row. Defaults to all frames in a single row.
        """
        self.texture = rl.load_texture(path)
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.frame_count = frame_count
        self.columns = columns if columns is not None else frame_count

        # Precompute a source rectangle for every frame.
        self.frames: list[rl.Rectangle] = []
        for i in range(frame_count):
            col = i % self.columns
            row = i // self.columns
            self.frames.append(
                rl.Rectangle(
                    float(col * frame_width),
                    float(row * frame_height),
                    float(frame_width),
                    float(frame_height),
                )
            )

    def draw_frame(
        self,
        index: int,
        x: float,
        y: float,
        scale: float = 1.0,
        tint: rl.Color = rl.WHITE,
    ) -> None:
        """Draw frame `index` with its top-left corner at (x, y)."""
        src = self.frames[index % self.frame_count]
        dst = rl.Rectangle(
            x, y, self.frame_width * scale, self.frame_height * scale
        )
        rl.draw_texture_pro(self.texture, src, dst, rl.Vector2(0, 0), 0.0, tint)

    def unload(self) -> None:
        """Free the GPU texture. Call before closing the window."""
        rl.unload_texture(self.texture)


@dataclass
class AnimatedSprite:
    """Plays through a SpriteSheet's frames at a fixed rate."""

    sheet: SpriteSheet
    fps: float = 10.0
    elapsed: float = 0.0
    frame: int = field(default=0)

    def update(self, dt: float) -> None:
        """Advance the animation timer by `dt` seconds."""
        self.elapsed += dt
        self.frame = int(self.elapsed * self.fps) % self.sheet.frame_count

    def draw(
        self,
        x: float,
        y: float,
        scale: float = 1.0,
        tint: rl.Color = rl.WHITE,
    ) -> None:
        self.sheet.draw_frame(self.frame, x, y, scale, tint)

    def unload(self) -> None:
        self.sheet.unload()
