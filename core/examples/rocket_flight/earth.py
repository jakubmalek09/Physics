from core.elementary.math.geometry.geometry3d.vector3 import Vector3
from core.objects.body import Body
from core.objects.collision.ball_collider import BallCollider

earth = Body(mass=5.972 * 10 ** 24,
             inertia_momentum=9.736 * 10 ** 37,
             position=Vector3(0, 0, 0),
             velocity=Vector3(0, 0, 0),
             acceleration=Vector3(0, 0, 0),
             rotation=Vector3(0, 0, 0),
             ang_velocity=Vector3(0, 0, 0),
             ang_acceleration=Vector3(0, 0, 0),
             collider=BallCollider(6371000),
             name='Earth')

earth_massless = Body(mass=1,
                      inertia_momentum=1,
                      position=Vector3(0, 0, 0),
                      velocity=Vector3(0, 0, 0),
                      acceleration=Vector3(0, 0, 0),
                      rotation=Vector3(0, 0, 0),
                      ang_velocity=Vector3(0, 0, 0),
                      ang_acceleration=Vector3(0, 0, 0),
                      collider=BallCollider(6371000),
                      name='Earth')
