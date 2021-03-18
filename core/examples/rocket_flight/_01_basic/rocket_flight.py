from core.elementary.math.geometry.geometry3d.vector3 import Vector3
from core.examples.rocket_flight.earth import earth
from core.examples.rocket_flight.f9 import Falcon9
from core.simulate import SimulationReal
from core.visual import RenderInfo

s = SimulationReal([
    earth,
    Falcon9(Vector3(0, 6371000, 0), Vector3(0, 0, 0))  # Have to start the engine
], RenderInfo(1000000, 0.001, 'sim', 10), visualize=False)
s.run()
