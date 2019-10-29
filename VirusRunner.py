"""
Filename: VirusRunner.py 
Names: Anmol, Anujan, Justin, and Param
Date: October 25, 2019.
Description: This was made to inform users about cybersecurity while having an enjoyable experience playing a game.
This runner game was based off of Google Chrome's dino run and the graphis are inspired by Ridley Scott's Blade Runner film.
The game uses Python Arcade and has 10 multiple choice questions relating to cybersecurity that pop up whenever the user hits an obstacle. 
"""

import csv
import math
import random
import arcade
from config import *

class VirusRunner(arcade.Window):
    def __init__(self):
        # Setup the window by initializing the parent class
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Set current state to title screen
        self.current_state = TITLE

        # Initialize sprite lists and the player sprite
        self.ground_list = None
        self.obstacle_list = None
        self.player_list = None
        self.flying_list = None

        # Initialize physics engine
        self.physics_engine = None

        # Initialize states and other variables
        self.key_pressed = False
        self.waiting_on_input = False
        self.start_zoom = False
        self.scale = 1

        # Inialize score at 0
        self.score = 0
        self.high_score = 0

        # Load sound effects
        self.correct_sound = arcade.load_sound(CORRECT_SFX)
        self.wrong_sound = arcade.load_sound(WRONG_SFX)

        # Play background music
        arcade.play_sound(arcade.load_sound(MUSIC))

    def setup(self):
        # Create the sprite lists
        self.player_list = arcade.SpriteList()
        self.obstacle_list = arcade.SpriteList()
        self.ground_list = arcade.SpriteList()
        self.flying_list = arcade.SpriteList()

         # Set up the player
        self.player_sprite = arcade.Sprite(PLAYER_SPRITE, CHARACTER_SCALING)
        self.player_sprite.center_x = 200
        self.player_sprite.center_y = 120
        self.player_list.append(self.player_sprite)

        self.player_sprite.texture = arcade.load_texture(PLAYER_SPRITE, scale=CHARACTER_SCALING)

        # Create the ground
        for x in range(0, 1450, 64):
            ground = arcade.Sprite(GROUND_SPRITE, TILE_SCALING)
            ground.center_x = x
            ground.center_y = 32
            self.ground_list.append(ground)

        obstacle = arcade.Sprite(OBSTACLE_SPRITE, OBSTACLE_SCALING)
        obstacle.position = [random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 100), 96]
        self.obstacle_list.append(obstacle)

        flying = arcade.Sprite(ROCKET_SPRITE, ROCKET_SCALING)
        flying.position = [random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 100), 400]
        self.flying_list.append(flying)

        self.num_of_obstacles = 0
        self.num_of_flyings = 0 
        self.difficulty = DIFFICULTY + 0.005
        self.is_ducking = False


        # Create the physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.ground_list, GRAVITY)

    def draw_game(self):
        # Clear the screen to the background color
        arcade.start_render()

        background = arcade.load_texture(BACKGROUND_IMAGE)
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, background)

        # Randomly generate obstacles
       
        flying = arcade.Sprite(ROCKET_SPRITE, ROCKET_SCALING)
        flying.position = [random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 100), 400]

        try:
            # Check to make sure that there is enough space between obstacles
            gap_exists = flying.position[0] - self.flying_list[self.num_of_flyings].position[0] > 15000

            if random.random() < self.difficulty and gap_exists:
                self.flying_list.append(flying)
                self.num_of_flyings += 1
                self.difficulty += 0.005
        except IndexError:
            self.flying_list.append(flying)
            self.num_of_flyings += 1
            self.difficulty += 0.005


        # Randomly generate obstacles
        obstacle = arcade.Sprite(OBSTACLE_SPRITE, OBSTACLE_SCALING)
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
        self.flying_list.draw()

        # Display score on the screen
        score_text = f"{self.score/10} meters"
        arcade.draw_text(score_text, 20, SCREEN_HEIGHT - 50, arcade.csscolor.WHITE, 40, font_name=FONT)
        high_score = f"High score: {self.high_score/10}"
        arcade.draw_text(high_score, 20, SCREEN_HEIGHT - 100, arcade.csscolor.WHITE, 40, font_name=FONT)

    # Display a random question image from assets/images/questions/
    def draw_question(self):
        if not self.waiting_on_input:
            with open('questions.csv') as questions:
                rows = questions.readlines()
                data = random.choice(list(csv.reader(rows,
                                                     quotechar='"',
                                                     delimiter=',',
                                                     quoting=csv.QUOTE_ALL,
                                                     skipinitialspace=True
                                                    )))
            self.question = data[0]
            self.correct_answer = int(data[1])
            self.waiting_on_input = True

        background = arcade.load_texture("assets/images/questions/" + self.question + ".png")
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, background)

    # Draw a fullscreen background from an image file
    def draw_image(self, image, width, height):
        background = arcade.load_texture(image)
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, width, height, background)

    # Render the screen based on the currect state
    def on_draw(self):
        if self.current_state == RUNNING:
            self.draw_game()

        elif self.current_state == HELP:
            self.draw_image(HELP_IMAGE, SCREEN_WIDTH, SCREEN_HEIGHT)

        elif self.current_state == CONTROLS:
            self.draw_image(CONTROLS_IMAGE, SCREEN_WIDTH, SCREEN_HEIGHT)

        elif self.current_state == TITLE:
            self.draw_image(TITLE_IMAGE, SCREEN_WIDTH * self.scale, SCREEN_HEIGHT * self.scale)

            if self.start_zoom and self:
                self.scale += 0.05

            if self.scale >= 3.5:
                self.current_state = RUNNING

        elif self.current_state == GAMEOVER:
            self.draw_game()
            self.draw_question()

    # Called whenever a key is pressed
    def on_key_press(self, key, modifiers):
       # Check whether the answer is correct
        if self.current_state == GAMEOVER:
            if key == self.correct_answer + 96:
                print("Correct answer! Continuing")
                self.waiting_on_input = False
                arcade.play_sound(self.correct_sound)
                self.setup()
                self.current_state = RUNNING
            elif key == 97 or key == 98 or key == 99 or key == 100:
                print("Wrong answer! Restarting")
                self.waiting_on_input = False
                arcade.play_sound(self.wrong_sound)

                if self.score > self.high_score:
                    self.high_score = self.score

                self.setup()
                self.score = 0
                self.current_state = RUNNING

         # Change between game states
        elif self.current_state == TITLE:
            if key == arcade.key.SPACE:
                self.start_zoom = True
            elif key == arcade.key.H:
                self.current_state = HELP
            elif key == arcade.key.ESCAPE:
                exit()
        elif self.current_state == HELP:
            self.current_state = CONTROLS
        elif self.current_state == CONTROLS:
            self.current_state = TITLE

        elif self.current_state == RUNNING:
            # Toggle on jumping/ducking
            if key == arcade.key.SPACE or key == arcade.key.UP or key == arcade.key.W:
                self.key_pressed = True
            elif key == arcade.key.DOWN or key == arcade.key.S:
                self.player_sprite.change_y = -STOMP_SPEED
                self.is_ducking = True

    def on_key_release(self, key, modifiers):
        # Toggle off jumping/ducking
        if key == arcade.key.SPACE or key == arcade.key.UP or key == arcade.key.W:
            self.key_pressed = False
        if key == arcade.key.DOWN or key == arcade.key.S:
            self.is_ducking = False

    # Movement and game logic
    def update(self, delta_time):
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

            collision2 = arcade.check_for_collision_with_list(self.player_sprite, self.flying_list)

            if collision2:
                self.current_state = GAMEOVER

            # Move all the obstacles forward (making it look the like player is moving forward)
            for flying in self.flying_list:
                # Multiply speed by delta time to make sure that the speed is consitent
                # Otherwise the obstacles will move faster on faster processors and vice versa
                flying.center_x -= delta_time * 800

                # Remove obstacles that aren't visible anymore (to prevent lag)
                if flying.center_x < -15000:
                    self.flying_list.remove(flying)
                    self.num_of_flyings -= 1
                    print("Removed flyingr")

            # Player movement (jumping and ducking)
            if self.physics_engine.can_jump():
                if self.is_ducking:
                    self.player_sprite.texture = arcade.load_texture(PLAYER_DUCK, scale=CHARACTER_SCALING)
                else:
                    self.player_sprite.texture = arcade.load_texture(PLAYER_SPRITE, scale=CHARACTER_SCALING)

                if self.key_pressed:
                    self.player_sprite.change_y = JUMP_SPEED
                    self.player_sprite.texture = arcade.load_texture(PLAYER_JUMP, scale=CHARACTER_SCALING)

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
