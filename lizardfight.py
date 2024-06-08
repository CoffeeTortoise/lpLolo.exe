from lizardvspenguin import PenguinWin, LizardWin
from lizardscreamer import LizardScreamer
from deathscene import DeathScene


class LizardFight(DeathScene):
    def __init__(self, surface):
        super().__init__(surface)
        self.l_screamer = LizardScreamer(surface)
        self.p_win = PenguinWin(surface)
        self.l_win = LizardWin(surface)
        self.queue, self.result = 0, None

    def behaviour(self):
        if not self.ended:
            self.fighting()
            if self.queue == 1:
                self.result = self.p_win
            elif self.queue == 2:
                self.result = self.l_win
            else:
                pass

    def choice(self):
        if self.queue == 0:
            return 0
        else:
            if not self.result.ended:
                self.result.behaviour()
                return 0
            else:
                self.l_screamer.sound.stop()
                self.result.sound.stop()
                return self.queue

    def fighting(self):
        if self.queue == 0:
            self.l_screamer.behaviour()
            self.state = self.l_screamer.penguin_status()
            if self.l_screamer.ended:
                self.solve_queue()

    def solve_queue(self):
        if not self.defined:
            if self.state == 2:
                self.queue = 1
            elif self.state == 1:
                self.queue = 2
            else:
                self.queue = 0
            if self.queue != 0:
                self.defined = True

    def __del__(self):
        pass
