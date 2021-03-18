import unittest
from core.elementary.physical.force import Force, from_numpy, add_forces
from core.elementary.math.geometry.geometry3d.vector3 import Vector3
import numpy as np


class MyTestCase(unittest.TestCase):
    def test_init(self):
        f = Force(5, application=Vector3(1, 1, 1), target=Vector3(5, 4, 2))
        assert str(f) == '[5, 4, 3, 1]'

    def test_math(self):
        f = Force(5, Vector3(2, 2, 2))
        assert -f == Force(5, Vector3(-2, -2, -2))
        assert f - f == Force(0, Vector3(0, 0, 0))

    def test_add_forces(self):
        f = add_forces([Force(5, Vector3(2, 4, 5)),
                        Force(2, Vector3(7, -1, -4)),
                        Force(8, Vector3(-4, 5, -9))])

        assert f == from_numpy(np.array((2.466887457053267, 0.105616328449975, 2.1188902765805984,
                                         -1.2588418934654486)))

    def test_from_numpy(self):
        f = from_numpy(np.array((1, 2, 3, 4)))
        assert f == Force(1, Vector3(2, 3, 4))

