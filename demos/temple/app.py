import os, sys
sys.path.append(os.getcwd())
print(os.getcwd())
from src import App, Scene
from src.entity import GameEntity
from src.camera import GameCamera
from src.actions import MoveAction, WaitAction, CompoundAction, LookAtAction, SplineMoveAction, LookRelativeAction, SequencedAction
from src.emitters import *
from pyray import unload_model, Vector3, vector3_zero, BLUE, WHITE, RED, GREEN, BLACK, WHITE, CameraMode, YELLOW, gen_mesh_cube, gen_mesh_sphere, load_model_from_mesh, CameraProjection, Model, load_model, Shader, load_shader, unload_shader, ShaderLocationIndex, get_shader_location, set_shader_value, ShaderUniformDataType, set_config_flags, ConfigFlags, BEIGE, Color, load_texture, MaterialMapIndex, gen_mesh_torus, unload_texture, load_materials, load_material_default, Material, set_model_mesh_material
from raylib import ffi

def main():
    app = App(1280, 720, 'temple', target_fps=60)
    set_config_flags(ConfigFlags.FLAG_MSAA_4X_HINT)
    app.init_context()
    entities = []
    
    shader_file_path = 'demos/temple/assets/shaders/lighting.{ext}'
    shader = load_shader(shader_file_path.format(ext='vs'), shader_file_path.format(ext='fs'))
    shader.locs[ShaderLocationIndex.SHADER_LOC_VECTOR_VIEW] = get_shader_location(shader, 'viewPos')
    shader.locs[ShaderLocationIndex.SHADER_LOC_MATRIX_MODEL] = get_shader_location(shader, "matModel")
    ambient_loc = get_shader_location(shader, 'ambient')

    # ambient = ffi.new("float ambient[4]", [0.1, 0.1, 0.1, 0.1])
    ambient = ffi.new("float ambient[4]", [0.1, 0.1, 0.1, 1.0])
    set_shader_value(shader, ambient_loc, ambient, ShaderUniformDataType.SHADER_UNIFORM_VEC4)

    tex = load_texture('demos/temple/assets/tex/marble-texture-background.jpg')

    temple_model = load_model("demos/temple/assets/Greek Temple.glb")
    
    floor_model = load_model_from_mesh(gen_mesh_cube(100.0, 1.0, 100.0))
    temple_model.materials[0].shader = shader
    temple_model.materials[1].shader = shader
    temple_model.materials[2].shader = shader
    temple_model.materials[0].maps[MaterialMapIndex.MATERIAL_MAP_ALBEDO].texture = tex
    floor_model.materials[0].shader = shader
    temple = GameEntity(
        temple_model,
        Vector3(0.0,0.0,0.0),
        Vector3(0.0,0.0,0.0),
        scale=20.0,
        color=WHITE
    )
    floor = GameEntity(
        floor_model,
        Vector3(0.0, -2.5, 0.0),
        color=BEIGE
    )
    lights = []
    # lights.append(Light.create(LightType.POINT, Vector3( 10.0, 10.0,  10.0), vector3_zero(), Color(*RED), shader))
    lights.append(Light.create(LightType.POINT, Vector3(-0.55, 1.5,  0.0), vector3_zero(), Color(*YELLOW), shader))
    # lights.append(Light.create(LightType.POINT, Vector3( 10.0, 10.0, -10.0), vector3_zero(), Color(*GREEN), shader))
    # lights.append(Light.create(LightType.POINT, Vector3(-10.0, 10.0, -10.0), vector3_zero(), Color(*BLUE), shader))

    entities.append(temple)
    entities.append(floor)
    
    camera = GameCamera(Vector3(36.0, 5.0, 36.0), [0.0,0.0,0.0], [0.0,1.0,0.0], 45.0, CameraMode.CAMERA_CUSTOM)
    camera.queue_action(MoveAction(camera, Vector3( 15.0, 5.0,  15.0), 05.0))
    camera.queue_action(MoveAction(camera, Vector3(-15.0, 5.0,  15.0), 05.0))
    camera.queue_action(MoveAction(camera, Vector3(-15.0, 5.0, -15.0), 05.0))
    camera.queue_action(MoveAction(camera, Vector3( 15.0, 5.0, -15.0), 05.0))
    scene  = Scene(camera, shader, entities, lights, BLACK)
    app.add_scene(scene, True)
    app.run()
    
    unload_shader(shader)
    unload_texture(tex)
    unload_model(temple_model)
    unload_model(floor_model)

if __name__ == "__main__":
    main()
