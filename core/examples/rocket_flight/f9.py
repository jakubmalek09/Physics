from .engine import Engine
from .rocket import Rocket
from core.elementary.math.geometry.geometry3d.vector3 import Vector3


class Falcon9(Rocket):

    def __init__(self, position: Vector3, rotation: Vector3):
        super().__init__(50, 50, position, Vector3(0, 0, 0), Vector3(0, 0, 0), rotation,
                         Vector3(0, 0, 0), Vector3(0, 0, 0), None, Engine(
                fuel_mass=1000,
                isp=3000,
                fps=5,
                fuel='rp1',
                relative_position=Vector3(0, -2, 0),
                force_angle=Vector3(90, 0, 0),
                vectoring_angle=5,
                power_percentage=1
            ))

    def actualize_loop(self, dt: float) -> None:
        super().actualize_loop(dt)
