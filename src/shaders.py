from dataclasses import dataclass
from src.exceptions import NotLoadedError
from typing import Any
from pyray import Shader, load_shader, unload_shader, set_shader_value, get_shader_location, ShaderUniformDataType
from raylib import ffi

@dataclass
class ShaderVar:
    cdecl: str
    cinit: Any
    uniform_type: ShaderUniformDataType


class GameShader:
    _fs: str
    _vs: str
    _shader: Shader

    def __init__(self, vertex_shader_fn, fragment_shader_fn, shader_vars: dict[str, ShaderVar]):
        self._shader = None
        self._vs = vertex_shader_fn
        self._fs = fragment_shader_fn
        self._vars = shader_vars
        self._locs = None
    
    @property
    def ready(self):
        return bool(self._shader)
    
    @property
    def shader(self):
        return self._shader
    
    def load(self):
        if self.ready:
            return
        self._shader = load_shader(self._vs, self._fs)
        self._locs = {k: self.get_loc(k) for k in self._vars.keys()}
    
    def unload(self):
        if not self.ready:
            return
        unload_shader(self._shader)
        self._shader = None
    
    def get_loc(self, name: str):
        if not self.ready:
            raise NotLoadedError("Shader has not been loaded!")
        return get_shader_location(self._shader, name)
    
    def set_val(self, loc: int, val: Any, uniform_type: int):
        if not self.ready:
            raise NotLoadedError("Shader has not been loaded!")
        set_shader_value(self._shader, loc, val, uniform_type)
    
    def update(self):
        for uname, var in self._vars.items():
            loc = self._locs[uname]
            val = ffi.new(var.cdecl, var.cinit)
            self.set_val(loc, val, var.uniform_type)
