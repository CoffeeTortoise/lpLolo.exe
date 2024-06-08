from timer import Timer


class Animator:
    def __init__(self, frames, fr_t):
        self.timer = Timer()
        self.frames = frames
        self.frT = fr_t
        self.len = len(self.frames)

    def animate(self):
        res = self.frames[0]
        time = self.timer.get_time()
        if time > self.len * self.frT:
            self.timer.restart()
        for i in range(self.len):
            if time >= self.frT*(i+1):
                res = self.frames[i]
        return res

    def __del__(self):
        pass
