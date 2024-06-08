from baseclasses import Block
from fire import Fire


class Candle:
    def __init__(self, rack_path, fire_paths, r_width, r_height, r_pos):
        """Fire height grater then rack height in almost two times"""
        self.rack = Block(r_width, r_height, r_pos, rack_path)
        fire_pos = (r_pos[0], r_pos[1]-self.rack.height*1.8)
        self.fire = Fire(fire_paths, r_width, r_height*2, fire_pos)
        self.width, self.height = self.rack.width, self.rack.height + self.fire.height
        self.top, self.left = fire_pos[1], r_pos[0]
        self.rect = self.rack.rect.union(self.fire.rect)
        self.fire.sound_on, self.burning = False, True

    def update(self, surface):
        self.rack.update(surface)
        if self.burning:
            self.fire.update(surface)

    def __del__(self):
        pass
