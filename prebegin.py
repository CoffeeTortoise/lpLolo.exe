from othermuspaths import mu_prebeg_mus
from lizardscene import LizardScene
from turtlescene import TurtleScene
from demonscene import DemonScene
from constants import ct_fps2
from baseclasses import Scene
import pygame as pg


class PreBegin(Scene):
    def __init__(self, surface):
        super().__init__(ct_fps2, surface)
        self.lizards = LizardScene()
        self.turtles = TurtleScene()
        self.demons = DemonScene()
        self.music = pg.mixer.music
        self.mus_path = mu_prebeg_mus

    def behaviour(self):
        self.start_mus()
        self.get_data()
        self.scenes()
        pg.display.flip()
        self.quit_opts()

    def scenes(self):
        if not self.lizards.ended:
            self.lizards.behaviour(self.surface)
        elif not self.turtles.ended:
            self.turtles.behaviour(self.surface)
        elif not self.demons.ended:
            self.demons.behaviour(self.surface)
        else:
            self.ended = True
            self.que = 2

    def __del__(self):
        pass
