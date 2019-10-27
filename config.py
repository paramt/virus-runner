import arcade

# Window
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Virus Run"
FONT = "assets/fonts/ARCADECLASSIC.ttf"

# Sprites
OBSTACLE_SPRITE = "assets/sprites/pylon.png"
GROUND_SPRITE = "assets/sprites/ground.png"
PLAYER_SPRITE = "assets/sprites/player.png"
PLAYER_DUCK = "assets/sprites/playerduck.png"
PLAYER_JUMP = "assets/sprites/playerjump.png"

CHARACTER_SCALING = 2
TILE_SCALING = 0.5
OBSTACLE_SCALING = 1.75

# Backgrounds
TITLE_IMAGE = "assets/images/title.png"
BACKGROUND_IMAGE = "assets/images/background.png"
HELP_IMAGE = "assets/images/help.png"
CONTROLS_IMAGE = "assets/images/controls.png"

# Movement
SPEED = 500
GRAVITY = 1.5
JUMP_SPEED = 30
STOMP_SPEED = 45
DIFFICULTY = 0 # Initial difficulty (0 - 1)

# Game states
TITLE = 1
HELP = 2
CONTROLS = 2.5
RUNNING = 3
GAMEOVER = 4
