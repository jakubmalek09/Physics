import numpy as np
from .objects import body
from .elementary.vector3 import Vector3, distance
from .elementary.constants import G
from .elementary.force import Force
import pygame
from time import time as t
import core


class Simulation:
    def __init__(self, objects=None, dt=0.1):
        self.objects = objects
        self.dt = dt
        self.time = 0
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 600))
        self.screen_width = 1200
        self.screen_height = 600
        pygame.display.set_caption('Simulation')
        self.max_screen_x = 10 ** 10  # million km
        self.max_screen_y = 0.5 * 10 ** 10  # half a million km
        for obj in self.objects:
            if obj.orbit is not None:
                orbit = self.find_object(obj.orbit)
                orbit_v = -obj.mass * obj.velocity / orbit.mass
                orbit.velocity += orbit_v

    def run(self):
        last_time = t()
        while True:
            # Some debug
            print(distance(self.find_object('Moon').position, self.find_object('Earth').position), self.time)

            # Visualization
            if t() - last_time > 0.01:
                last_time = t()
                self.screen.fill((0, 0, 0))
                for obj in self.objects:
                    pygame.draw.circle(self.screen, obj.color, (int(0.5 * (self.screen_width + (obj.position.x /
                                       self.max_screen_x) * self.screen_width)), int(0.5 * (self.screen_height + (
                                       obj.position.y / self.max_screen_y) * self.screen_height))),
                                       2)  # int(obj.collider.radius / self.max_screen_x)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                pygame.display.update()

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
                    # GOD YOU CAN'T APPLY FORCE TO ANOTHER OBJECT HERE!!!; IT WILL BE APPLIED IN ONE OF THE NEXT LOOPS
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

    def find_object(self, name) -> core.objects.body.Body:
        for obj in self.objects:
            if obj.name == name:
                return obj

