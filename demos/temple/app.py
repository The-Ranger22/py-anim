import os, sys
sys.path.append(os.getcwd())
print(os.getcwd())
from src import App, Scene
from src.entity import GameEntity
from src.camera import GameCamera
from src.actions import MoveAction, WaitAction, CompoundAction, LookAtAction, SplineMoveAction, LookRelativeAction, SequencedAction
from pyray import Vector3, BLUE, WHITE, RED, GREEN, BLACK, CameraMode, YELLOW, gen_mesh_cube, gen_mesh_sphere, load_model_from_mesh, CameraProjection, Model, load_model



def main():
    app = App(1280, 720, 'temple', target_fps=60)
    app.init_context()
    entites = []
    temple = GameEntity(
        load_model("demos/temple/assets/Greek Temple.glb"),
        # load_model("demos/temple/assets/Wall Towers Door Seco.glb"),
        Vector3(0.0,0.0,0.0),
        Vector3(0.0,0.0,0.0),
        scale=25.0,
        color=WHITE
    )
    floor = GameEntity(
        g
    )
    camera = GameCamera([36.0, 10.0, 36.0], [0.0,0.0,0.0], [0.0,1.0,0.0], 45.0, CameraMode.CAMERA_CUSTOM)
    scene  = Scene(camera, [temple], background_color=BLACK)
    app.add_scene(scene, True)
    app.run()

if __name__ == "__main__":
    main()
