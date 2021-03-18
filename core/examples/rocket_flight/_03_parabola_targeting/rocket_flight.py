from core.elementary.math.geometry.geometry3d.vector3 import Vector3
from core.examples.rocket_flight._03_parabola_targeting.ball import Ball
from core.examples.rocket_flight._03_parabola_targeting.f9 import Falcon9
from core.examples.rocket_flight.earth import earth
from core.simulate import SimulationReal
from core.visual import RenderInfo

if __name__ == '__main__':
    s = SimulationReal([
        earth,
        # Ball(10, 10, Vector3(0, 6371000 + 30000, 0), Vector3(0, 0, 0), Vector3(0, 0, 0),
        #      Vector3(0, 0, 0), Vector3(0, 0, 0), Vector3(0, 0, 0), 1)
        Falcon9(Vector3(0, 6371000 + 100000, 0), Vector3(0, 0, 0))
    ], RenderInfo(1000000, 0.001, 'sim', 10), visualize=False, dt=1)
    s.run()
