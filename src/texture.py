from src.exceptions import NotLoadedError
from pyray import Texture, load_texture, unload_texture

class GameTexture:
    _fn: str
    _tex: Texture
    def __init__(self, texture_fn: str):
        self._fn = texture_fn
        self._tex = None
    
    @property
    def ready(self):
        return bool(self._tex)
    
    @property
    def tex(self):
        return self._tex
    
    def load(self):
        if self.ready:
            return
        self._tex = load_texture(self._fn)
    
    def unload(self):
        unload_texture(self._tex)
        self._tex = None