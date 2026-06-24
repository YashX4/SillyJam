"""
Asset-specific glue + renderer for the layered city-skyline backdrop in
assets/images/Pixel_Art_City_Landscape_V2/.

The pack is a stack of 512px-wide pixel-art layers that overlay one another to
form one 512x405 scene (Sky is the full-canvas back layer; the building/shade
strips are bottom-aligned within it; two tiny clouds float in the sky). The
companion "City Landscape V2 - SpriteList.txt" lists them front-to-back.

We render them as a *parallax* backdrop: each layer scrolls horizontally at its
own fraction of the camera's movement (far layers barely move, near layers move
a lot), giving a sense of depth. Clouds also drift slowly on their own timer.

Everything is drawn in SCREEN space (not through the world camera) so the
backdrop sits behind the grid at a fixed scale regardless of zoom/pan. The
scene is scaled to fill the live window height and tiled to fill its width.

Must be constructed after rl.init_window() (textures need a GL context).
"""

from dataclasses import dataclass, field

import pyray as rl

_DIR = "assets/images/Pixel_Art_City_Landscape_V2"

# The Sky layer is the full canvas, so its height defines the scene height that
# everything else is laid out within and bottom-aligned to. The scene is scaled
# at draw time to fill the live window height (which can be larger than the
# configured viewport, e.g. on a HiDPI or resized window).
SCENE_HEIGHT = 405


@dataclass
class _Layer:
    """One parallax layer: a texture plus how it scrolls and where it sits."""

    texture: rl.Texture
    parallax: float       # fraction of camera.target.x applied as horizontal scroll
    scene_y: float        # y of the layer's top edge within the 405-tall scene
    spacing: float        # horizontal tile spacing, scene px (defaults to width)
    drift: float = 0.0    # extra auto-scroll, scene px/sec (used for clouds)


@dataclass
class ParallaxBackground:
    layers: list[_Layer] = field(default_factory=list)

    def draw(self, camera: rl.Camera2D) -> None:
        """Draw every layer back-to-front, filling the live window."""
        time = rl.get_time()
        screen_w = rl.get_screen_width()
        screen_h = rl.get_screen_height()
        scale = screen_h / SCENE_HEIGHT
        for layer in self.layers:
            _draw_layer(layer, camera.target.x, time, scale, screen_w)

    def unload(self) -> None:
        for layer in self.layers:
            rl.unload_texture(layer.texture)


def _draw_layer(
    layer: _Layer, camera_x: float, time: float, scale: float, screen_w: int
) -> None:
    """Tile one layer across the window at its parallax-shifted offset."""
    tex = layer.texture
    scaled_w = tex.width * scale
    scaled_h = tex.height * scale
    spacing = layer.spacing * scale
    y = layer.scene_y * scale

    # How far this layer has scrolled, in screen pixels. Far layers (small
    # parallax) lag the camera; clouds add a slow constant drift on top.
    scroll = camera_x * layer.parallax + time * layer.drift * scale
    # Wrap into [0, spacing) and start one tile to the left so the seam is
    # always off-screen.
    start_x = -(scroll % spacing) - spacing

    src = rl.Rectangle(0.0, 0.0, float(tex.width), float(tex.height))
    x = start_x
    while x < screen_w:
        dst = rl.Rectangle(x, y, scaled_w, scaled_h)
        rl.draw_texture_pro(tex, src, dst, rl.Vector2(0, 0), 0.0, rl.WHITE)
        x += spacing


def _bottom_aligned(texture: rl.Texture, parallax: float) -> _Layer:
    """A full-width strip resting on the bottom of the scene (buildings/shade)."""
    return _Layer(
        texture=texture,
        parallax=parallax,
        scene_y=SCENE_HEIGHT - texture.height,
        spacing=float(texture.width),
    )


def _cloud(texture: rl.Texture, parallax: float, scene_y: float, drift: float) -> _Layer:
    """A small cloud spread out across the sky (wide spacing, slow drift)."""
    return _Layer(
        texture=texture,
        parallax=parallax,
        scene_y=scene_y,
        spacing=420.0,  # wide gap so clouds are scattered, not a solid band
        drift=drift,
    )


def load_background() -> ParallaxBackground:
    """Load all skyline layers, ordered back-to-front. Call after init_window()."""

    def tex(name: str) -> rl.Texture:
        return rl.load_texture(f"{_DIR}/{name}")

    # Back (slowest) to front (fastest). Parallax factors increase toward the
    # camera; clouds sit between building rows and drift leftward.
    sky = tex("Sky.png")
    layers = [
        _Layer(sky, parallax=0.05, scene_y=0.0, spacing=float(sky.width)),
        _bottom_aligned(tex("Buildings 4.png"), parallax=0.12),
        _cloud(tex("Tiny Cloud 2.png"), parallax=0.18, scene_y=120.0, drift=-7.0),
        _bottom_aligned(tex("Buildings 3.png"), parallax=0.25),
        _cloud(tex("Tiny Cloud.png"), parallax=0.32, scene_y=70.0, drift=-12.0),
        _bottom_aligned(tex("Shade 3.png"), parallax=0.38),
        _bottom_aligned(tex("Buildings 2.png"), parallax=0.48),
        _bottom_aligned(tex("Shade 2.png"), parallax=0.60),
        _bottom_aligned(tex("Buildings 1.png"), parallax=0.75),
    ]
    return ParallaxBackground(layers)
