from shortscenes import Lolo, Family, Joke, StarPainter
from random import randint, seed
from timer import Timer


class Bogeyman:
    def __init__(self, surface, time_lim):
        scene1, scene2 = Lolo(surface), Family(surface)
        scene3, scene4 = Joke(surface), StarPainter(surface)
        self.ended, self.on, self.determined = False, False, False
        self.scenes = [scene1, scene2, scene3, scene4]
        self.active_scene = self.scenes[0]
        self.timer = Timer()
        self.time_lim = time_lim

    def mainloop(self):
        time = self.timer.get_time()
        if time > self.time_lim:
            self.on = True
            self.ended = False
            self.timer.restart()
        if self.on:
            self.behaviour()

    def behaviour(self):
        if not self.ended:
            self.run_scene()
        else:
            self.determined = False
            self.on = False

    def run_scene(self):
        if not self.determined:
            seed()
            n = randint(0, len(self.scenes) - 1)
            self.active_scene = self.scenes[n]
            self.refresh_scene()
            self.determined = True
        else:
            self.active_scene.behaviour()
            self.ended = self.active_scene.ended

    def refresh_scene(self):
        self.active_scene.ended = False
        self.active_scene.mute = False
        self.active_scene.timer.restart()
        if hasattr(self.active_scene, 'booked'):
            self.active_scene.booked = False
        if hasattr(self.active_scene, 'timer2'):
            self.active_scene.timer2.restart()
        if hasattr(self.active_scene, 'determined'):
            self.active_scene.determined = False

    def __del__(self):
        pass
