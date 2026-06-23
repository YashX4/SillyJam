import asyncio
import pyray as rl

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
TARGET_FPS = 60
WINDOW_TITLE = "spin to win game"
async def main():
    rl.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_TITLE)
    rl.set_target_fps(TARGET_FPS)

    while not rl.window_should_close():
        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)
        rl.draw_text("Hello", 300, 200, 32, rl.DARKGRAY)
        rl.end_drawing()

        await asyncio.sleep(0)

    rl.close_window()

asyncio.run(main())