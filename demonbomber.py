from demonspaths import dp_deadman
from monster import Monster
import pygame as pg


class DemonBomber(Monster):
    def __init__(self, m_speed, m_jump, width, height, hp, attack, pos):
        super().__init__(m_speed, m_jump, width, height, hp, attack)
        img = pg.image.load(dp_deadman).convert_alpha()
        self.normal = pg.transform.scale(img, (width, height))
        self.flipped = pg.transform.flip(self.normal, True, False)
        self.image = self.normal
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = pos[0], pos[1]

    def animate(self):
        if self.speed != 0:
            if self.right:
                self.image = self.normal
            else:
                self.image = self.flipped
        else:
            if self.right:
                self.image = self.normal
            else:
                self.image = self.flipped

    def __del__(self):
        pass
