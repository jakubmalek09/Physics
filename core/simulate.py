import numpy as np
from .objects import body
from .elementary.vector3 import Vector3, distance
from .elementary.constants import G
from .elementary.force import Force
from time import time as t
import core
from core.visual import Visualization, RenderInfo
from copy import deepcopy


class SimulationReal:
    def __init__(self, objects, render_info, dt=0.1, visualize=True):
        self.start_objects = deepcopy(objects)
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

    def run(self):
        last_time = self.time_function()
        while True:
            # Some debug
            print(distance(self.find_object('Moon').position, self.find_object('Earth').position), self.time)
            if self.time > 100000:
                self.reset_simulation()

            # Visualization
            if self.visualize:
                if self.time_function() - last_time > self.render_info.update_time:
                    last_time = self.time_function()
                    self.visualization.update(self.objects)

            # Clean all effects from the objects
            for obj in self.objects:
                obj.actualize_loop(self.dt)

            # Apply gravity forces
            for obj1 in self.objects:
                for obj2 in self.objects:
                    if obj1 is obj2:
                        continue
                    force = G * obj1.mass * obj2.mass / (distance(obj1.position, obj2.position) ** 2)
                    obj1.apply_force(Force(force, application=obj1.position, target=obj2.position))
            self.time += self.dt

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

