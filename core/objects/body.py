import numpy as np
from core.objects.collision.collider import Collider
from core.objects.collision.ball_collider import BallCollider
from core.elementary.vector3 import Vector3
from core.elementary.force import Force


class Body:
    """
    Base class for all celestial bodies
    """
    def __init__(self, mass: float, position: Vector3, velocity: Vector3, acceleration: Vector3, rotation: Vector3,
                 ang_velocity: Vector3, ang_acceleration: Vector3, collider: Collider, name=None, color=(80, 80, 80),
                 orbit=None):
        self.collider = collider
        self.mass = mass
        self.position = position
        self.rotation = rotation
        self.velocity = velocity
        self.acceleration = acceleration
        self.ang_velocity = ang_velocity
        self.ang_acceleration = ang_acceleration
        self.name = name
        self.color = color
        self.orbit = orbit

    def crush(self, target):
        pass

    def check_collision(self, other) -> bool:
        return self.collider.check_collision(self, other)

    def apply_force(self, force: Force) -> None:
        """
        For now the force can be only applied to the centre of the mass
        :param force: Force applied to the object
        """
        forces = force.to_components()
        self.acceleration.x += forces[0] / self.mass
        self.acceleration.y += forces[1] / self.mass
        self.acceleration.z += forces[2] / self.mass

    def actualize_loop(self, dt: float) -> None:
        """
        Actualizes position, velocity, acceleration, rotation, angular velocity, angular acceleration etc
        :param dt:
        """
        self.position.x += self.velocity.x * dt + self.acceleration.x * dt ** 2 / 2
        self.position.y += self.velocity.y * dt + self.acceleration.y * dt ** 2 / 2
        self.position.z += self.velocity.z * dt + self.acceleration.z * dt ** 2 / 2

        self.velocity.x += self.acceleration.x * dt
        self.velocity.y += self.acceleration.y * dt
        self.velocity.z += self.acceleration.z * dt

        self.acceleration.x = 0
        self.acceleration.y = 0
        self.acceleration.z = 0

    def destroy(self):
        pass
