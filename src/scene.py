from src.entity import GameEntity
from src.camera import GameCamera
from itertools import count
import pyray as pr
from raylib import ffi
class Scene:
    # Index entities from furthest to closest relative to camera
    _entities: list[GameEntity] 
    _cameras: list[GameCamera]
    _active_cam: GameCamera
    _count = count()
    _instances = {}
    def __init__(self, camera: GameCamera, shader: pr.Shader, entity_or_entities, lights, background_color=pr.RAYWHITE, showgrid: bool = False):
        self._uid = next(Scene._count)
        Scene._instances[self._uid] = self
        self._shader = shader
        self._entities = list(entity_or_entities)
        self._lights = lights
        self._cameras = [camera]
        self._active_cam = camera
        self._bg_color = background_color
        self._showgrid = showgrid

    def __str__(self):
        return f"<Scene{self._uid}>"
    # Poll all current active events
    def poll_events(self):
        pass

    def _render3d(self):
        pr.begin_mode_3d(self._active_cam._cam)
        pr.draw_grid(20, 1.0)
        for ent in self._entities:
            # print(f"Drawing `{ent}`")
            ent.draw()
        pr.end_mode_3d()

    def render(self):
        self._active_cam.update()
        pr.begin_drawing()
        pr.clear_background(self._bg_color)
        # Draw Background
        # Draw Entities
        camera_pos = ffi.new(
            "float cameraPos[3]",
            (
                self._active_cam._cam.position.x,
                self._active_cam._cam.position.y,
                self._active_cam._cam.position.z
            )
        )
        pr.set_shader_value(
            self._shader,
            self._shader.locs[pr.ShaderLocationIndex.SHADER_LOC_VECTOR_VIEW],
            camera_pos,
            pr.ShaderUniformDataType.SHADER_UNIFORM_VEC3
        )
        # Do updates
        for ent in self._entities:
            ent.update(self._shader)
        pr.begin_mode_3d(self._active_cam._cam)
        pr.begin_shader_mode(self._shader)
        if self._showgrid: 
            pr.draw_grid(20, 5.0)


        for ent in self._entities:
            # print(f"Drawing `{ent}`")
            ent.draw()
        pr.end_shader_mode()
        
        for light in self._lights:
            light.draw()
        pr.end_mode_3d()
        # Draw Config
        pr.end_drawing()