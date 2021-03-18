from copy import deepcopy

from core.elementary.physical.force import Force
from core.elementary.math.geometry.geometry3d.vector3 import Vector3
from core.examples.rocket_flight.engine import Engine
from core.objects.body import Body
from core.objects.collision.collider import Collider


class Rocket(Body):

    def __init__(self, mass: float, inertia_momentum: float, position: Vector3, velocity: Vector3,
                 acceleration: Vector3, rotation: Vector3, ang_velocity: Vector3, ang_acceleration: Vector3,
                 collider: Collider, engine: Engine):
        self.__engine = engine
        self.__engine_working = False
        self.__zero_mass = mass
        super().__init__(mass + engine.fuel_mass, inertia_momentum, position, velocity, acceleration, rotation,
                         ang_velocity, ang_acceleration, collider)

    def actualize_loop(self, dt: float) -> None:
        engine_rotation = self.rotation + self.__engine.rotation + self.__engine.force_angle
        if self.__engine_working:
            force = self.__engine.force * engine_rotation.vector_from_angle
            self.__engine.reduce_fuel(dt * self.__engine.fps)

            self.apply_force(Force(
                force.length,
                force.unit,
                self.position + self.__engine.relative_position
            ))

            self.mass = self.__zero_mass + self.__engine.fuel_mass
        else:
            super().actualize_loop(dt)

    @property
    def engine(self) -> Engine:
        return deepcopy(self.__engine)

    def engine_angle(self, angle: Vector3):
        self.__engine.set_vector_angle(angle)

    def engine_on(self) -> None:
        self.__engine_working = True

    def engine_off(self) -> None:
        self.__engine_working = False
