"""
Virus Runner
by Anmol, Anujan, Justin, Param
"""

import math
import random
import arcade
from config import *

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

        # Initialize physics engine
        self.physics_engine = None

        self.key_pressed = False

        # Inialize score at 0
        self.score = 0

    def setup(self):
        # Create the sprite lists
        self.player_list = arcade.SpriteList()
        self.obstacle_list = arcade.SpriteList()
        self.ground_list = arcade.SpriteList()

         # Set up the player
        self.player_sprite = arcade.Sprite(PLAYER_SPRITE, CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 120
        self.player_list.append(self.player_sprite)

        # Create the ground
        for x in range(0, 1450, 64):
            ground = arcade.Sprite(GROUND_SPRITE, TILE_SCALING)
            ground.center_x = x
            ground.center_y = 32
            self.ground_list.append(ground)

        obstacle = arcade.Sprite(OBSTACLE_SPRITE, TILE_SCALING)
        obstacle.position = [random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 100), 96]
        self.obstacle_list.append(obstacle)

        self.num_of_obstacles = 0
        self.difficulty = DIFFICULTY + 0.005

        # Create the physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.ground_list, GRAVITY)

    def draw_game(self):
        # Clear the screen to the background color
        arcade.start_render()

        # Randomly generate obstacles
        obstacle = arcade.Sprite(OBSTACLE_SPRITE, TILE_SCALING)
        obstacle.position = [random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 100), 96]

        try:
            # Check to make sure that there is enough space between obstacles
            gap_exists = obstacle.position[0] - self.obstacle_list[self.num_of_obstacles].position[0] > 300

            if random.random() < self.difficulty and gap_exists:
                self.obstacle_list.append(obstacle)
                self.num_of_obstacles += 1
                self.difficulty += 0.005
        except IndexError:
            self.obstacle_list.append(obstacle)
            self.num_of_obstacles += 1
            self.difficulty += 0.005

        # Draw the sprites
        self.obstacle_list.draw()
        self.ground_list.draw()
        self.player_list.draw()

        # Display score on the screen
        score_text = f"{self.score} hertz"
        arcade.draw_text(score_text, 20, SCREEN_HEIGHT - 50, arcade.csscolor.WHITE, 40, font_name=FONT)

    def draw_game_over(self):
        arcade.draw_text("Game   Over!", 400, 400, arcade.csscolor.WHITE, 100, font_name=FONT)
        arcade.draw_text("Press   any   button   to   restart", 425, 350, arcade.csscolor.WHITE, 30, font_name=FONT)

    def draw_title_screen(self):
        background = arcade.load_texture("assets/sprites/background.png")
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, background)

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

        if key == arcade.key.SPACE or key == arcade.key.UP or key == arcade.key.W:
            self.key_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -JUMP_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.SPACE or key == arcade.key.UP or key == arcade.key.W:
            self.key_pressed = False

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
                obstacle.center_x -= delta_time * (SPEED + math.sqrt(100*self.score))

                # Remove obstacles that aren't visible anymore (to prevent lag)
                if obstacle.center_x < -25:
                    self.obstacle_list.remove(obstacle)
                    self.num_of_obstacles -= 1
                    print("Removed obstacle")

            if self.physics_engine.can_jump() and self.key_pressed:
                self.player_sprite.change_y = JUMP_SPEED

            self.score += 1

            # Update all sprites
            self.physics_engine.update()

def main():
    window = VirusRunner()
    window.setup()
    arcade.run()

# Entrypoint to the program
if __name__ == "__main__":
    main()
