from src.abstract import EntityI
from src.actions import ActionBase, ActionState, HasActionQueue
from pyray import Vector3, Model, GRAY, gen_mesh_cylinder, load_model_from_mesh, matrix_rotate_xyz, draw_model

class GameEntity(EntityI, HasActionQueue):
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
        super(EntityI, self).__init__()
        super(HasActionQueue, self).__init__()
        self._model = model if model else GameEntity.default_cylinder()
        self.pos = pos if pos else Vector3(0,0,0)
        self.orient = orient if orient else Vector3(0,0,0)
        self._scale = scale
        self._color = color
        

    @property
    def scale(self) -> float:
        return self._scale
    @scale.setter
    def scale(self, new_scale):
        assert isinstance(new_scale, float)
        assert new_scale > 0
        self._scale = new_scale


    # Updates
    def update(self, shader=None):
        self.resolve_current_action()
            

    
    def draw(self):
        # self._model.transform = matrix_rotate_xyz(self._orient)
        draw_model(self._model, self.pos, self.scale, self._color)
    
    def __str__(self):
        return f"<GameEntity_{self._uid}>"