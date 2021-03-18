from cmath import acos, pi
from copy import deepcopy
from math import degrees
from time import time

from core.elementary.math.geometry.geometry3d.crossing import cross_point
from core.elementary.math.geometry.geometry3d.line import Line3D
from core.elementary.math.geometry.geometry3d.plane import Plane
from core.elementary.math.geometry.geometry3d.vector3 import Vector3, distance
from core.examples.rocket_flight.earth import earth_massless, earth
from core.examples.rocket_flight.f9 import Falcon9 as f9
from core.objects.body import Body
from core.objects.collision.ball_collider import BallCollider
from core.simulate import SimulationReal
from core.visual import RenderInfo


class Falcon9(f9):
    """
    Trying to target the parabola into the given place in x coord
    Uses simple condition for checking test ball position that enables the script only to work on short distances
    """
    __g = 9.81
    __dt = 0.01
    __dt_sim = 10
    __target = Vector3(6000000, 0, 0)
    __base: Vector3 = None
    __base_distance = None
    __force_vector = None
    position = None

    def __init__(self, position: Vector3, rotation: Vector3):
        super().__init__(position, rotation)
        start = time()
        self.velocity.x = self.calculate_optimal_velocity()
        print(time() - start)

    def calculate_optimal_velocity(self):
        test_ball = TestBody(Vector3(self.__target.x, self.position.y, 0), Vector3(0, -100, 0), Vector3(),
                             Vector3(), Vector3(), Vector3())
        simulation = SimulationReal([
            earth_massless,
            test_ball
        ], RenderInfo(1000000, 0.001, 'sim', 10), dt=self.__dt_sim, visualize=False)

        self.__target = self.calculate_translation(simulation, test_ball)

        test_ball.velocity = Vector3(0, -100, 0)
        self.__base = self.calculate_translation(simulation, test_ball)
        self.__base_distance = self.__distance_on_earth(self.__base, self.__target)
        self.__force_vector = self.calculate_force_vector()

        # Values to binary search the optimal speed to reach the target
        low = 0
        high = 1

        simulation = SimulationReal([
            earth,
            test_ball
        ], RenderInfo(1000000, 0.001, 'sim', 10), dt=self.__dt_sim, visualize=False)

        test_ball.mass = 1
        test_ball.inertia = 1
        while True:
            # print(high)
            test_ball.velocity = self.__force_vector * high
            test_ball.position = deepcopy(self.position)
            new_position = self.calculate_translation(simulation, test_ball)
            try:
                if self.__distance_on_earth(self.__base, new_position) >= self.__base_distance:
                    break
                else:
                    high *= 2
            except:
                break

        # print(high, new_position.x)
        optimal_velocity_x, translation = self.__bs(low, high, 15, simulation, test_ball)
        print(optimal_velocity_x, translation, translation.length, self.__distance_on_earth(translation, self.__base))
        return optimal_velocity_x

    def __bs(self, l, h, k_left, simulation, test_ball):
        mid = (l + h) / 2
        test_ball.velocity = mid * self.__force_vector
        test_ball.position = deepcopy(self.position)
        translation = self.calculate_translation(simulation, test_ball)

        print(mid, translation)
        if k_left == 0:
            return mid, translation

        dist = self.__distance_on_earth(translation, self.__base)
        if dist >= self.__base_distance:
            return self.__bs(l, mid, k_left - 1, simulation, test_ball)
        else:
            return self.__bs(mid, h, k_left - 1, simulation, test_ball)

    def __distance_on_earth(self, point1, point2):
        # Assumes that the earth is at (0, 0, 0) and the radius is 6371000m
        alpha = acos(Vector3.dot_product(point1, point2) / (point1.length * point2.length)).real
        return 2 * pi * 6371000 * degrees(alpha) / 360

    def calculate_translation(self, simulation, test_ball):
        last_distance = 0
        while not test_ball.collided:
            simulation.do_step()
            if distance(test_ball.position, deepcopy(self.position)) < last_distance:
                break
            else:
                last_distance = distance(test_ball.position, deepcopy(self.position))
        output = deepcopy(test_ball.position)
        test_ball.position = deepcopy(self.position)
        if not test_ball.collided:
            return None
        test_ball.collided = False
        return output

    def calculate_force_vector(self):
        normal = Line3D.from_points(deepcopy(self.position), Vector3())
        plane = Plane.from_normal(deepcopy(self.position), normal)
        line_to_target = Line3D.from_points(self.__target, Vector3())
        cp = cross_point(plane, line_to_target)
        if cp is None:
            force_vector = line_to_target
        else:
            force_vector = (cp - deepcopy(self.position)).unit

        cos = Vector3.dot_product(normal.direction, line_to_target.direction) / (normal.direction.length *
                                                                                 line_to_target.direction.length)
        if acos(cos).real > pi / 2:
            force_vector = -force_vector

        return force_vector

    def actualize_loop(self, dt: float) -> None:
        super().actualize_loop(dt)

    def __end_simulation(self):
        raise Exception('done')

    def __distance_to_ground(self, y):
        return y - 6371000

    def __distance_to_center(self, y):
        return y + 6371000


class TestBody(Body):

    def __init__(self, position: Vector3, velocity: Vector3, acceleration: Vector3,
                 rotation: Vector3, ang_velocity: Vector3, ang_acceleration: Vector3):
        super().__init__(0, 0, position, velocity, acceleration, rotation, ang_velocity,
                         ang_acceleration, BallCollider(1), visual=False)
        self.collided = False
        self.start_position = deepcopy(position)

    def on_collided(self, target):
        self.collided = True

    def reset(self):
        self.position = deepcopy(self.start_position)
        self.collided = False
