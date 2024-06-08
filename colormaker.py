

class ColorMaker:
    def __init__(self, speed):
        self.speed = speed
        self.r = 0
        self.g = 0
        self.b = 0

    def make_red(self):
        self.make_green_zero()
        self.make_blue_zero()
        if self.r < 255:
            self.r += self.speed
        res = (int(self.r), int(self.g), int(self.b))
        return res

    def make_green(self):
        self.make_red_zero()
        self.make_blue_zero()
        if self.g < 255:
            self.g += self.speed
        res = (int(self.r), int(self.g), int(self.b))
        return res

    def make_blue(self):
        self.make_red_zero()
        self.make_green_zero()
        if self.b < 255:
            self.b += self.speed
        res = (int(self.r), int(self.g), int(self.b))
        return res
    
    def make_red_zero(self):
        if self.r != 0:
            if self.r > 0:
                self.r -= self.speed
            else:
                self.r += self.speed

    def make_green_zero(self):
        if self.g != 0:
            if self.g > 0:
                self.g -= self.speed
            else:
                self.g += self.speed

    def make_blue_zero(self):
        if self.b != 0:
            if self.b > 0:
                self.b -= self.speed
            else:
                self.b += self.speed

    def __del__(self):
        pass
