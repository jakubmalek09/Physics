from core.simulate import SimulationReal
from core.objects.body import Body
from core.elementary.math.geometry.geometry3d.vector3 import Vector3
from core.objects.collision.ball_collider import BallCollider
from core.visual import RenderInfo

s = SimulationReal([
    Body(5.972 * 10 ** 24, Vector3(0, 0, 0), Vector3(0, 0, 0), Vector3(0, 0, 0), Vector3(0, 0, 0),
         Vector3(0, 0, 0), Vector3(0, 0, 0), BallCollider(6371000), name='Earth', color=(160, 160, 160)),
    Body(7.24 * 10 ** 22, Vector3(384400000, 0, 0), Vector3(0, 1018.2890, 0), Vector3(0, 0, 0), Vector3(0, 0, 0),
         Vector3(0, 0, 0), Vector3(0, 0, 0), BallCollider(1737100), name='Moon', orbit='Earth')
], RenderInfo(1000000, 0.001, 'sim', 10), 100)
s.run()


