"""
Virus Runner
by Anmol, Anujan, Justin, Param
"""

import arcade

# Config (window)
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Virus Run"
BG_COLOR = arcade.csscolor.CORNFLOWER_BLUE

# Config (sprites)
CHARACTER_SCALING = 1
TILE_SCALING = 0.5

# Config (player)
SPEED = 500
GRAVITY = 1.2
PLAYER_JUMP_SPEED = 20

# Game states
TITLE = 0
RUNNING = 1
GAMEOVER = 2


class VirusRunner(arcade.Window):
    def __init__(self):
        # Setup the window by initializing the parent class
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(BG_COLOR)

        # Set current state to title screen
        self.current_state = TITLE

        # Initialize sprite lists and the player sprite
        self.ground_list = None
        self.obstacle_list = None
        self.player_list = None
        #self.player_sprite = None

        # Initialize physics engine
        self.physics_engine = None

        # Inialize score at 0
        self.score = 0

    def setup(self):
        # Create the sprite lists
        self.player_list = arcade.SpriteList()
        self.obstacle_list = arcade.SpriteList()
        self.ground_list = arcade.SpriteList()

         # Set up the player
        self.player_sprite = arcade.Sprite("images/player.png", CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 120
        self.player_list.append(self.player_sprite)

        # Create the ground
        for x in range(0, 1450, 64):
            ground = arcade.Sprite("images/grass.png", TILE_SCALING)
            ground.center_x = x
            ground.center_y = 32
            self.ground_list.append(ground)

        # Put some crates on the ground
        coordinate_list = [[1000, 96],
                           [1500, 96],
                           [750, 96]]

        for coordinate in coordinate_list:
            # Add a crate on the ground
            obstacle = arcade.Sprite("images/crate.png", TILE_SCALING)
            obstacle.position = coordinate
            self.obstacle_list.append(obstacle)

        # Create the physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.ground_list, GRAVITY)

    def draw_game(self):
        # Clear the screen to the background color
        arcade.start_render()

        # Draw the sprites
        self.obstacle_list.draw()
        self.ground_list.draw()
        self.player_list.draw()

        # Display score on the screen
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 50, arcade.csscolor.WHITE, 18)

    def draw_game_over(self):
        arcade.draw_text("You lost!", 100, 100, arcade.csscolor.WHITE, 18)
        arcade.draw_text("Press any button to restart", 100, 50, arcade.csscolor.WHITE, 18)

    def draw_title_screen(self):
        pass

    def on_draw(self):
        """ Render the screen """
        if self.current_state == RUNNING:
            self.draw_game()
        elif self.current_state == TITLE:
            self.draw_title_screen()
        elif self.current_state == GAMEOVER:
            self.draw_game()
            self.draw_game_over()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed """

        # Change between game states
        if self.current_state == GAMEOVER:
            self.score = 0
            self.setup()

        self.current_state = RUNNING

        if key == arcade.key.SPACE or key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED

    def update(self, delta_time):
        """ Movement and game logic """
        if self.current_state == RUNNING:
            # Check if any obstacles are hit
            collision = arcade.check_for_collision_with_list(self.player_sprite, self.obstacle_list)

            if collision:
                self.current_state = GAMEOVER

            # Move all the obstacles forward (making it look the like player is moving forward)
            for obstacle in self.obstacle_list:
                # Multiply speed by delta time to make sure that the speed is consitent
                # Otherwise the obstacles will move faster on faster processors and vice versa
                obstacle.center_x -= SPEED * delta_time

                # Remove obstacles that aren't visible anymore (to prevent lag)
                if obstacle.center_x < -25:
                    self.obstacle_list.remove(obstacle)
                    print("Removed obstacle")

            self.score += 1

            # Update all sprites
            self.physics_engine.update()

def main():
    # The main function (called when the program runs)
    window = VirusRunner()
    window.setup()
    arcade.run()

# Entrypoint to the program
if __name__ == "__main__":
    main()
