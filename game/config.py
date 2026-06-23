"""Global configuration constants.

constants used to adjust window size, timing, etc.
"""

VIEWPORT_WIDTH = 800
VIEWPORT_HEIGHT = 450
WINDOW_TITLE = "spin to win game"

CELL_SIZE = 32
GRID_COLS = VIEWPORT_WIDTH // CELL_SIZE
GRID_ROWS = VIEWPORT_HEIGHT // CELL_SIZE

TARGET_FPS = 60

PHYSICS_HZ = 60
PHYSICS_DT = 1.0 / PHYSICS_HZ

# Guard against the spiral of death:
#  if the window stalls, never try to catch up more than this:
MAX_FRAME_TIME = 0.25
