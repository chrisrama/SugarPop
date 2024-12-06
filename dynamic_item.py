#############################################################
# Module Name: Sugar Pop Dynamic Item Module
# Project: Sugar Pop Program
# Date: Nov 17, 2024
# By: Brett W. Huffman
# Description: The dynamic item implementation of the sugar pop game
#############################################################
import pygame as pg
import pymunk
from settings import SCALE, HEIGHT, WIDTH

class DynamicItem:
    def __init__(self, space, color='red', friction=0.3, elasticity=0.5, thickness=0.2):
        """
        Initialize the dynamic item.

        :param space: The Pymunk space.
        :param color: The color for drawing the item.
        :param friction: The friction coefficient of the item's surfaces.
        :param elasticity: The elasticity (bounciness) of the item's surfaces.
        """
        self.color = color
        self.space = space
        self.friction = friction
        self.elasticity = elasticity
        self.thickness = thickness
        self.vertices = []  # Store vertices as they are added
        self.segments = []  # Store the segments created
        # Create a static body to attach the segments to
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.space.add(self.body)

    def add_vertex(self, x, y):
        """
        Add a new vertex and create a Segment between the last vertex and the new one.
        """
        # Convert the Pygame coordinates to Pymunk coordinates (Pymunk's Y-axis points upwards)
        adjusted_x = x / SCALE
        adjusted_y = (HEIGHT - y) / SCALE

        # Add the new vertex with adjusted coordinates
        new_vertex = (adjusted_x, adjusted_y)
        
        if self.vertices:
            # Create a segment between the last vertex and the new vertex
            last_vertex = self.vertices[-1]
            segment = pymunk.Segment(self.body, last_vertex, new_vertex, self.thickness)  # Thickness of 0.1 units
            segment.friction = self.friction
            segment.elasticity = self.elasticity
            self.space.add(segment)
            self.segments.append(segment)
        
        # Add the new vertex to the list
        self.vertices.append(new_vertex)

    def set_color(self, color='blue'):
        """
        Set the drawing color of the dynamic item.

        :param color: The color to set.
        """
        self.color = color
        
    def draw(self, screen):
        """
        Draw the chain shape (edges) on the Pygame screen.
        """
        # Calculate the visual line width based on thickness
        line_width = max(1, int(self.thickness * SCALE * 0.7))
    
        for i in range(len(self.vertices) - 1):
            start_x = self.vertices[i][0] * SCALE
            start_y = HEIGHT - self.vertices[i][1] * SCALE
            end_x = self.vertices[i + 1][0] * SCALE
            end_y = HEIGHT - self.vertices[i + 1][1] * SCALE
            start = (start_x, start_y)
            end = (end_x, end_y)
            pg.draw.line(screen, pg.Color(self.color), start, end, line_width)

    def delete(self):
        """
        Delete the dynamic item by removing its segments from the Pymunk space and clearing its vertices.
        """
        # Remove segments from the space
        for segment in self.segments:
            self.space.remove(segment)
        self.segments = []
        # Remove the body from the space
        if self.body is not None:
            self.space.remove(self.body)
            self.body = None
        # Clear the vertices list
        self.vertices = []


# class MovingObstacle(DynamicItem):
#     def __init__(self, space, x_start, x_end, y, speed=100, **kwargs):
#         """
#         Initialize a moving obstacle that oscillates horizontally.
        
#         :param space: The Pymunk space.
#         :param x_start: Start x-position for movement.
#         :param x_end: End x-position for movement.
#         :param y: Fixed y-position of the obstacle.
#         :param speed: Speed of the horizontal movement.
#         """
#         super().__init__(space, **kwargs)
#         self.x_start = x_start
#         self.x_end = x_end
#         self.y = y
#         self.speed = speed
#         self.current_direction = 1  # 1 for right, -1 for left

#         # Add a single horizontal segment
#         self.add_vertex(x_start, y)
#         self.add_vertex(x_start + 50, y)  # Width of the obstacle

#     def update(self, delta_time):
#         """
#         Update the position of the obstacle.
        
#         :param delta_time: Time since the last update, used for consistent movement.
#         """
#         # Update position based on speed and direction
#         x_movement = self.speed * self.current_direction * delta_time

#         # Calculate new position
#         for vertex in self.vertices:
#             new_x = vertex[0] + x_movement / SCALE
#             if new_x < self.x_start / SCALE or new_x > self.x_end / SCALE:
#                 self.current_direction *= -1  # Reverse direction
#                 x_movement *= -1
#                 break
#             vertex = (new_x, vertex[1])

#         # Recalculate all segments
#         self.delete()  # Remove old segments
#         for i in range(len(self.vertices) - 1):
#             self.add_vertex(
#                 self.vertices[i][0] * SCALE, 
#                 HEIGHT - self.vertices[i][1] * SCALE
#             )
        

#     def draw(self, screen):
#         """Draws the moving obstacle."""
#         super().draw(screen)
#     def setup_dynamic_obstacles(self):
#         self.moving_obstacles.append(dynamic_item.MovingObstacle(
#             space=self.space,
#             x_start=100,
#             x_end=400,
#             y=300,
#             speed=100,
#             color="blue",
#             line_width=5
#         ))

#         self.moving_obstacles.append(dynamic_item.MovingObstacle(
#             space=self.space,
#             x_start=200,
#             x_end=500,
#             y=400,
#             speed=80,
#             color="red",
#             line_width=3
#         ))

