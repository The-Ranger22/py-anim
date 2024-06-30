from enum import Enum, auto
from itertools import count
from pyray import Shader, Color, Vector3, get_shader_location, set_shader_value, ShaderUniformDataType, draw_sphere_ex
from raylib import ffi
class LightType(Enum):
    DIRECTIONAL = auto()
    POINT = auto()

MAX_LIGHTS = 4
class Light:
    _instances = {}
    _uid: int
    _count = count()
    
    def __init__(self):
        self.ltype: int = 0
        self.enabled: bool = False
        self.pos: Vector3 = None
        self.target: Vector3 = None
        self.color: Color = None
        self.attenuation: float = 0
        self.enabled_loc: int = 0
        self.type_loc: int = 0
        self.position_loc: int = 0
        self.target_loc: int = 0
        self.color_loc: int = 0
        self.attenuation_loc: int = 0
        self._uid = next(Light._count)
        Light._instances[self._uid] = self


    @classmethod
    def create(cls, l_type: LightType, pos: Vector3, target: Vector3, color: Color, shader: Shader):
        light = cls()
        print(light._uid)
        lights_count = len(cls._instances)
        if lights_count <= MAX_LIGHTS:
            light.enabled = True
            match l_type:
                case LightType.DIRECTIONAL:
                    light.ltype = 0
                case LightType.POINT:
                    light.ltype = 1
                case _:
                    raise ValueError("Unknown or unsupport LightType was provided!")
            light.pos = pos
            light.target = target
            light.color = color

            light.enabled_loc = get_shader_location(shader, f"lights[{lights_count}].enabled")
            light.type_loc = get_shader_location(shader, f"lights[{lights_count}].type")
            light.position_loc = get_shader_location(shader, f"lights[{lights_count}].position")
            light.target_loc = get_shader_location(shader, f"lights[{lights_count}].target")
            light.color_loc = get_shader_location(shader, f"lights[{lights_count}].color")

            light.update(shader)
        return light

    def update(self, shader: Shader):
        enabled = ffi.new("int* enabled", 1 if self.enabled else 0)
        set_shader_value(shader, self.enabled_loc, enabled, ShaderUniformDataType.SHADER_UNIFORM_INT)
        _type = ffi.new("int* type", self.ltype)
        set_shader_value(shader, self.type_loc, _type, ShaderUniformDataType.SHADER_UNIFORM_INT)

        position = ffi.new('float position[3]', [self.pos.x, self.pos.y, self.pos.z])
        set_shader_value(shader, self.position_loc, position, ShaderUniformDataType.SHADER_UNIFORM_VEC3)

        target = ffi.new('float target[3]', [self.target.x, self.target.y, self.target.z])
        set_shader_value(shader, self.target_loc, target, ShaderUniformDataType.SHADER_UNIFORM_VEC3)

        color = ffi.new('float color[4]', [self.color.r/255.0, self.color.g/255.0, self.color.b/255.0, self.color.a/255.0])
        # color = ffi.new('float color[4]', [0.8, 0.0, 0.0, 1.0])
        set_shader_value(shader, self.color_loc, color, ShaderUniformDataType.SHADER_UNIFORM_VEC4)
    
    def draw(self):
        if self.enabled:
            draw_sphere_ex(self.pos, 0.2, 8, 8, self.color)
    
    def __str__(self):
        return f"<Light{self._uid}>"
