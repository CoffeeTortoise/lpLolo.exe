from baseclasses import Block
from animator import Animator
from constants import ct_frT
import pygame as pg


class AnimatedBlock(Block):
    def __init__(self, width, height, pos, paths):
        """Paths is a tuple/list"""
        super().__init__(width, height, pos, paths[0])
        self.frames, origs = [], []
        for dirs in paths:
            image = pg.image.load(dirs).convert_alpha()
            origs.append(image)
        for image in origs:
            frame = pg.transform.scale(image, (width, height))
            self.frames.append(frame)
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = pos[0], pos[1]
        self.animator = Animator(self.frames, ct_frT)

    def update(self, surface):
        self.image = self.animator.animate()
        super().update(surface)

    def __del__(self):
        pass
