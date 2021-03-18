from math import sqrt

import ratcave as rc

from core.elementary.physical.force import Force
from core.elementary.math.geometry.geometry3d.vector3 import Vector3
from core.objects.collision.collider import Collider


class Body:
    """
    Base class for all celestial bodies
    """

    def __init__(self, mass: float, inertia_momentum: float, position: Vector3, velocity: Vector3, acceleration:
                 Vector3, rotation: Vector3, ang_velocity: Vector3, ang_acceleration: Vector3, collider: Collider,
                 mesh=None, name=None, color=(80, 80, 80), orbit=None, visual=True):
        """

        :param mass:
        :param position:
        :param velocity:
        :param acceleration:
        :param rotation: In radians
        :param ang_velocity:
        :param ang_acceleration:
        :param collider:
        :param mesh:
        :param name:
        :param color:
        :param orbit:
        """
        self.collider = collider
        self.mass = mass
        self.inertia = inertia_momentum
        self.position = position
        self.rotation = rotation
        self.velocity = velocity
        self.acceleration = acceleration
        self.ang_velocity = ang_velocity
        self.ang_acceleration = ang_acceleration
        self.name = name
        self.color = color
        self.orbit = orbit
        self.mesh = mesh
        if visual:
            if mesh is None:
                obj_filename = rc.resources.obj_primitives
                obj_reader = rc.WavefrontReader(obj_filename)
                self.mesh = obj_reader.get_mesh('Sphere')

    def on_collided(self, target):
        pass

    def check_collision(self, other) -> bool:
        if self.collider is None:
            return False
        return self.collider.check_collision(self, other)

    def apply_force(self, force: Force) -> None:
        """

        :param force: Force applied to the object
        """
        # todo this code is so shitty (use force instead of vector3 to describe force)
        if force.application is None:
            self.apply_translation_force(force)
        else:
            translation_vector = self.position - force.application
            xa, ya, za = force.vector.x, force.vector.y, force.vector.z
            xb, yb, zb = translation_vector.x, translation_vector.y, translation_vector.z
            cosa = ((xa * xb + ya * yb + za * zb) / (sqrt(xa ** 2 + ya ** 2 + za ** 2) *
                                                     sqrt(xb ** 2 + yb ** 2 + zb ** 2)))
            if cosa == 0:
                rotation_force = force.vector * force.value
                translation_force = Vector3(0, 0, 0)
            else:
                translation_force = force.vector * force.value * abs(cosa)
                rotation_force = force.vector - translation_force
            self.apply_translation_force(translation_force)
            self.apply_rotation_force(Force(rotation_force.length, rotation_force, force.application))

    def apply_translation_force(self, force):
        if type(force) == Force:
            forces = force.components
            self.acceleration.x += forces[0] / self.mass
            self.acceleration.y += forces[1] / self.mass
            self.acceleration.z += forces[2] / self.mass
        elif type(force) == Vector3:
            self.acceleration.x += force.x / self.mass
            self.acceleration.y += force.y / self.mass
            self.acceleration.z += force.z / self.mass

    def apply_rotation_force(self, f: Force):
        d = f.application - self.position

        self.ang_acceleration -= Vector3.cross_product(f.vector.unit, d).unit * f.value * d.length / self.inertia

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

    def reset(self):
        pass
