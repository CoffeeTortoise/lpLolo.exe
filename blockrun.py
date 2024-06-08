from rectmotion import SinMotion
from baseclasses import Block


class BlockSin(Block):
    """Just block that moves along a sin wave"""
    def __init__(self, width, height, pos, img_path, speed):
        super().__init__(width, height, pos, img_path)
        a, b = pos[1], width*3
        self.motion = SinMotion(self.rect, False, speed, a=a, b=b)

    def update(self, surface):
        self.rect = self.motion.move()
        self.motion.me_rect = (self.rect, False)
        super().update(surface)

    def __del__(self):
        pass
