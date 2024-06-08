from blockpaths import bs_burning_snd
from animator import Animator
from constants import ct_frT
import pygame as pg


class Fire(pg.sprite.Sprite):
    def __init__(self, paths, width, height, pos):
        pg.sprite.Sprite.__init__(self)
        origs = list()
        for path in paths:
            frame = pg.image.load(path).convert_alpha()
            origs.append(frame)
        self.frames = list()
        self.width = width
        self.height = height
        for frame in origs:
            sprite = pg.transform.scale(frame, (self.width, self.height))
            self.frames.append(sprite)
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = pos[0], pos[1]
        self.animator = Animator(self.frames, ct_frT)
        self.sound = pg.mixer.Sound(bs_burning_snd)
        self.sound_on = True

    def update(self, surface):
        if self.sound_on:
            self.sound.play()
        self.image = self.animator.animate()
        surface.blit(self.image, self.rect)

    def __del__(self):
        pass
