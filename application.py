from constants import ct_wndSize, ct_beg_path, ct_que_path, ct_lev_path
from languageselector import LanguageSelector
from threedaysbefore import ThreeDays
from introduction import Introduction
from saveload import SaveLoad
from prebegin import PreBegin
from levelone import LevelOne
from menu import Menu
import pygame as pg
pg.mixer.pre_init(44100, -16, 5, 512)
pg.init()


class Application:
    def __init__(self):
        self.running = True
        self.surface = pg.display.set_mode(ct_wndSize, pg.HWSURFACE)
        SaveLoad.save(ct_que_path, str(0))
        self.beg = int(SaveLoad.load(ct_beg_path))
        self.que = int(SaveLoad.load(ct_que_path))
        self.lev = int(SaveLoad.load(ct_lev_path))
        scene10 = LanguageSelector(self.surface)
        scene11 = Introduction(self.surface)
        scene12 = ThreeDays(self.surface)
        scene13 = Introduction(self.surface)
        scene13.scened = True
        self.scenes1 = [scene10, scene11, scene12, scene13]
        scene20 = Menu(self.surface)
        scene21 = PreBegin(self.surface)
        scene22 = LevelOne(self.surface)
        self.scenes2 = [scene20, scene21, scene22]
        self.clock = pg.time.Clock()
        self.fps = self.scenes1[0].fps

    def run_app(self):
        while self.running:
            if self.beg == 1:
                self.queue_one()
            else:
                self.queue_two()
            self.clock.tick(self.fps)

    def queue_one(self):
        if self.que == 0:
            self.run_scene(self.scenes1[0])
        elif self.que == 1:
            self.run_scene(self.scenes1[1])
        elif self.que == 2:
            self.run_scene(self.scenes1[2])
        elif self.que == 3:
            self.run_scene(self.scenes1[3])
        elif self.que == 4:
            SaveLoad.save(ct_beg_path, '0')
            SaveLoad.save(ct_que_path, '0')
            self.refresh()
        else:
            self.quit()

    def queue_two(self):
        if self.que == 0:
            self.run_scene(self.scenes2[0])
        elif self.que == 1:
            self.run_scene(self.scenes2[1])
        elif self.que == 2:
            self.run_scene(self.scenes2[2])
        else:
            self.quit()

    def run_scene(self, scene):
        if not scene.ended:
            self.fps = scene.fps
            scene.behaviour()
        else:
            self.refresh()

    def refresh(self):
        self.beg = int(SaveLoad.load(ct_beg_path))
        self.que = int(SaveLoad.load(ct_que_path))
        self.lev = int(SaveLoad.load(ct_lev_path))

    def quit(self):
        self.refresh()
        self.running = False
        pg.quit()

    def __del__(self):
        pass
