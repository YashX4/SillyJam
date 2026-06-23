import asyncio
from pyray import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
TARGET_FPS = 60
WINDOW_TITLE = "spin to win game"
async def main():
    init_window(SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_TITLE)
    set_target_fps(TARGET_FPS)

    while not window_should_close():
        begin_drawing()
        clear_background(RAYWHITE)
        draw_text("Hello", 300, 200, 32, DARKGRAY)
        end_drawing()

        await asyncio.sleep(0)

    close_window()

asyncio.run(main())