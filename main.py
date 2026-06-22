from pyray import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450

init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Hello raylib from Python")
set_target_fps(60)

while not window_should_close():
    begin_drawing()
    clear_background(RAYWHITE)
    draw_text("Hello raylib!", 260, 200, 32, DARKGRAY)
    end_drawing()

close_window()