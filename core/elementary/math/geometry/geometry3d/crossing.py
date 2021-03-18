from core.elementary.math.geometry.geometry3d.line import Line3D
from core.elementary.math.geometry.geometry3d.plane import Plane


# todo
def cross_point(obj1, obj2):
    if type(obj1) == Plane and type(obj2) == Plane:
        return None
    elif type(obj1) == Line3D and type(obj2) == Plane:
        try:
            t = (obj2.D - obj2.A * obj1.point.x - obj2.B * obj1.point.y - obj2.C * obj1.point.z) /\
                (obj2.A * obj1.a + obj2.B * obj1.b + obj2.C * obj1.c)
            return obj1.value_of_t(t)
        except:
            return None
    elif type(obj1) == Plane and type(obj2) == Line3D:
        return cross_point(obj2, obj1)
    elif type(obj1) == Line3D and type(obj2) == Line3D:
        pass
