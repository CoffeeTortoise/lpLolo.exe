from constants import ct_fnt_path, ct_fnt_size
from constants import ct_white, ct_cinnabar
from baseclasses import Block
import pygame as pg


class CoinBar(Block):
    def __init__(self, width, height, pos, img_path, coins, surface):
        super().__init__(width, height, pos, img_path)
        self.coins, self.surface = coins, surface
        self.font = pg.font.Font(ct_fnt_path, ct_fnt_size)
        self.text1 = self.font.render('X', 1, ct_white)
        self.text2 = self.font.render(str(self.coins), 1, ct_cinnabar)
        self.text1_pos = (pos[0]+self.width, pos[1])
        self.text2_pos = (pos[0]+self.width+self.text1.get_width(), pos[1])

    def show_coins(self, coins):
        self.coins = coins
        self.text2 = self.font.render(str(self.coins), 1, ct_cinnabar)
        self.update(self.surface)
        self.surface.blit(self.text1, self.text1_pos)
        self.surface.blit(self.text2, self.text2_pos)

    def __del__(self):
        pass
