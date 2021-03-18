from math import sqrt, atan2, tan, degrees, radians, sin, cos

import numpy as np


class Vector3:
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        """
        Any 3d vector in the simulation e.g. place of object, point of force application etc.
        Values are represented in SI units.
        """
        self.x = x
        self.y = y
        self.z = z

    def to_xyz(self):
        return self.x, self.y, self.z

    @property
    def length(self):
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    @property
    def unit(self):
        if self.length == 0:
            return Vector3(0, 0, 0)
        return self / self.length

    @property
    def ndarray(self):
        return np.array([self.x, self.y, self.z], dtype='float32')

    @property
    def angle_from_vector(self):
        x = degrees(atan2(self.y, self.z))
        y = degrees(atan2(self.x, self.z))
        z = degrees(atan2(self.y, self.x))
        return Vector3(x, y, z)

    @property
    def vector_from_angle(self):
        x = cos(radians(self.y)) * cos(radians(self.x))
        z = sin(radians(self.y)) * cos(radians(self.x))
        y = sin(radians(self.x))
        return Vector3(x, y, z)

    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z)

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

    @staticmethod
    def from_ndarray(arr: np.ndarray) -> 'Vector3':
        return Vector3(arr[0], arr[1], arr[2])

    @staticmethod
    def dot_product(a: 'Vector3', b: 'Vector3'):
        return a.x * b.x + a.y * b.y + a.z * b.z

    @staticmethod
    def cross_product(a: 'Vector3', b: 'Vector3'):
        return Vector3.from_ndarray(np.cross(a.ndarray, b.ndarray))


def distance(vec1: Vector3, vec2: Vector3) -> float:
    return sqrt((vec1.x - vec2.x) ** 2 + (vec1.y - vec2.y) ** 2 + (vec1.z - vec2.z) ** 2)
