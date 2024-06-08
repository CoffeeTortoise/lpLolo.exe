from demonspaths import dp_eg_eye1, dp_eg_eye2, dp_eg_eye3, dp_eg_eye4
from demonspaths import dp_eg_body, dp_eg_mouth
from animatedblock import AnimatedBlock
from baseclasses import Block


class Egg:
    def __init__(self, width, height, pos):
        eye_paths = (dp_eg_eye1, dp_eg_eye2, dp_eg_eye3, dp_eg_eye4)
        self.width, self.height = width, height
        self.body = Block(width, height, pos, dp_eg_body)
        m_x, m_y = self.body.pos[0]*1.08, self.body.pos[1]*10
        m_w, m_h = self.body.width*.8, self.body.height/4
        self.mouth = Block(m_w, m_h, (m_x, m_y), dp_eg_mouth)
        e_x1, e_x2, e_y = self.body.pos[0]*1.1, self.body.pos[0]*1.51, self.body.pos[1]*5
        e_w, e_h = self.body.width*.3, self.body.height/5
        self.eye1 = AnimatedBlock(e_w, e_h, (e_x1, e_y), eye_paths)
        self.eye2 = AnimatedBlock(e_w, e_h, (e_x2, e_y), eye_paths)

    def update(self, surface):
        self.body.update(surface)
        self.mouth.update(surface)
        self.eye1.update(surface)
        self.eye2.update(surface)

    @property
    def pos(self):
        return self.body.rect.left, self.body.rect.top

    @pos.setter
    def pos(self, new):
        self.body.rect.left, self.body.rect.top = new

    def __del__(self):
        pass
