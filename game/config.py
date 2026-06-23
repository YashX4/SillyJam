"""Global configuration constants.

constants used to adjust window size, timing, etc.
"""

# Render area we draw into, in pixels. This is the size passed to
# init_window, but a tiling compositor may give the actual OS window a
# different size — physics and drawing are all in viewport coordinates.
VIEWPORT_WIDTH = 800
VIEWPORT_HEIGHT = 450
WINDOW_TITLE = "spin to win game"

CELL_SIZE = 32

TARGET_FPS = 60

PHYSICS_HZ = 60
PHYSICS_DT = 1.0 / PHYSICS_HZ

# Guard against the spiral of death:
#  if the window stalls, never try to catch up more than this:
MAX_FRAME_TIME = 0.25
