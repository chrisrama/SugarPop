#############################################################
# Module Name: Sugar Pop Head Up Display Module
# Project: Sugar Pop Program
# Date: Dec 7, 2024
# By: Christian Ramazani
# Description: The HEad Up Display implementation of the sugar pop game
#############################################################

import pygame as pg

class HUD:
    def __init__(self, screen, font_size=24, font_color='white'):
        """
        Initialize the HUD.

        :param screen: The Pygame screen to render the HUD on.
        :param font_size: The size of the font used for text.
        :param font_color: The color of the font used for text.
        """
        self.screen = screen
        self.font = pg.font.Font(None, font_size)
        self.font_color = pg.Color(font_color)
        self.total_sugar = 0
        self.sugar_in_buckets = {}
        self.num_sugar_drop = 0
        self.level_count = 1
        self.gravity_pos = "DOWN"

    def update(self, total_sugar, sugar_in_buckets, sugar_left, level_count,gravity_pos):
        """
        Update the Head up display values.

        :param total_sugar: total number sugar grains in the game.
        :param sugar_in_buckets: dictionary with bucket IDs as keys and sugar counts as values.
        :param sugar_not_sent: count of  the sugar not yet sent from the spout.
        :param level_count: Current level number.
        """
        self.total_sugar = total_sugar
        self.sugar_in_buckets = sugar_in_buckets
        self.num_sugar_drop = sugar_left
        self.level_count = level_count
        self.gravity_pos = gravity_pos
         # Process the list of bucket objects to extract their IDs and counts
        self.sugar_in_buckets = {idx: bucket.count for idx, bucket in enumerate(sugar_in_buckets)}


    def draw(self):
        """
        Draw the HUD on the screen.
        """
        y_offset = 10  # Vertical spacing
        x_offset = 10  # Horizontal margin

        # Drawing the total Count of sugar on the screen
        total_sugar_surface = self.font.render(f"Total Sugar: {self.total_sugar}", True, self.font_color)
        self.screen.blit(total_sugar_surface, (x_offset, y_offset))
        y_offset += total_sugar_surface.get_height() + 5

        # Drawing the sugar in buckets
        for bucket_id, count in self.sugar_in_buckets.items():
            bucket_sugar_surface = self.font.render(f"Bucket {bucket_id+1}: {count} grains", True, self.font_color)
            self.screen.blit(bucket_sugar_surface, (x_offset, y_offset))
            y_offset += bucket_sugar_surface.get_height() + 5

        # Drawing sugar remain
        sugar_left = self.total_sugar - int(self.num_sugar_drop)
        Sugar_left_surface = self.font.render(f"Sugar Left: {sugar_left}", True, self.font_color)
        self.screen.blit(Sugar_left_surface, (x_offset, y_offset))
        y_offset += Sugar_left_surface.get_height() + 5

        # Drawing level count
        level_surface = self.font.render(f"Current Level: {self.level_count}", True, self.font_color)
        self.screen.blit(level_surface, (x_offset, y_offset))
        y_offset += level_surface.get_height() + 5


        # drawing the gravity text
        gravity_text = f"Gravity is : {self.gravity_pos}"
        gravity_surface = self.font.render(gravity_text, True, self.font_color)
        self.screen.blit(gravity_surface, (400, 10))

        #drawing the instructions
        pause_text =  'Press space to pause'
        pause_surface = self.font.render(pause_text, True, self.font_color)
        self.screen.blit(pause_surface,(800,10))
        #drawing the gavity text message
        gravity1_text = 'Press G to change gravity'
        gravity1_text = self.font.render(gravity1_text, True, self.font_color)
        self.screen.blit(gravity1_text,(800,25))


        
