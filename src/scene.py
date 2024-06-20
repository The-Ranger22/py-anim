from src.entity import GameEntity
from src.camera import GameCamera
from itertools import count
import pyray as pr

class Scene:
    # Index entities from furthest to closest relative to camera
    _entities: list[GameEntity] 
    _cameras: list[GameCamera]
    _active_cam: GameCamera
    _count = count()
    _instances = {}
    def __init__(self, camera: GameCamera, *entity_or_entities):
        self._uid = next(Scene._count)
        Scene._instances[self._uid] = self

        self._entities = list(*entity_or_entities)
        self._cameras = [camera]
        self._active_cam = camera

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
        pr.clear_background(pr.RAYWHITE)
        # Draw Background

        # Draw Entities
        pr.begin_mode_3d(self._active_cam._cam)
        pr.draw_grid(20, 5.0)
        for ent in self._entities:
            # print(f"Drawing `{ent}`")
            ent.update()
            ent.draw()
        pr.end_mode_3d()
        # Draw Config


        pr.end_drawing()