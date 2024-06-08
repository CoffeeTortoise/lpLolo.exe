import time as tm


class Timer:
    def __init__(self):
        self.remember = 0
        self.timeCntr = 0
        self.switch = False

    def get_time(self):        # returns time in seconds
        if not self.switch:
            self.remember = tm.time()
            self.switch = True
        else:
            current_time = tm.time()
            elapsed_time = current_time - self.remember
            self.timeCntr += elapsed_time
            self.switch = False
        return self.timeCntr        # every time increases by ~0.15

    def restart(self):
        if self.timeCntr != 0:
            self.timeCntr = 0
            self.remember = 0
            self.switch = False

    def __del__(self):
        pass
