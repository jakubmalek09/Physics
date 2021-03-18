from copy import deepcopy

from core.elementary.math.geometry.geometry3d.vector3 import Vector3
from core.objects.body import Body
from core.objects.collision.ball_collider import BallCollider
from core.objects.collision.collider import Collider


class Ball(Body):
    def __init__(self, mass: float, inertia_momentum: float, position: Vector3, velocity: Vector3,
                 acceleration: Vector3, rotation: Vector3, ang_velocity: Vector3, ang_acceleration: Vector3,
                 radius: float):
        self.__start_position = deepcopy(position)
        super().__init__(mass, inertia_momentum, position, velocity, acceleration, rotation, ang_velocity,
                         ang_acceleration, BallCollider(radius))

    def actualize_loop(self, dt: float) -> None:
        print(self.position - self.__start_position)

        super().actualize_loop(dt)

    def on_collided(self, target):
        print(self.position - self.__start_position)
        raise Exception()


class SimBall(Body):
    def __init__(self, mass: float, inertia_momentum: float, position: Vector3, velocity: Vector3,
                 acceleration: Vector3, rotation: Vector3, ang_velocity: Vector3, ang_acceleration: Vector3,
                 collider: Collider):
        super().__init__(mass, inertia_momentum, position, velocity, acceleration, rotation, ang_velocity,
                         ang_acceleration, collider)
