from core.simulate import Simulation
from core.objects.body import Body
from core.elementary.vector3 import Vector3, distance
from core.objects.collision.ball_collider import BallCollider

s = Simulation([
    Body(5.972 * 10 ** 24, Vector3(0, 0, 0), Vector3(0, 0, 0), Vector3(0, 0, 0), Vector3(0, 0, 0), Vector3(0, 0, 0),
         Vector3(0, 0, 0), BallCollider(6371000), 'Earth', color=(160, 160, 160)),
    Body(7.24 * 10 ** 22, Vector3(384400000, 0, 0), Vector3(0, 1018.2890, 0), Vector3(0, 0, 0), Vector3(0, 0, 0),
         Vector3(0, 0, 0), Vector3(0, 0, 0), BallCollider(1737100), 'Moon', orbit='Earth')
], 10)
s.run()
