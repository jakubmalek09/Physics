from copy import deepcopy
from time import time as t
from typing import List

import core
from core.visual import Visualization
from .elementary.constants import G
from core.elementary.physical.force import Force
from core.elementary.math.geometry.geometry3d.vector3 import distance
from .objects import body
from .objects.body import Body


class SimulationReal:
    def __init__(self, objects: List[Body], render_info, dt=0.01, visualize=True):
        self.start_objects = objects
        self.objects = objects
        self.dt = dt
        self.time = 0
        self.visualize = visualize

        # Adding momentum on the start. If not added, the star system will only have the momentum of the orbiting
        # object, so it will start to move somewhere
        for obj in self.objects:
            if obj.orbit is not None:
                orbit = self.find_object(obj.orbit)
                orbit_v = -obj.mass * obj.velocity / orbit.mass
                orbit.velocity += orbit_v

        # Visualization things
        if visualize:
            self.visualization = Visualization(objects, render_info)
        self.render_info = render_info
        if render_info.time_scale == 'real':
            self.time_function = t
        else:
            self.time_function = self.get_simulation_time

        self.last_time = self.time_function()

    def do_step(self):
        # Visualization
        if self.visualize:
            if self.time_function() - self.last_time > self.render_info.update_time:
                self.last_time = self.time_function()
                self.visualization.update(self.objects)

        # Clean all effects from the objects
        for obj in self.objects:
            obj.actualize_loop(self.dt)

        # Apply gravity forces
        for obj1 in self.objects:
            for obj2 in self.objects:
                if obj1 is obj2 or obj1.mass == 0 or obj2.mass == 0:
                    continue
                force = G * obj1.mass * obj2.mass / (distance(obj1.position, obj2.position) ** 2)
                obj1.apply_force(Force(value=force, vector=(obj2.position - obj1.position).unit,
                                       application=deepcopy(obj2.position)))
        self.time += self.dt

        # Compute collisions
        for obj1 in self.objects:
            for obj2 in self.objects:
                if obj1 is obj2:
                    continue
                try:
                    if obj1.collider.check_collision(obj1, obj2):
                        obj1.collider.react(obj1, obj2)
                        obj2.collider.react(obj2, obj1)

                        obj1.on_collided(obj2)
                        obj2.on_collided(obj1)
                except AttributeError:
                    pass

    def run(self):
        self.last_time = self.time_function()
        while True:
            self.do_step()

    def stop(self):
        pass

    def add_object(self, object):
        self.objects.append(object)

    def find_object(self, name) -> core.objects.body.Body:
        for obj in self.objects:
            if obj.name == name:
                return obj

    def get_simulation_time(self):
        return self.time

    def reset_simulation(self):
        self.time = 0
        for obj in self.objects:
            obj.reset()


class SimulationFlat:
    def __init__(self, objects, render_info, dt=0.1, visualize=True):
        self.start_objects = deepcopy(objects)
        self.objects = objects
        self.dt = dt
        self.time = 0
        self.visualize = visualize

        # Visualization things
        if visualize:
            self.visualization = Visualization(objects, render_info)
        self.render_info = render_info
        if render_info.time_scale == 'real':
            self.time_function = t
        else:
            self.time_function = self.get_simulation_time

    def run(self):
        last_time = self.time_function()
        while True:
            # Visualization
            if self.visualize:
                if self.time_function() - last_time > self.render_info.update_time:
                    last_time = self.time_function()
                    self.visualization.update(self.objects)

            # Clean all effects from the objects
            for obj in self.objects:
                obj.actualize_loop(self.dt)

            # Add air force

            # Compute collisions
            for obj1 in self.objects:
                for obj2 in self.objects:
                    if obj1 is obj2:
                        continue
                    if obj1.collider.check_collision(obj1, obj2):
                        obj1.collider.react(obj1, obj2)
                        obj2.collider.react(obj2, obj1)

    def stop(self):
        pass

    def add_object(self, object):
        self.objects.append(object)

    def find_object(self, name) -> core.objects.body.Body:
        for obj in self.objects:
            if obj.name == name:
                return obj

    def get_simulation_time(self):
        return self.time

    def reset_simulation(self):
        self.time = 0
        for obj in self.start_objects:
            this_obj = self.find_object(obj.name)
            this_obj.position = obj.position
            this_obj.velocity = obj.velocity
