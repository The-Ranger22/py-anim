import sys, os
sys.path.append(os.getcwd())
from src import App
from src.camera import GameCamera
from src.entity import GameEntity
from src.events import MoveAction
from src.scene import Scene
import pyray as pr

def main():
    app = App(800, 600, 'MaiyaOrbit')
    app.init_context()

    jeep_model = pr.load_model('resources/models/jeep/jeep.obj')
    pr.mesh
    # jeep_materials = pr.load_materials('resources/models/jeep/jeep2.mtl', 1)
    # jeep_model.materials = jeep_materials
    entites = [
        GameEntity(
            model=jeep_model,

            pos=pr.Vector3(0, 1, 0),
            scale=1.0,
            color=pr.WHITE
        )
    ]
    camera = GameCamera([18.0, 16.0, 18.0], [0.0, 0.0, 0.0], [0.0, 1.0, 0.0], mode=pr.CameraMode.CAMERA_ORBITAL)
    scene = Scene(camera, entites)
    app.add_scene(scene, True)
    app.run()


if __name__ == "__main__":
    main()

