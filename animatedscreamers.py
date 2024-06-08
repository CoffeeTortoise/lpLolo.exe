from lizardspaths import lp_scr1, lp_scr2, lp_scr3
from animatedblock import AnimatedBlock


class LizardsMouth(AnimatedBlock):
    def __init__(self, width, height, pos):
        paths = [lp_scr1, lp_scr2, lp_scr3]
        super().__init__(width, height, pos, paths)

    def __del__(self):
        pass
