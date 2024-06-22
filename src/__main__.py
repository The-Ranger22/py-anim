from src import App, Scene
from src.entity import GameEntity
from src.camera import GameCamera
from src.events import MoveAction
from pyray import Vector3, BLUE, RED, GREEN, BLACK, CameraMode, YELLOW, gen_mesh_sphere, load_model_from_mesh
def test_scene():
    print("Enter Test Scene")
    app = App(800, 800, 'test')
    app.init_context()
    print("Prepare entities")
    coord = 10.0
    entities = [
        # GameEntity(pos=Vector3( 0.0, 0,  0.0), color=BLUE),
        GameEntity(pos=Vector3( coord, 0,  coord), scale=5.0, color=BLUE),
        GameEntity(pos=Vector3(-coord, 0,  coord), scale=5.0, color=RED),
        GameEntity(pos=Vector3( coord, 0, -coord), scale=5.0, color=GREEN),
        GameEntity(pos=Vector3(-coord, 0, -coord), scale=5.0, color=BLACK),
    ]
    print("Prepare Camera")
    camera = GameCamera([18.0, 16.0, 18.0], [0.0, 0.0, 0.0], [0.0, 1.0, 0.0], mode=CameraMode.CAMERA_ORBITAL)
    scene = Scene(camera, entities)
    app.add_scene(scene, True)
    print("App Start")
    app.run()
    
def test_actions():
    print("Enter Test Scene")
    app = App(800, 800, 'action')
    app.init_context()
    print("Prepare entities")
    coord = 10.0
    entities = [
        # GameEntity(pos=Vector3( 0.0, 0,  0.0), color=BLUE),
        GameEntity(pos=Vector3( coord, 0,  coord), scale=5.0, color=BLUE),
        GameEntity(pos=Vector3(-coord, 0,  coord), scale=5.0, color=RED),
        GameEntity(pos=Vector3( coord, 0, -coord), scale=5.0, color=GREEN),
        GameEntity(pos=Vector3(-coord, 0, -coord), scale=5.0, color=BLACK),
        GameEntity(load_model_from_mesh(gen_mesh_sphere(1.0, 8, 8)), pos=Vector3(0,0,0), color=YELLOW)
    ]
    entities[4].add_action(MoveAction(entities[4], Vector3(-coord, 0, 0), 1.5))
    entities[4].add_action(MoveAction(entities[4], Vector3(0, 0, coord), 3.0))
    entities[4].add_action(MoveAction(entities[4], Vector3(coord, 0, 0), 3.0))
    entities[4].add_action(MoveAction(entities[4], Vector3(0, 0, -coord), 3.0))
    entities[4].add_action(MoveAction(entities[4], Vector3(-coord, 0, 0), 3.0))
    entities[4].add_action(MoveAction(entities[4], Vector3(0, 5.0, 0), 3.0))

    print("Prepare Camera")
    camera = GameCamera([18.0, 16.0, 18.0], [0.0, 0.0, 0.0], [0.0, 1.0, 0.0], mode=CameraMode.CAMERA_ORBITAL)
    scene = Scene(camera, entities)
    app.add_scene(scene, True)
    print("App Start")
    app.run()



if __name__ == "__main__":
    test_actions()
