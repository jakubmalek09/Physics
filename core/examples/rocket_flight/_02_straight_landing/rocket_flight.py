from core.elementary.math.geometry.geometry3d.vector3 import Vector3
from core.examples.rocket_flight._02_straight_landing.f9 import Falcon9
from core.examples.rocket_flight.earth import earth
from core.simulate import SimulationReal
from core.visual import RenderInfo

if __name__ == '__main__':
    s = SimulationReal([
        earth,
        Falcon9(Vector3(0, 6371000 + 30000, 0), Vector3(0, 0, 0))
    ], RenderInfo(1000000, 0.001, 'sim', 10), visualize=False, dt=0.01)
    s.run()
