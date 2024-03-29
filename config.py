import arcade

# Window
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Virus Run"
FONT = "assets/fonts/ARCADECLASSIC.ttf"

# Assets
OBSTACLE_SPRITE = "assets/sprites/pylon.png"
GROUND_SPRITE = "assets/sprites/ground.png"
PLAYER_SPRITE = "assets/sprites/player.png"
ROCKET_SPRITE = "assets/sprites/Rocket.png"
PLAYER_DUCK = "assets/sprites/playerduck.png"
PLAYER_JUMP = "assets/sprites/playerjump.png"

CORRECT_SFX = "assets/sounds/correct.mp3"
WRONG_SFX = "assets/sounds/wrong.mp3"
MUSIC = "assets/sounds/music.mp3"

# Scaling
CHARACTER_SCALING = 2
TILE_SCALING = 0.5
OBSTACLE_SCALING = 1.75
ROCKET_SCALING = 2.5

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
