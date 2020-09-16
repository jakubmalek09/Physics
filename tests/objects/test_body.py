import unittest
from core.objects.body import Body
from core.elementary.vector3 import Vector3
from core.objects.collision.ball_collider import BallCollider


class MyTestCase(unittest.TestCase):
    def test_check_collision(self):
        a = Body(BallCollider(5), 5, Vector3(0, 0, 0), Vector3(0, 0, 0))
        b = Body(BallCollider(5), 5, Vector3(0, 0, 0), Vector3(0, 0, 0))

        assert a.check_collision(b) == True
