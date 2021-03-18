import unittest

from core.elementary.physical.force import Force
from core.objects.body import Body
from core.elementary.math.geometry.geometry3d.vector3 import Vector3
from core.objects.collision.ball_collider import BallCollider


class MyTestCase(unittest.TestCase):

    def test_apply_force(self):
        body = Body(5, 1, Vector3(0, 0, 0), Vector3(0, 0, 0), Vector3(0, 0, 0), Vector3(0, 0, 0),
                    Vector3(0, 0, 0), Vector3(0, 0, 0), BallCollider(5))
        # body.apply_force(Force(1, Vector3(-1, 0, 0), Vector3(0, -1, 0)))
        body.apply_force(Force(1, Vector3(0, 1, 0), Vector3(0, -1, 0)))
        print(body.acceleration, body.ang_acceleration)

    def test_check_collision(self):
        a = Body(5, 1, Vector3(0, 0, 0), Vector3(0, 0, 0), Vector3(0, 0, 0), Vector3(0, 0, 0),
                 Vector3(0, 0, 0), Vector3(0, 0, 0), BallCollider(5))
        b = Body(5, 1, Vector3(0, 0, 0), Vector3(0, 0, 0), Vector3(0, 0, 0), Vector3(0, 0, 0),
                 Vector3(0, 0, 0), Vector3(0, 0, 0), BallCollider(5))

        assert a.check_collision(b) == True
