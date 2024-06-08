from math import sqrt, pow, acos
from sys import exit


# The argument should be a tuple or list
class Point:
    def __init__(self, pos):
        self.pos = pos

    def __del__(self):
        pass


# For these vectors use points
class Vector:
    def __init__(self, point1, point2):
        self.point1 = point1.pos
        self.point2 = point2.pos
        self.d = len(self.point1)

    def get_cords(self):
        cords = list()
        for i in range(self.d):
            cord = self.point2[i]-self.point1[i]
            cords.append(cord)
        return cords

    def modulus(self):
        s, cords = 0, self.get_cords()
        for i in range(self.d):
            n = pow(cords[i], 2)
            s += n
        return sqrt(s)

    def scalar_product(self, other):
        res = 0
        my_cords = self.get_cords()
        they_cords = other.get_cords()
        for i in range(self.d):
            n = my_cords[i] * they_cords[i]
            res += n
        return res

    def cos_between(self, other):
        scalar_product = self.scalar_product(other)
        my_modul, they_modul = self.modulus(), other.modulus()
        res = scalar_product/(my_modul*they_modul)
        return res

    def angle_between(self, other):
        """ Returns angle in rad"""
        angle = acos(self.cos_between(other))
        return angle

    def __add__(self, other):
        res = list()
        my_cords = self.get_cords()
        they_cords = other.get_cords()
        if self.d == other.d:
            for i in range(self.d):
                n = my_cords[i] + they_cords[i]
                res.append(n)
            return res
        else:
            exit(1)

    def __radd__(self, other):
        res = list()
        my_cords = self.get_cords()
        they_cords = other.get_cords()
        if self.d == other.d:
            for i in range(self.d):
                n = my_cords[i] + they_cords[i]
                res.append(n)
            return res
        else:
            exit(1)

    def __sub__(self, other):
        res = list()
        my_cords = self.get_cords()
        they_cords = other.get_cords()
        if self.d == other.d:
            for i in range(self.d):
                n = my_cords[i] - they_cords[i]
                res.append(n)
            return res
        else:
            exit(1)

    def __rsub__(self, other):
        res = list()
        my_cords = self.get_cords()
        they_cords = other.get_cords()
        if self.d == other.d:
            for i in range(self.d):
                n = they_cords[i] - my_cords[i]
                res.append(n)
            return res
        else:
            exit(1)

    def __mul__(self, other):
        if self.d == other.d:
            res = self.scalar_product(other)
            return res
        else:
            exit(1)

    def __rmul__(self, other):
        if self.d == other.d:
            res = self.scalar_product(other)
            return res
        else:
            exit(1)

    # Cosinus between vectors
    def __truediv__(self, other):
        if self.d == other.d:
            res = self.cos_between(other)
            return res
        else:
            exit(1)

    def __rtruediv__(self, other):
        if self.d == other.d:
            res = self.cos_between(other)
            return res
        else:
            exit(1)

    def __eq__(self, other):
        my_modul, they_modul = self.modulus(), other.modulus()
        if (my_modul == they_modul) and (self.d == other.d):
            return True
        else:
            return False

    def __qt__(self, other):
        my_modul, they_modul = self.modulus(), other.modulus()
        if my_modul > they_modul:
            return True
        else:
            return False

    def __lt__(self, other):
        my_modul, they_modul = self.modulus(), other.modulus()
        if my_modul < they_modul:
            return True
        else:
            return False

    def __del__(self):
        pass
