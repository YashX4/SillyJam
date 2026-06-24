"""
Input handling.
polled once per frame (not per physics step)
"""

import pyray as rl

from game import grid
from game.config import (
    CAMERA_PAN_SPEED,
    CAMERA_ZOOM_MAX,
    CAMERA_ZOOM_MIN,
    CAMERA_ZOOM_STEP,
    CELL_SIZE,
    GEAR_FPS_MAX,
    GEAR_FPS_MIN,
    GEAR_FPS_STEP,
    GRID_COLS,
    GRID_ROWS,
)
from game.types import Cell


def center_camera_on_cell(camera: rl.Camera2D, cell: Cell) -> None:
    """Move the camera so that `cell` is centered on screen."""
    px, py = grid.cell_to_px(cell)
    camera.target.x = px + CELL_SIZE / 2
    camera.target.y = py + CELL_SIZE / 2
    camera.offset.x = rl.get_screen_width() / 2
    camera.offset.y = rl.get_screen_height() / 2
from game.state import GameState, GridState
from game.types import PipeSprite


def handle_input(state: GameState) -> None:
    handle_camera(state.camera)

    gridstate = state.grid_state
    handle_mouse_click(gridstate, state.camera)
    if rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_MIDDLE):
        center_camera_on_cell(state.camera, hover_cell(gridstate, state.camera))
    if rl.is_key_pressed(rl.KeyboardKey.KEY_P):
        gridstate.show_grid = not gridstate.show_grid
    if rl.is_key_pressed(rl.KeyboardKey.KEY_SEMICOLON):
        gridstate.show_debug_rect = not gridstate.show_debug_rect
    if rl.is_key_pressed(rl.KeyboardKey.KEY_APOSTROPHE):
        gridstate.show_debug_circle = not gridstate.show_debug_circle
    if rl.is_key_pressed(rl.KeyboardKey.KEY_S):
        cell = hover_cell(gridstate, state.camera)
        gridstate.toggle_source(cell.x, cell.y)
    if rl.is_key_pressed(rl.KeyboardKey.KEY_B):
        cell = hover_cell(gridstate, state.camera)
        gridstate.place_boiler(cell.x, cell.y)
    if rl.is_key_pressed(rl.KeyboardKey.KEY_M):
        cell = hover_cell(gridstate, state.camera)
        gridstate.place_gear(cell.x, cell.y)
    if rl.is_key_pressed(rl.KeyboardKey.KEY_Z):
        adjust_gear_fps(state, -GEAR_FPS_STEP)
    if rl.is_key_pressed(rl.KeyboardKey.KEY_X):
        adjust_gear_fps(state, GEAR_FPS_STEP)
    if rl.is_key_pressed(rl.KeyboardKey.KEY_C):
        hcell = hover_cell(gridstate, state.camera)
        print("hover_cell = ", hcell)
        if hcell.pipe != PipeSprite.AIR:
            res = grid.connected_neighbors(gridstate, hcell)
            print("connected_neighbors = ", res)


def adjust_gear_fps(state: GameState, delta: float) -> None:
    """Change the gear animation rate by `delta` fps (clamped to range) and print it."""
    if state.gear_sprite is None:
        return
    new_fps = state.gear_sprite.fps + delta
    state.gear_sprite.fps = max(GEAR_FPS_MIN, min(GEAR_FPS_MAX, new_fps))
    print("gear fps =", state.gear_sprite.fps)


def mouse_world_pos(camera: rl.Camera2D) -> rl.Vector2:
    """Mouse position converted from screen space into world space."""
    return rl.get_screen_to_world_2d(rl.get_mouse_position(), camera)


def hover_cell(gridstate: GridState, camera: rl.Camera2D):
    """The grid cell currently under the mouse, accounting for the camera."""
    world = mouse_world_pos(camera)
    return gridstate.get_hover_cell(world.x, world.y)


def handle_camera(camera: rl.Camera2D) -> None:
    """Pan with the arrow keys, zoom toward the mouse with the scroll wheel."""
    dt = rl.get_frame_time()
    pan = CAMERA_PAN_SPEED * dt / camera.zoom
    if rl.is_key_down(rl.KeyboardKey.KEY_RIGHT):
        camera.target.x += pan
    if rl.is_key_down(rl.KeyboardKey.KEY_LEFT):
        camera.target.x -= pan
    if rl.is_key_down(rl.KeyboardKey.KEY_DOWN):
        camera.target.y += pan
    if rl.is_key_down(rl.KeyboardKey.KEY_UP):
        camera.target.y -= pan

    wheel = rl.get_mouse_wheel_move()
    if wheel != 0.0:
        # Keep the world point under the cursor fixed while zooming.
        mouse = rl.get_mouse_position()
        before = rl.get_screen_to_world_2d(mouse, camera)
        camera.zoom = max(
            CAMERA_ZOOM_MIN,
            min(CAMERA_ZOOM_MAX, camera.zoom * (1.0 + wheel * CAMERA_ZOOM_STEP)),
        )
        after = rl.get_screen_to_world_2d(mouse, camera)
        camera.target.x += before.x - after.x
        camera.target.y += before.y - after.y
        print(f"zoom: {camera.zoom:.3f}")


def handle_mouse_click(gridstate: GridState, camera: rl.Camera2D) -> None:
    """Cycle the clicked cell's pipe sprite to the next frame in the enum."""
    if not rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_LEFT):
        return

    cell = hover_cell(gridstate, camera)
    if not (0 <= cell.x < GRID_COLS and 0 <= cell.y < GRID_ROWS):
        return

    # Cells under a boiler or gear are reserved; don't place pipes there.
    if gridstate.cell_reserved(cell.x, cell.y):
        return

    current_pipe = gridstate.grid[cell.y][cell.x].pipe
    next_pipe: PipeSprite = current_pipe.next()
    print("setpipe:", next_pipe)
    gridstate.set_pipe(cell.x, cell.y, next_pipe)
