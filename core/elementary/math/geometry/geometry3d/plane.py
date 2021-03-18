from core.elementary.math.geometry.geometry3d.vector3 import Vector3
from core.elementary.math.geometry.geometry3d.line import Line3D


class Plane:
    def __init__(self, A: float, B: float, C: float, D: float):
        self.__A = A
        self.__B = B
        self.__C = C
        self.__D = D

    @property
    def A(self):
        return self.__A

    @property
    def B(self):
        return self.__B

    @property
    def C(self):
        return self.__C

    @property
    def D(self):
        return self.__D

    @staticmethod
    def from_normal(point: Vector3, normal: Line3D):
        A = normal.a
        B = normal.b
        C = normal.c
        D = A * point.x + B * point.y + C * point.z
        return Plane(A, B, C, D)
