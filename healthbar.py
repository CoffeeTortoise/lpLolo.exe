from constants import ct_fnt_path, ct_fnt_size, ct_ru_path
from constants import ct_red, ct_white
from rectentity import RectEntity
from saveload import SaveLoad
import pygame as pg


class HealthBar:
    def __init__(self, pos, surface):
        ru = int(SaveLoad.load(ct_ru_path))
        text = 'Purification' if (ru == 0) else 'Очищение'
        self.pos, self.surface = pos, surface
        self.font = pg.font.Font(ct_fnt_path, ct_fnt_size)
        self.text = self.font.render(text, 1, ct_red, ct_white)
        width = self.text.get_width()
        self.bar = RectEntity(width, ct_fnt_size, ct_red, pos[0], pos[1])

    def show_hp(self, k):
        width = self.bar.width
        self.bar.width *= k
        self.surface.blit(self.text, self.pos)
        self.bar.draw(self.surface)
        self.bar.width = width

    def __del__(self):
        pass
