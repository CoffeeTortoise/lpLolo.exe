from turtlepaths import tp_tf_stay, tp_tf_step1, tp_tf_step2
from turtlepaths import tp_tm_stay, tp_tm_step1, tp_tm_step2
from animator import Animator
from monster import Monster
from constants import ct_frT
import pygame as pg


class Turtle(Monster):
    def __init__(self, m_speed, m_jump, width, height, hp, attack, pos, female):
        super().__init__(m_speed, m_jump, width, height, hp, attack)
        stay = tp_tf_stay if female else tp_tm_stay
        step1 = tp_tf_step1 if female else tp_tm_step1
        step2 = tp_tf_step2 if female else tp_tm_step2
        paths = [stay, step1, step2]
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

    def __del__(self):
        pass
