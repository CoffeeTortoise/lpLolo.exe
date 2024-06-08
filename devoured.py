from turtlepaths import tp_stg1, tp_stg2, tp_stg3, tp_stg4, tp_stg5, tp_stg6
from turtlepaths import tp_c_stay
from constants import ct_size, ct_wndSize, ct_black, ct_red, ct_white
from othersoundpaths import so_slow_clock, so_short_scream_m
from darkenedsouls import ds_slug_faced, ds_slug
from circleentity import CircleEntity
from deathscene import DeathScene
from baseclasses import Block
from timer import Timer
from fire import Fire
import pygame as pg
pg.mixer.pre_init(44100, -16, 3, 512)
pg.init()


class Devoured(DeathScene):
    def __init__(self, surface):
        super().__init__(surface)
        self.sound = pg.mixer.Sound(so_slow_clock)
        self.timer_beg = Timer()
        self.time_mus_co = 10
        self.penguin.rect.top -= ct_size*8
        self.lizard.rect.top -= ct_size*8
        self.turtle.rect.top -= ct_size*8
        c_center, c_rad = (ct_size*24, ct_size*5), ct_size*5
        self.circle = CircleEntity(c_rad, ct_white, c_center)
        self.screamed, self.creamed = False, False
        self.scream = pg.mixer.Sound(so_short_scream_m)
        sf_w, sf_h = ct_size*18, ct_size*20
        sf_x, sf_y = ct_size*14, ct_size
        self.screamer = Block(sf_w, sf_h, (sf_x, sf_y), ds_slug_faced)
        fire_path = [tp_stg1, tp_stg2, tp_stg3, tp_stg4, tp_stg5, tp_stg6]
        f_w, f_h = ct_size*3, ct_size*6
        f_x, f_y = ct_size*22.5, ct_wndSize[1]-ct_size*13
        self.fire = Fire(fire_path, f_w, f_h, (f_x, f_y))
        self.fire.sound_on = False
        sd_w, sd_h = ct_size*1.5, ct_size*5
        sd_x1, sd_y = ct_size*20, ct_size*2
        self.slug1 = Block(sd_w, sd_h, (sd_x1, sd_y), ds_slug)
        sd_x2 = sd_x1+ct_size*6.5
        self.slug2 = Block(sd_w, sd_h, (sd_x2, sd_y), ds_slug)
        self.slug2.image = pg.transform.flip(self.slug2.image, True, False)
        self.cultists = []
        cs_w, cs_h = ct_size*3, ct_size*5
        cs_x, cs_y = -ct_size, ct_wndSize[1]-ct_size*12
        for i in range(13):
            x = cs_x + (cs_w+ct_size)*i
            if (x > f_x) and (x < (f_x + f_w)):
                continue
            else:
                cultist = Block(cs_w, cs_h, (x, cs_y), tp_c_stay)
                if x >= (f_x + f_w):
                    cultist.image = pg.transform.flip(cultist.image, True, False)
                self.cultists.append(cultist)
        self.timer_exec = Timer()

    def behaviour(self):
        if not self.ended:
            if self.creamed:
                self.refresh()
                self.start_mus()
                self.drawings()
            else:
                self.show_screamer()

    def drawings(self):
        self.surface.fill(ct_black)
        self.glitch()
        self.circle.draw(self.surface)
        self.penguin.update(self.surface)
        self.slug1.update(self.surface)
        self.slug2.update(self.surface)
        self.execution()
        if self.state != 2:
            self.fire.update(self.surface)
        self.set_cult()
        self.draw_opts()

    def execution(self):
        if self.state == 2:
            time = self.timer_exec.get_time()
            if time > 2:
                # self.executed = True
                self.ended = True

    def set_cult(self):
        for cultist in self.cultists:
            cultist.update(self.surface)

    def show_screamer(self):
        time = self.timer_beg.get_time()
        if time <= 1.7:
            self.surface.fill(ct_red)
            self.screamer.update(self.surface)
            self.yell()
        else:
            self.creamed = True

    def yell(self):
        if not self.screamed:
            self.scream.play()
            self.screamed = True

    def reset(self):
        self.timer_exec.restart()
        self.defined = False
        self.executed, self.merci = False, False
        self.creamed, self.screamed = False, False

    def __del__(self):
        pass
