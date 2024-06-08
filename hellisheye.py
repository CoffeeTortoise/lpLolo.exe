from demonspaths import dp_h_e_idle, dp_h_e_step
from animator import Animator
from constants import ct_frT
from monster import Monster
import pygame as pg


class HellishEye(Monster):
    def __init__(self, m_speed, m_jump, width, height, hp, attack, pos):
        super().__init__(m_speed, m_jump, width, height, hp, attack)
        paths = [dp_h_e_idle, dp_h_e_step]
        origs = []
        for dirs in paths:
            image = pg.image.load(dirs).convert_alpha()
            origs.append(image)
        self.frames_r = []
        for image in origs:
            sprite = pg.transform.scale(image, (width, height))
            self.frames_r.append(sprite)
        self.frames_l = []
        for sprite in self.frames_r:
            flipped = pg.transform.flip(sprite, True, False)
            self.frames_l.append(flipped)
        self.animate_r = Animator(self.frames_r, ct_frT)
        self.animate_l = Animator(self.frames_l, ct_frT)
        self.image = self.frames_r[0]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = pos[0], pos[1]
        self.width, self.height = width, height

    def animate(self):
        if self.right:
            self.image = self.animate_r.animate()
        else:
            self.image = self.animate_l.animate()

    def __del__(self):
        pass
