from src.abstract import EntityI
from src.events import ActionBase, ActionState
from pyray import Vector3, Model, GRAY, gen_mesh_cylinder, load_model_from_mesh, matrix_rotate_xyz, draw_model

class GameEntity(EntityI):
    @staticmethod
    def default_cylinder(radius: float = 0.5, height: float = 2.0, slices: int = 8):
        return load_model_from_mesh(gen_mesh_cylinder(radius, height, slices))


    def __init__(
            self,
            model: Model = None,
            pos: Vector3 = None,
            orient: Vector3 = None,
            scale: float = 1.0,
            color = GRAY
        ):
        super().__init__(self)
        self._model = model if model else GameEntity.default_cylinder()
        self.pos = pos if pos else Vector3(0,0,0)
        self.orient = orient if orient else Vector3(0,0,0)
        self._scale = scale
        self._color = color
        self._actions: list[ActionBase] = []
        self._active_action = None
        

    @property
    def scale(self) -> float:
        return self._scale
    @scale.setter
    def scale(self, new_scale):
        assert isinstance(new_scale, float)
        assert new_scale > 0
        self._scale = new_scale

    def add_action(self, new_action: ActionBase):
        self._actions.append(new_action)

    # Updates
    def update(self):
        if not self._active_action and len(self._actions) <= 0:
            return
        if not self._active_action:
            self._active_action = self._actions.pop(0)
        self._active_action.step()
        if self._active_action._state == ActionState.COMPLETE:
            self._active_action = None
            

    
    def draw(self):
        # self._model.transform = matrix_rotate_xyz(self._orient)
        draw_model(self._model, self.pos, self.scale, self._color)
    
    def __str__(self):
        return f"<GameEntity_{self._uid}>"