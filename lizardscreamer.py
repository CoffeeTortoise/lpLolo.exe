from constants import ct_size, ct_wndSize, ct_yellow, ct_red, ct_scarlett
from constants import ct_black
from lizardspaths import lp_claw1, lp_claw2, lp_fight_snd
from animatedscreamers import LizardsMouth
from baseclasses import Block, ScreamScene
from screamerbar import ScreamerBar
from rectmotion import Patrol
import pygame as pg


class LizardScreamer(ScreamScene):
    def __init__(self, surface):
        super().__init__(surface)
        mo_w, mo_h = ct_size*13, ct_size*16
        mo_x, mo_y = ct_size*17, ct_size
        self.mouth = LizardsMouth(mo_w, mo_h, (mo_x, mo_y))
        claw_w, claw_h = ct_size*15, ct_size*15
        cl_x1, cl_y, cl_x2 = ct_size*3, ct_wndSize[1]-ct_size*20, ct_size*28.5
        self.claw1 = Block(claw_w, claw_h, (cl_x1, cl_y), lp_claw1)
        self.claw2 = Block(claw_w, claw_h, (cl_x2, cl_y), lp_claw2)
        floor, speed = ct_wndSize[1]-ct_size*15, ct_size*6
        self.motion1 = Patrol(self.claw1.rect, False, speed,
                              top=cl_y, bottom=floor)
        self.motion2 = Patrol(self.claw2.rect, False, speed,
                              top=cl_y, bottom=floor)
        db_x, db_y = cl_x1 + self.claw1.width, ct_wndSize[1] - ct_size*5
        db_w, db_h = ct_size*11, ct_size*2
        self.bar = ScreamerBar(db_w, db_h, ct_yellow, ct_red, (db_x, db_y))
        text = 'Hold the \'space\'' if (self.ru == 0) else 'Зажми пробел'
        self.text = self.base_fnt.render(text, 1, ct_black)
        self.text_pos = (db_x, db_y-ct_size*2)
        self.sound, self.time_period = pg.mixer.Sound(lp_fight_snd), .7

    def behaviour(self):
        if not self.ended:
            self.refresh()
            self.play_mus()
            self.drawings()
            self.bar.behaviour(self.surface)

    def refresh(self):
        text = 'Hold the \'space\'' if (self.ru == 0) else 'Зажми пробел'
        self.text = self.base_fnt.render(text, 1, ct_black)

    def penguin_status(self):
        """0 means battle, 1 means the victory of the lizard,
        2 means the victory of the penguin
        """
        res = 0
        if self.bar.full:
            res = 2
        elif self.bar.k <= 0:
            res = 1
        else:
            res = 0
        if (res == 1) or (res == 2):
            self.sound.stop()
            self.ended = True
        return res

    def drawings(self):
        self.surface.fill(ct_scarlett)
        self.surface.blit(self.text, self.text_pos)
        self.mouth.update(self.surface)
        self.move_claw(self.claw1, self.motion1)
        self.claw1.update(self.surface)
        self.move_claw(self.claw2, self.motion2)
        self.claw2.update(self.surface)

    @staticmethod
    def move_claw(claw, motion):
        claw.rect = motion.patrol_v()
        motion.me_rect = (claw.rect, False)

    def reset(self):
        self.ended, self.mute, self.fresh, self.start_mus = False, False, False, False
        self.bar.reset()

    def __del__(self):
        pass
