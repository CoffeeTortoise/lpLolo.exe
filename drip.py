from baseclasses import Block
from randpos import RandPos
from timer import Timer


class Drip(Block):
    def __init__(self, width, height, img_path, top, line, bottom, begin, end, speed):
        pos = RandPos.rand_cords(top, line, begin, end)
        super().__init__(width, height, pos, img_path)
        self.top, self.line, self.bottom = top, line, bottom
        self.begin, self.end = begin, end
        self.speed = speed
        self.fallen = False
        self.timer = Timer()

    def update(self, surface):
        self.fall()
        surface.blit(self.image, self.rect)

    def fall(self):
        pos_y = self.rect.top
        time = self.timer.get_time()
        self.timer.restart()
        if not self.fallen:
            self.rect.top += self.speed*time
            if pos_y >= self.bottom:
                self.fallen = True
        else:
            pos = RandPos.rand_cords(self.top, self.line, self.begin, self.end)
            self.rect.left, self.rect.top = pos[0], pos[1]
            self.fallen = False

    def __del__(self):
        pass
