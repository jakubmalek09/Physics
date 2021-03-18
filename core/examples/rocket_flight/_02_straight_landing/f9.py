from cmath import log
from math import ceil

from core.elementary.constants import G
from core.elementary.math.geometry.geometry3d.vector3 import Vector3
from core.examples.rocket_flight.earth import earth
from core.examples.rocket_flight.f9 import Falcon9 as f9


class Falcon9(f9):
    """
    Vertical landing
    """
    __g = 9.81
    __dt = 0.01
    __save_distance = 0

    def __init__(self, position: Vector3, rotation: Vector3):
        super().__init__(position, rotation)
        self.__land_burn_height = self.find_optimal_distance()

    def actualize_loop(self, dt: float) -> None:
        if self.__do_start_burn(dt):
            print('actual values:', self.__distance_to_ground(self.position.y), self.velocity.y)
            print(self.__simulate_stop_now(self.position.y, self.velocity.y))
            self.__end_simulation()

        super().actualize_loop(dt)

    def find_optimal_distance(self):
        """
        Binary search
        n + klog(n)
        n - steps to calculate falling
        k - steps to calculate landing
        :return:
        """
        accuracy = 1
        k = ceil(log(self.__distance_to_ground(self.position.y) / accuracy, 2).real)
        l = 0
        h = self.__distance_to_ground(self.position.y)

        return self.__bs(l, h, 0, k)

    def __bs(self, l, h, v_h, k_left):
        """

        :param l: Low distance in m above the ground
        :param h: High distance in m above the ground
        :param v_h: Velocity at high distance
        :return:
        """
        mid = (l + h) / 2
        h_mid, v_mid = self.__simulate_velocity(mid, h, v_h)

        stopped, time, distance = self.__simulate_stop_now(h_mid, v_mid)
        sh, th, dh = self.__simulate_stop_now(self.__distance_to_center(h), v_h)

        if k_left == 0 and not stopped:
            print('calculated height and velocity:', h, v_h)
            print(sh, th, dh)
        elif k_left == 0:
            print('calculated height and velocity:', mid, v_mid)
            print(stopped, time, distance)

        if stopped:
            # print(mid, v_mid, distance)
            if k_left == 0:
                return mid
            else:
                return self.__bs(l, self.__distance_to_ground(h_mid), v_mid, k_left - 1)
        else:
            if k_left == 0:
                return h
            else:
                return self.__bs(mid, h, v_h, k_left - 1)

    def __simulate_velocity(self, low, high, velocity):
        distance = self.__distance_to_center(high)

        while True:
            a = -G * earth.mass / (distance ** 2)
            distance += velocity * self.__dt
            velocity += a * self.__dt

            if self.__distance_to_ground(distance) <= low:
                return distance, velocity

    def __simulate_stop_now(self, distance: float, velocity: float) -> (bool, float, float):
        """

        :param distance: Y position
        :param velocity: Y velocity
        :return: Did stop before crushing down, time of stopping, distance above the earth; (False, 0, 0) if crushed
        """
        full_time = 0

        engine = self.engine  # using deepcopy

        while True:
            force = engine.force
            engine.reduce_fuel_dt(self.__dt)
            a = force / self.mass
            a -= G * earth.mass / (distance ** 2)
            distance += velocity * self.__dt
            velocity += a * self.__dt

            full_time += self.__dt

            if engine.fuel_mass <= 0:
                return False, full_time, self.__distance_to_ground(distance)
            elif velocity >= 0:
                if self.__distance_to_ground(distance) < self.__save_distance:
                    return False, full_time, self.__distance_to_ground(distance)
                else:
                    return True, full_time, self.__distance_to_ground(distance)

    def __do_start_burn(self, dt: float):
        if self.__distance_to_ground(self.position.y) < self.__land_burn_height:
                # self.__distance_to_ground(self.position.y) + dt * self.velocity.y < self.__land_burn_height:
            return True
        return False

    def __end_simulation(self):
        raise Exception('done')

    def __distance_to_ground(self, y):
        return y - 6371000

    def __distance_to_center(self, y):
        return y + 6371000
