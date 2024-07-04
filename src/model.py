from src.exceptions import NotLoadedError
from src.texture import GameTexture
from src.shaders import GameShader
from pyray import Model, load_model, unload_model, MaterialMapIndex
class GameModel:
    _fn: str
    _model: Model
    def __init__(self, model_fn: str):
        self._fn = model_fn
        self._model = None
        self._tex = None
        self._shader = None
        
    @property
    def ready(self):
        return bool(self._model)

    def load(self):
        self._model = load_model(self._fn)

    def unload(self):
        unload_model(self._model)
        self._model = None

    def apply_shader(self, material_id: int, shader: GameShader):
        if not self.ready():
            raise NotLoadedError("Model is not ready! Call `GameModel().load()`")
        self._model.materials[material_id].shader = shader.shader
    
    def apply_texture(self, material_id: int, material_map_idx: MaterialMapIndex, tex: GameTexture):
        if not self.ready():
            raise NotLoadedError("Model is not ready! Call `GameModel().load()`")
        self._model.materials[material_id].maps[material_map_idx].texture = tex.tex

