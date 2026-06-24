"""Global configuration constants.

constants used to adjust window size, timing, etc.
"""

VIEWPORT_WIDTH = 800
VIEWPORT_HEIGHT = 450
WINDOW_TITLE = "spin to win game"

CELL_SIZE = 32
# The grid is much larger than the viewport; pan/zoom the camera to see it all.
GRID_COLS = 100
GRID_ROWS = 100
WORLD_WIDTH = GRID_COLS * CELL_SIZE
WORLD_HEIGHT = GRID_ROWS * CELL_SIZE

# Camera pan/zoom limits.
CAMERA_PAN_SPEED = 600.0  # pixels per second (in world units, before zoom)
CAMERA_ZOOM_MIN = 0.25
CAMERA_ZOOM_MAX = 4.0
CAMERA_ZOOM_STEP = 0.15

TARGET_FPS = 60

PHYSICS_HZ = 60
PHYSICS_DT = 1.0 / PHYSICS_HZ

# Guard against the spiral of death:
#  if the window stalls, never try to catch up more than this:
MAX_FRAME_TIME = 0.25
