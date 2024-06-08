from baseclasses import RectMotion
from math import sin, cos, pi
from timer import Timer


class CircleMotion(RectMotion):
    def __init__(self, rect, is_entity, speed, center, radius):
        super().__init__(rect, is_entity, speed)
        self.t1 = pi * 2
        self.t2 = -pi * 2
        self.center, self.radius = center, radius

    @property
    def round(self):
        return self.center, self.radius

    @round.setter
    def round(self, data):     # data is a tuple: (center, radius)
        self.center, self.radius = data[0], data[1]

    def circle(self, by_hour):
        time = self.timer.get_time()
        self.timer.restart()
        speed = self.speed
        self.speed *= time * 100
        if by_hour:
            self.by_hour()
        else:
            self.counterclockwise()
        t = self.t2 if by_hour else self.t1
        self.rect.left = self.center[0] + self.radius * cos(t)
        self.rect.top = self.center[1] + self.radius * sin(t)
        self.speed = speed
        return self.rect

    def counterclockwise(self):
        self.t1 -= self.speed
        if self.t1 <= 0:
            self.t1 = pi * 2

    def by_hour(self):
        self.t2 += self.speed
        if self.t2 >= 0:
            self.t2 = -pi * 2

    def __del__(self):
        pass


class Patrol(RectMotion):
    def __init__(self, rect, is_entity, speed, begin=None, end=None, top=None, bottom=None):
        super().__init__(rect, is_entity, speed)
        self.begin, self.end = begin, end
        self.top, self.bottom = top, bottom
        self.pp_h, self.pp_v = False, False
        self.timer2 = Timer()

    @property
    def begin_end(self):
        return self.begin, self.end

    @begin_end.setter
    def begin_end(self, new):
        self.begin, self.end = new[0], new[1]

    @property
    def top_bottom(self):
        return self.top, self.bottom

    @top_bottom.setter
    def top_bottom(self, new):
        self.top, self.bottom = new[0], new[1]

    def patrol_h(self):
        time, pos = self.timer.get_time(), self.rect.left
        self.timer.restart()
        speed = self.speed
        self.speed *= time
        if (pos <= self.begin) and not self.pp_h:
            self.rect.move_ip(self.speed, 0)
        elif ((pos >= self.begin) and (pos < self.end)) and not self.pp_h:
            self.rect.move_ip(self.speed, 0)
        elif (pos >= self.end) and not self.pp_h:
            self.pp_h = True
        elif (pos >= self.end) and self.pp_h:
            self.rect.move_ip(-self.speed, 0)
        elif ((pos <= self.end) and (pos > self.begin)) and self.pp_h:
            self.rect.move_ip(-self.speed, 0)
        elif (pos <= self.begin) and self.pp_h:
            self.rect.move_ip(-self.speed, 0)
            self.pp_h = False
        else:
            self.rect.move_ip(0, 0)
        self.speed = speed
        return self.rect

    def patrol_v(self):
        time, pos = self.timer2.get_time(), self.rect.top
        self.timer2.restart()
        speed = self.speed
        self.speed *= time
        if (pos <= self.top) and not self.pp_v:
            self.rect.move_ip(0, self.speed)
        elif ((pos >= self.top) and (pos < self.bottom)) and not self.pp_v:
            self.rect.move_ip(0, self.speed)
        elif (pos >= self.bottom) and not self.pp_v:
            self.pp_v = True
        elif (pos >= self.bottom) and self.pp_v:
            self.rect.move_ip(0, -self.speed)
        elif ((pos <= self.bottom) and (pos > self.top)) and self.pp_v:
            self.rect.move_ip(0, -self.speed)
        elif (pos <= self.top) and self.pp_v:
            self.rect.move_ip(0, -self.speed)
            self.pp_v = False
        else:
            self.rect.move_ip(0, 0)
        self.speed = speed
        return self.rect

    def __del__(self):
        pass


class SinMotion(RectMotion):
    def __init__(self, rect, is_entity, speed, a=0, b=1, c=1, d=0, is_to_left=False):
        """The large the 'a', the higher the graph rises.
        The more 'b' increases, the more the amplitude increases.
        As 'c' increases, the oscillation frequency increases.
        When increasing 'd', the graph moves in the negative direction
        of the abscissa axis.
        By default, 'a' and 'd' set to 0, 'b' and 'c' set to 1.
        """
        super().__init__(rect, is_entity, speed)
        self.a, self.b, self.c, self.d = a, b, c, d
        self.to_left = is_to_left
        if not self.to_left:
            if self.speed < 0:
                self.speed *= -1
        else:
            if self.speed > 0:
                self.speed *= -1

    @property
    def abcd(self):
        return self.a, self.b, self.c, self.d

    @abcd.setter
    def abcd(self, abcd):
        self.a, self.b, self.c, self.d = abcd[0], abcd[1], abcd[2], abcd[3]

    def move(self):
        time = self.timer.get_time()
        self.timer.restart()
        x = self.rect.left + self.speed*time
        self.rect.top = self.a + self.b*sin(self.c*x + self.d)
        self.rect.left = x
        return self.rect

    def __del__(self):
        pass


class CosMotion(SinMotion):
    def __init__(self, rect, is_entity, speed, a=0, b=1, c=1, d=0, is_to_left=True):
        super().__init__(rect, is_entity, speed, a, b, c, d, is_to_left)

    def move(self):
        time = self.timer.get_time()
        self.timer.restart()
        x = self.rect.left + self.speed * time
        self.rect.top = self.a + self.b*cos(self.c*x + self.d)
        self.rect.left = x
        return self.rect

    def __del__(self):
        pass
