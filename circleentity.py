import pygame as pg


class CircleEntity:
    def __init__(self, radius, color, center):
        self.color = color
        self.center = center
        self.radius = radius

    @property
    def my_circle(self):
        """Color, center and radius of the circle"""
        return self.color, self.center, self.radius

    @my_circle.setter
    def my_circle(self, data):
        """Color, center and radius of the circle"""
        self.color, self.center, self.radius = data[0], data[1], data[2]

    def draw(self, surface):
        pg.draw.circle(surface, self.color, self.center, self.radius)

    def __del__(self):
        pass
