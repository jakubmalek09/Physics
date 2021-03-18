from core.elementary.math.geometry.geometry3d.vector3 import Vector3


class Engine:
    def __init__(self, fuel_mass: float, isp: float, fps: float, fuel: str, relative_position: Vector3,
                 force_angle: Vector3, vectoring_angle: float, power_percentage: float):
        self.__fuel_mass = fuel_mass
        self.__isp = isp
        self.__fps = fps
        self.__fuel = fuel
        self.__relative_position = relative_position
        self.__force_angle = force_angle
        self.__vectoring_angle = vectoring_angle
        self.__rotation = Vector3(0, 0, 0)
        self.__power_percentage = power_percentage

    @property
    def fuel_mass(self):
        return self.__fuel_mass

    @property
    def isp(self):
        return self.__isp

    @property
    def fps(self):
        return self.__fps

    @property
    def fuel(self):
        return self.__fuel

    @property
    def relative_position(self):
        return self.__relative_position

    @property
    def force_angle(self):
        return self.__force_angle

    @property
    def vectoring_angle(self):
        return self.__vectoring_angle

    @property
    def rotation(self) -> Vector3:
        return self.__rotation

    @property
    def force(self):
        return self.isp * self.fps * self.__power_percentage

    def reduce_fuel(self, mass):
        self.__fuel_mass -= mass
        if self.__fuel_mass < 0:
            self.__fuel_mass = 0

    def reduce_fuel_dt(self, dt):
        self.reduce_fuel(dt * self.__fps)

    def set_vector_angle(self, angle: Vector3):
        new_angle = self.__rotation + angle
        if new_angle.x > self.__vectoring_angle:
            new_angle.x = self.__vectoring_angle
        if new_angle.x < -self.__vectoring_angle:
            new_angle.x = -self.__vectoring_angle

        if new_angle.y > self.__vectoring_angle:
            new_angle.y = self.__vectoring_angle
        if new_angle.y < -self.__vectoring_angle:
            new_angle.y = -self.__vectoring_angle

        if new_angle.z > self.__vectoring_angle:
            new_angle.z = self.__vectoring_angle
        if new_angle.z < -self.__vectoring_angle:
            new_angle.z = -self.__vectoring_angle

        self.__rotation = new_angle

    def rotate_vector_angle(self, angle: Vector3):
        self.set_vector_angle(self.__rotation + angle)
