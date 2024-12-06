#############################################################
# Module Name: Sugar Pop Main Module
# Project: Sugar Pop Program
# Date: Dec 7, 2024
# By: Christian Ramazani
# Description: The main implementation of the sugar pop game
#############################################################

import pygame as pg
import pymunk  # Import Pymunk library
import sys
from settings import *
import random
import static_item
import dynamic_item
import sugar_grain
import bucket
import level
import message_display  
from audio import *
from HUD import HUD 
import time 

class Game:
    def __init__(self) -> None:
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.iter = 0
        
        # Initialize font for HUD
        self.font = pg.font.SysFont(None, 36)  # Default font, size 36

        # Create a Pymunk space with gravity
        self.current_level = 0 # Start game at 0
        self.level_complete = False
        self.space = pymunk.Space()
        self.space.gravity = (0, -9)  # Gravity pointing downwards in Pymunk's coordinate system
        # Iterations defaults to 10. Higher is more accurate collison detection
        self.space.iterations = 30 

        self.drawing_lines = []
        self.sugar_grains = []
        self.buckets = []
        self.statics = []
        self.total_sugar_count = None
        self.level_spout_position = None
        self.level_grain_dropping = None
        self.mouse_down = False
        self.current_line = None
        self.message_display = message_display.MessageDisplay(font_size=72)
        # loading the sound class
        self.sound = Sound()
        # Load the intro image
        self.intro_image = pg.image.load("./images/SugarPop.png").convert()  # Load the intro image
        # Get new height based on correct scale
        scale_height = self.intro_image.get_height() * WIDTH / self.intro_image.get_width()
        self.intro_image = pg.transform.scale(self.intro_image, (WIDTH, int(scale_height)))  # Scale to screen resolution
        
        pg.time.set_timer(LOAD_NEW_LEVEL, 2000)  # Load in 2 seconds
        # creating the class for the head up display messages
        self.hud = HUD(self.screen)
        #ussed to chnage gravity attributes 
        self.gravity_direction = 1
        self.gravity_pos = "Down"
        # setting the times limit 
        self.is_pause = False

       


    def load_level(self, levelnumber=0):
        # Destroy any current game objects
        for item in self.sugar_grains:
            item.delete()  # Delete all sugar grains
        for item in self.drawing_lines:
            item.delete() 
        for item in self.buckets:
            item.delete() 
        for item in self.statics:
            item.delete() 
        self.sugar_grains = []
        self.drawing_lines = []  # Clear the list
        self.buckets = []
        self.statics = []
 
        new_level = LEVEL_FILE_NAME.replace("X", str(levelnumber))
        self.level = level.Level(new_level)
        
        # Make sure the file was found
        if not self.level or not self.level.data:
            return False
        else:  # Do final steps to start the level
            self.level_grain_dropping = False
            self.level_spout_position = (self.level.data['spout_x'], self.level.data['spout_y'])
            self.build_main_walls()

            # Load buckets
            for nb in self.level.data['buckets']:
                self.buckets.append(bucket.Bucket(self.space, nb['x'], nb['y'], nb['width'], nb['height'], nb['needed_sugar']))
            # Load static items
            for nb in self.level.data['statics']:
                self.statics.append(static_item.StaticItem(self.space, nb['x1'], nb['y1'], nb['x2'], nb['y2'], nb['color'], nb['line_width'], nb['friction'], nb['restitution']))
            self.total_sugar_count = self.level.data['number_sugar_grains']
            pg.time.set_timer(START_FLOW, 5 * 1000)  # 5 seconds
            self.message_display.show_message("Level Up", 10)
            self.level_complete = False
            return True

    def build_main_walls(self):
        '''Build the walls, ceiling, and floor of the screen'''
        # Floor
        floor = static_item.StaticItem(self.space, 0, 0, WIDTH, 0, 'red', 5)
        self.statics.append(floor)
        # Left Wall
        left_wall = static_item.StaticItem(self.space, 0, 0, 0, HEIGHT, 'red')
        self.statics.append(left_wall)
        # Right Wall
        right_wall = static_item.StaticItem(self.space, WIDTH, 0, WIDTH, HEIGHT, 'red')
        self.statics.append(right_wall)
        # Ceiling
        ceiling = static_item.StaticItem(self.space, 0, HEIGHT, WIDTH, HEIGHT, 'red')
        self.statics.append(ceiling)
    
    def check_all_buckets_exploded(self):
        """
        Check if all buckets have exploded.
        """
        return all(bucket.exploded for bucket in self.buckets)

    def update(self):
        '''Update the program physics'''
        # pausing game
        if self.is_pause == True:
            return
        
        # Keep an overall iterator
        self.iter += 1
        
        # Calculate time since last frame
        delta_time = self.clock.tick(FPS) / 1000.0  # Convert milliseconds to seconds

        # Cap delta_time to prevent instability from large time steps
        time_step = min(delta_time, MAX_TIME_STEP)

        # Step the physics simulation forward with the calculated time_step
        self.space.step(time_step)
        
        # Update our game counter
        if self.iter == 60:
            self.iter = 0

        pg.display.set_caption(f'Level : {self.current_level} fps: {self.clock.get_fps():.1f}')
        
        # Only do the following every 20 frames for less system stress
        if self.iter % 20 == 0:
            # Update any messages
            self.message_display.update()
            
            # Calculate buckets count by counting each grain's position
            # First, explode or reset the counter on each bucket
            for bucket in self.buckets:
                if bucket.count >= bucket.needed_sugar:
                    bucket.explode(self.sugar_grains)
                    # If all the buckets are gone, level up!
                    if not self.level_complete and self.check_all_buckets_exploded():
                        self.level_complete = True
                        
                        self.message_display.show_message("Level Complete!", 2)
                        #playing the sound of level complete
                        self.sound.play_level_complete()

                        pg.time.set_timer(LOAD_NEW_LEVEL, 2000)  # Schedule next level load
                else:
                    bucket.count_reset()
            # Count the grains in the un-exploded buckets
            for grain in self.sugar_grains:
                for bucket in self.buckets:
                    bucket.collect(grain)
                
            # Drop sugar if needed
            if self.level_grain_dropping:
                # Create new sugar to drop
                new_sugar = sugar_grain.sugar_grain(self.space, self.level_spout_position[0], self.level_spout_position[1], 0.1)
                self.sugar_grains.append(new_sugar)
                # Check if it's time to stop
                if len(self.sugar_grains) >= self.total_sugar_count:
                    self.level_grain_dropping = False
        # initializing the headup display module to becalled 
        self.hud.update(
        total_sugar=self.total_sugar_count,
        sugar_in_buckets=self.buckets,  # Pass the list of bucket objects
        sugar_left= len(self.sugar_grains),
        level_count=self.current_level,gravity_pos = self.gravity_pos)
       


    def draw_hud(self):
        """Drawing the head up display  the number of grains."""
         #   self.screen.blit(text_surface, (10, 10))  # Position at top-left corner
        if self.total_sugar_count:
            self.hud.draw() # calling the draw function from the head up display module
    def toggle_gravity(self):
        """reversing the gravity direction and update Head up display ."""
        self.gravity_direction *= -1  # changing direction between 1 and -1
        
        #changin the gravity of 
        self.space.gravity = (0, -9 * self.gravity_direction)
        if self.gravity_direction == -1:  # check if the gravity direction is posit
            self.gravity_pos = "Up"  # changing the position of the gravity 
        else:
            self.gravity_pos = "Down"
        # displaying message gravity is down
        self.message_display.show_message('Gravity now {0}'.format(self.gravity_pos), 1)
    #pausing the game is the key space is press
    def pause_game(self):
        #self.message_display.show_message('Game is pause',1)
        self.is_pause = not(self.is_pause)
        if self.is_pause == True:
            self.message_display.show_message('Game is pause',1)
        else:
            self.message_display.show_message('Game is playing',1)

        
         




    def draw(self):
        '''Draw the overall game. Should call individual item draw() methods'''
        # Clear the screen
        self.screen.fill('black')
        # Only show the intro screen if we haven't loaded a level yet
        if self.intro_image:
            self.sound.play_start_game()
            self.screen.blit(self.intro_image, (0, 0))  # Draw the intro image

    
        for bucket in self.buckets:
            bucket.draw(self.screen)

        # Draw each sugar grain
        for grain in self.sugar_grains:
            grain.draw(self.screen)

        # Draw the current dynamic line
        if self.current_line is not None:
            self.current_line.draw(self.screen)
        
        # Draw the user-drawn lines
        for line in self.drawing_lines:
            line.draw(self.screen)
            
        # Draw any static items
        for static in self.statics:
            static.draw(self.screen)
        

        # Draw the nozzle (Remember to subtract y from the height)
        if self.level_spout_position:
            pg.draw.line(
                self.screen, 
                (255, 165, 144), 
                (self.level_spout_position[0], HEIGHT - self.level_spout_position[1] - 10), 
                (self.level_spout_position[0], HEIGHT - self.level_spout_position[1]), 
                5
            )
        
        # Draw the heads-up display
        if self.total_sugar_count:
            self.hud.draw()

        # Show any messages needed        
        self.message_display.draw(self.screen)

        # Update the display
        pg.display.update()

    def check_events(self):
        '''Check for keyboard and mouse events'''
        for event in pg.event.get():
            if event.type == EXIT_APP or event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.mouse_down = True
                # Get mouse position and start a new dynamic line
                mouse_x, mouse_y = pg.mouse.get_pos()
                self.current_line = dynamic_item.DynamicItem(self.space, 'blue')
                self.current_line.add_vertex(mouse_x, mouse_y)
                
            elif event.type == pg.MOUSEBUTTONUP:
                self.mouse_down = False
                if self.current_line:
                    self.drawing_lines.append(self.current_line)
                    self.current_line = None
                
            elif event.type == pg.MOUSEMOTION and self.mouse_down:
                # Get mouse position
                mouse_x, mouse_y = pg.mouse.get_pos()
                if mouse_x == 0 or mouse_x == WIDTH or mouse_y == 0 or mouse_y == HEIGHT:
                    self.mouse_down = False
                if self.current_line and self.iter % 10 == 0:
                    self.current_line.add_vertex(mouse_x, mouse_y)

            elif event.type == START_FLOW:
                self.level_grain_dropping = True
                # Disable the timer after the first trigger
                pg.time.set_timer(START_FLOW, 0)
                #checking if the gravity is bring change
            elif event.type == pg.KEYDOWN: #createing a check of even when G is press the gravity change
                if event.key == pg.K_g:  # Press 'G' to reverse gravity
                    self.toggle_gravity()
                    #self.pause_game()
                elif event.key == pg.K_SPACE:
                     self.pause_game()   
            #elif event.type == pg.KEYDOWN: #createing a check of even when G is press the gravity change
            #    if event.key == pg.K_p:  # Press 'G' to reverse gravity
                    #self.toggle_gravity()
                    #self.pause_game()      
            elif event.type == LOAD_NEW_LEVEL:
                pg.time.set_timer(LOAD_NEW_LEVEL, 0)  # Clear the timer
                self.intro_image = None
                self.current_level += 1
                if not self.load_level(self.current_level):
                    self.message_display.show_message("You Win!", 5)  # End of game message
                    pg.time.set_timer(EXIT_APP, 5000)  # Quit game after 5 seconds
                else:
                    self.message_display.show_message(f"Level {self.current_level} Start!", 2)
                    
                    
    def run(self):
        '''Run the main game loop'''
        while True:
    # Calculate elapsed time
           # elapsed_time = time.time() - self.start_time
           # remaining_time = self.time_limit - elapsed_time

    # Check if time is up
            #if remaining_time <= 0:
                #self.message_display.show_message("Time's up! Restarting level...", 10)
               # self.restart_current_level()

    # Render timer on the HUD
                #self.hud.render_timer(remaining_time)
            self.check_events()
            self.update()
            self.draw()

def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()
