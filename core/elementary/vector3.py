from math import sqrt


class Vector3:
    def __init__(self, x, y, z):
        """
        Any 3d vector in the simulation e.g. place of object, point of force application etc.
        Values are represented in SI units.
        """
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        if type(other) == Vector3:
            return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            return Vector3(self.x + other, self.y + other, self.z + other)

    def __sub__(self, other):
        if type(other) == Vector3:
            return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
        else:
            return Vector3(self.x - other, self.y - other, self.z - other)

    def __mul__(self, other):
        if type(other) == Vector3:
            return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)
        else:
            return Vector3(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other):
        if type(other) == Vector3:
            return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)
        else:
            return Vector3(self.x * other, self.y * other, self.z * other)

    def __truediv__(self, other):
        if type(other) == Vector3:
            return Vector3(self.x / other.x, self.y / other.y, self.z / other.z)
        else:
            return Vector3(self.x / other, self.y / other, self.z / other)

    def __str__(self):
        return '[{}, {}, {}]'.format(self.x, self.y, self.z)


def distance(vec1: Vector3, vec2: Vector3) -> float:
    return sqrt((vec1.x - vec2.x) ** 2 + (vec1.y - vec2.y) ** 2 + (vec1.z - vec2.z) ** 2)
