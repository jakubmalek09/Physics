from core.elementary.math.geometry.geometry3d.vector3 import Vector3
from math import sqrt
import numpy as np


class Force:
    def __init__(self, value, vector, application=None):
        """
        Any forced applied to any body
        No need to give all 4 values.
        If vector isn't given, it will be computed from application and target vectors
        :type value: float
        :type vector: Vector3
        :type application: Vector3
        :param value: Value of the force
        :param vector: Direction to apply the force. These values are only relatable and have no unit
        :param application: Point of the force application; if none the force is applied to the center of the mass
        """
        if value < 0 or (type(value) is not int and type(value) is not float):
            raise ValueError('Force value must be positive integer or float')
        self.__value = value
        self.__vector = vector.unit
        self.__application = application

    @property
    def components(self):
        w = self.vector.length
        if w == 0:
            return 0, 0, 0
        fx = self.vector.x / w * self.value
        fy = self.vector.y / w * self.value
        fz = self.vector.z / w * self.value

        return fx, fy, fz

    @property
    def force_x(self):
        return Force(self.components[0], Vector3(self.components[0], 0, 0))

    @property
    def force_y(self):
        return Force(self.components[1], Vector3(0, self.components[1], 0))

    @property
    def force_z(self):
        return Force(self.components[2], Vector3(0, 0, self.components[2]))

    @property
    def value(self):
        return self.__value

    @property
    def vector(self):
        return self.__vector

    @property
    def application(self):
        return self.__application

    def __sub__(self, other):
        return self + (-other)

    def __add__(self, other: 'Force'):
        fx = self.vector.x * self.value
        fy = self.vector.y * self.value
        fz = self.vector.z * self.value

        fx2 = other.vector.x * other.value
        fy2 = other.vector.y * other.value
        fz2 = other.vector.z * other.value

        fx += fx2
        fy += fy2
        fz += fz2

        return Force(sqrt(fx ** 2 + fy ** 2 + fz ** 2), Vector3(fx, fy, fz), self.application)

    def __neg__(self):
        return Force(self.value, Vector3(-self.vector.x, -self.vector.y, -self.vector.z))

    def __eq__(self, other):
        return self.value == other.value and self.vector.x == other.vector.x and self.vector.y == other.vector.y and \
               self.vector.z == other.vector.z

    def __str__(self):
        return '[{}, {}, {}, {}]'.format(self.value, self.vector.x, self.vector.y, self.vector.z)


def add_forces(forces):
    fx = 0
    fy = 0
    fz = 0
    for force in forces:
        w = sqrt(force.vector.x ** 2 + force.vector.y ** 2 + force.vector.z ** 2)
        fxp = force.value * force.vector.x / w
        fyp = force.value * force.vector.y / w
        fzp = force.value * force.vector.z / w
        fx += fxp
        fy += fyp
        fz += fzp
    fx /= len(forces)
    fy /= len(forces)
    fz /= len(forces)

    return Force(sqrt(fx ** 2 + fy ** 2 + fz ** 2), Vector3(fx, fy, fz))


def from_numpy(arr):
    if arr.dtype != np.int and arr.dtype != np.float:
        raise ValueError('Array data type must be int or float')
    return Force(arr[0], Vector3(arr[1], arr[2], arr[3]))
