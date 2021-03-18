from core.elementary.math.geometry.geometry2d.vector2 import Vector2
from core.elementary.math.geometry.geometry3d.vector3 import Vector3
from core.objects.body import Body
from core.objects.collision.ball_collider import BallCollider


class Spherical(Body):
    """
    Enables to use GPS like coordinate system on the body
    """

    def __init__(self, mass: float, inertia_momentum: float, position: Vector3, velocity: Vector3,
                 acceleration: Vector3, rotation: Vector3, ang_velocity: Vector3, ang_acceleration: Vector3,
                 radius: float):
        super().__init__(mass, inertia_momentum, position, velocity, acceleration, rotation, ang_velocity,
                         ang_acceleration, BallCollider(radius))

    def coords(self, point: Vector3) -> (Vector2, float):
        pass

    def point_from_coords(self, coords: Vector2, height: float = 0) -> Vector3:
        pass
