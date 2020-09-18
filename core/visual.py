import numpy as np
import pyglet
import ratcave as rc
from dataclasses import dataclass


class Visualization:
    def __init__(self, objects, render_info):
        self.window = pyglet.window.Window()
        meshes = []
        self.ids = {}
        for obj in objects:
            mesh = obj.mesh
            mesh.position.xyz = obj.position.to_xyz()
            # mesh.position.xyz = 0, 0, 0
            print(obj.name, mesh.position)
            mesh.scale.xyz = obj.collider.to_xyz()
            # mesh.scale.xyz = 1000, 1000, 1000
            meshes.append(mesh)
            self.ids[obj.name] = mesh

        self.scene = rc.Scene(meshes=meshes)
        self.scene.bgColor = 0, 0, 1
        # projection = rc.camera.ProjectionBase(z_far=10000, z_near=0.001)
        projection = rc.PerspectiveProjection(z_far=render_info.far, z_near=render_info.near)
        self.scene.camera = rc.Camera(projection, rotation=(0, 0, 0))
        self.scene.camera.position.xyz = 0, 0, 1000
        self.render_info = render_info

        @self.window.event
        def on_draw():
            with rc.default_shader:
                self.scene.light.position = self.scene.camera.position
                self.scene.draw()

    def update(self, objects):
        pyglet.clock.tick()

        for window in pyglet.app.windows:
            for obj in objects:
                mesh = self.ids[obj.name]
                if mesh is not None:
                    mesh.position.xyz = obj.position.to_xyz()
            window.switch_to()
            window.dispatch_events()
            window.dispatch_event('on_draw')
            window.flip()


@dataclass
class RenderInfo:
    def __init__(self, far, near, time_scale, update_time):
        """

        :param far: Maximum render distance
        :param near Minimum render distance
        :param time_scale: 'real' or 'sim':
            'real' - the visualization updates basing on computer time
            'sim' - the visualization updates basing on simulation time
        :param update_time: Cycle of visualization update
        """
        self.far = far
        self.near = near
        self.time_scale = time_scale
        self.update_time = update_time
