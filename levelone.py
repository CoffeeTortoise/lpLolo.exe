from blockpaths import bs_ubuntu_logo, bs_collect_snd, bs_bld_drip
from constants import ct_wndSize, ct_size, ct_black
from othermuspaths import mu_lvl_one
from stagethree import StageThree
from stagefour import StageFour
from stagefive import StageFive
from bogeyman import Bogeyman
from stageone import StageOne
from stagetwo import StageTwo
from solidblocks import Coin
from level import Level
from timer import Timer
from drip import Drip
import pygame as pg


class LevelOne(Level):
    def __init__(self, surface):
        super().__init__(surface)
        stage1 = StageOne(self.surface, self.penguin)
        stage2 = StageTwo(self.surface, self.penguin)
        stage3 = StageThree(self.surface, self.penguin)
        stage4 = StageFour(self.surface, self.penguin)
        stage5 = StageFive(self.surface, self.penguin)
        self.stages = [stage1, stage2, stage3, stage4, stage5]
        self.ubs = []
        co_x, co_y = ct_size*10, ct_wndSize[1]-ct_size*4
        for i in range(6):
            x_co = co_x + ct_size*i
            ubuntu = Coin(ct_size, ct_size, (x_co, co_y),
                        bs_ubuntu_logo, bs_collect_snd)
            self.ubs.append(ubuntu)
        top, line, bottom = -ct_size * 30, 0, ct_wndSize[1] - ct_size
        begin, end = -ct_size * 5, ct_wndSize[0] + ct_size * 5
        for i in range(300):
            drip = Drip(ct_size * .2, ct_size * .4, bs_bld_drip, top, line, bottom,
                        begin, end, 0)
            self.drips.append(drip)
        self.timer_rain = Timer()
        self.bogeyman = Bogeyman(self.surface, 6)
        self.music = pg.mixer.music
        self.mus_path = mu_lvl_one

    def behaviour(self):
        self.surface.fill(ct_black)
        if self.penguin.alive:
            self.mainloop()
        else:
            self.stop_killed()
        self.change_stage()
        if not self.busy:
            self.bogeyman.mainloop()
        self.increase_fear()
        pg.display.flip()
        self.quit_opts()

    # If penguin doesn't move, monsters and blocks shouldn't move either
    def increase_fear(self):
        if self.bogeyman.on:
            self.paused = True
            self.paralyze_penguin()
            self.transfer_penguin()
            self.put_penguin()
        else:
            self.penguin.movable = True
            self.transfer_penguin()
            self.put_penguin()
            self.paused = False

    def mainloop(self):
        self.false_some_attr()
        self.permanent_death()
        self.start_mus()
        self.mus_stopper()
        self.rain()
        self.get_data()
        self.define_stages()
        self.draw_health()
        self.coin_bar.show_coins(self.coins)
        self.draw_coins()

    def rain(self):
        time = self.timer_rain.get_time()
        self.timer_rain.restart()
        for drip in self.drips:
            drip.speed = ct_size*time*1100
            drip.update(self.surface)

    def draw_coins(self):
        for coin in self.ubs:
            coin.update(self.surface)
            self.coins = coin.collect(self.coins, self.penguin)

    def false_some_attr(self):
        for stage in self.stages:
            if not stage.active:
                if hasattr(stage, 'masher_loaded'):
                    stage.masher_loaded = False
                if hasattr(stage, 'sanctuary'):
                    stage.reset_sanctuary()

    def __del__(self):
        pass
