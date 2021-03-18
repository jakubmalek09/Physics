from copy import deepcopy

from core.elementary.math.geometry.geometry3d.vector3 import Vector3


class Line3D:
    def __init__(self, point: Vector3, direction: Vector3):
        self.__point = deepcopy(point)
        self.__direction = deepcopy(direction)

    def value_of_t(self, t: float) -> Vector3:
        return self.__point + self.__direction * t

    @property
    def a(self):
        return self.__direction.x

    @property
    def b(self):
        return self.__direction.y

    @property
    def c(self):
        return self.__direction.z

    @property
    def direction(self):
        return deepcopy(self.__direction)

    @property
    def point(self):
        return deepcopy(self.__point)

    @staticmethod
    def from_points(p1: Vector3, p2: Vector3):
        return Line3D(p1, p1 - p2)
