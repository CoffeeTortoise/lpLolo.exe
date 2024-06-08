import random as rd


class RandPos:
    @staticmethod
    def rand_num(begin, end):
        res = rd.randint(begin, end)
        return res

    @staticmethod
    def rand_cords(top, bottom, begin, end):
        x = rd.randint(begin, end)
        y = rd.randint(top, bottom)
        res = (x, y)
        return res
