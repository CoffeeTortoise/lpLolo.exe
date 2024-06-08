from constants import ct_rosy, ct_red, ct_white
from constants import ct_fnt_size, ct_fnt_path
from rectentity import RectEntity
import pygame as pg


class StarBar:
    def __init__(self, pos):
        font = pg.font.Font(ct_fnt_path, ct_fnt_size)
        text = 'Punished'
        self.text, self.position = font.render(text, 1, ct_red, ct_white), pos
        self.width, self.height = self.text.get_width(), self.text.get_height()
        self.line = RectEntity(self.width, self.height, ct_rosy, pos[0], pos[1])

    @property
    def pos(self):
        return self.position

    @pos.setter
    def pos(self, new):
        self.position = new
        self.line.left, self.line.top = new

    def show_hp(self, k, surface):
        self.line.width *= k
        surface.blit(self.text, self.position)
        self.line.draw(surface)
        self.line.width = self.width

    def __del__(self):
        pass
