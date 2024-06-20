from src.entity import EntityI
from pyray import Camera3D, CameraMode, CameraProjection, update_camera_pro, update_camera, Vector3

class GameCamera(EntityI):

    def __init__(
            self, 
            pos: Vector3, 
            target: Vector3,
            up: Vector3,
            fovy: float = 45.0,
            projection: CameraProjection = CameraProjection.CAMERA_PERSPECTIVE,
            mode: CameraMode = CameraMode.CAMERA_CUSTOM
        ):
        super().__init__(self)
        self._cam = Camera3D(pos, target, up, fovy, projection)
        self._pos = pos
        self._target = target
        self._up = up
        self._fovy = fovy
        self._proj = projection
        self._mode = mode
    
    def _update_std(self):
        update_camera(self._cam, self._mode)
    


    def update(self):
        # update_camera_pro(self._cam, self._cam.position, self._orient, 1.0) 
        # update_camera_pro(self._cam, self._cam.position, self._cam.)
        update_camera(self._cam, self._mode)