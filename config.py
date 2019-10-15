import arcade

# Window
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Virus Run"
BG_COLOR = arcade.csscolor.CORNFLOWER_BLUE

# Sprites
CHARACTER_SCALING = 1
TILE_SCALING = 0.5

# Movement
SPEED = 500
GRAVITY = 1.5
JUMP_SPEED = 25
DIFFICULTY = 0 # Initial difficulty (0 - 1)

# Game states
TITLE = 0
RUNNING = 1
GAMEOVER = 2
