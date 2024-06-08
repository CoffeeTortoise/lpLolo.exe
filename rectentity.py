import pygame as pg


class RectEntity:
    def __init__(self, width, height, color, left, top):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.color = color

    @property
    def my_rect(self):
        return pg.Rect(self.left, self.top, self.width, self.height)

    @my_rect.setter
    def my_rect(self, new):
        self.left, self.top, self.width, self.height = new[0], new[1], new[2], new[3]

    def draw(self, surface):
        rect = (self.left, self.top, self.width, self.height)
        pg.draw.rect(surface, self.color, rect)

    def cold_rect(self, rect):
        me = pg.Rect(self.left, self.top, self.width, self.height)
        res = True if me.colliderect(rect) else False
        return res

    def cold_point(self, point):
        me = pg.Rect(self.left, self.top, self.width, self.height)
        res = True if me.collidepoint(point) else False
        return res

    def __del__(self):
        pass
