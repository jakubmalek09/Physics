from .collider import Collider
from core.elementary.vector3 import distance, Vector3


class BallCollider(Collider):
    def __init__(self, radius):
        self.radius = radius
        super().__init__()

    def check_collision(self, obj, other) -> bool:
        if isinstance(other.collider, BallCollider):
            return self.radius + other.collider.radius > distance(obj.position, other.position)
        else:
            raise NotImplementedError('Collision with collider of type: {} not implemented yet'.format(type(other.collider)))

    def react(self, obj, other) -> None:
        # todo add momentum
        obj.velocity = Vector3(0, 0, 0)
        other.velocity = Vector3(0, 0, 0)
        obj.acceleration = Vector3(0, 0, 0)
        other.acceleration = Vector3(0, 0, 0)

        dist_m = (self.radius + other.collider.radius) - distance(obj.position, other.position)  # Distance that the
        # balls  must be moved by
        dist = distance(obj.position, other.position)
        dist_x = obj.position.x - other.position.x
        dist_y = obj.position.y - other.position.y
        dist_z = obj.position.z - other.position.z

        xp = dist_x / dist
        yp = dist_y / dist
        zp = dist_z / dist

        dx = xp * dist_m
        dy = yp * dist_m
        dz = zp * dist_m

        this_p = obj.mass / (obj.mass + other.mass)
        other_p = other.mass / (obj.mass + other.mass)

        obj.position.x += other_p * dx
        obj.position.y += other_p * dy
        obj.position.z += other_p * dz

        other.position.x -= this_p * dx
        other.position.y -= this_p * dy
        other.position.z -= this_p * dz

    def to_xyz(self):
        return self.radius / 1000000, self.radius / 1000000, self.radius / 1000000
