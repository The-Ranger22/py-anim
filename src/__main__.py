from src import App, Scene
from src.entity import GameEntity
from src.camera import GameCamera
from src.actions import MoveAction, WaitAction, CompoundAction, LookAtAction, SplineMoveAction, LookRelativeAction
from pyray import Vector3, BLUE, RED, GREEN, BLACK, CameraMode, YELLOW, gen_mesh_sphere, load_model_from_mesh, CameraProjection
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
    entities[4].queue_action(MoveAction(entities[4], Vector3(-coord, 0, 0), 1.5))
    entities[4].queue_action(MoveAction(entities[4], Vector3(0, 0, coord), 3.0))
    entities[4].queue_action(MoveAction(entities[4], Vector3(coord, 0, 0), 3.0))
    entities[4].queue_action(MoveAction(entities[4], Vector3(0, 0, -coord), 3.0))
    entities[4].queue_action(MoveAction(entities[4], Vector3(-coord, 0, 0), 3.0))
    entities[4].queue_action(WaitAction(entities[4], 3.0))
    entities[4].queue_action(MoveAction(entities[4], Vector3(0, 5.0, 0), 3.0))

    print("Prepare Camera")
    camera = GameCamera([18.0, 16.0, 18.0], [0.0, 0.0, 0.0], [0.0, 1.0, 0.0], mode=CameraMode.CAMERA_ORBITAL)
    scene = Scene(camera, entities)
    app.add_scene(scene, True)
    print("App Start")
    app.run()

def test_camera_movement():
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
    entities[4].queue_action(MoveAction(entities[4], Vector3(-coord, 0, 0), 1.5))
    entities[4].queue_action(MoveAction(entities[4], Vector3(0, 0, coord), 3.0))
    entities[4].queue_action(MoveAction(entities[4], Vector3(coord, 0, 0), 3.0))
    entities[4].queue_action(MoveAction(entities[4], Vector3(0, 0, -coord), 3.0))
    entities[4].queue_action(MoveAction(entities[4], Vector3(-coord, 0, 0), 3.0))
    entities[4].queue_action(MoveAction(entities[4], Vector3(0, 5.0, 0), 3.0))

    print("Prepare Camera")
    # camera = GameCamera([18.0, 16.0, 18.0], [0.0, 0.0, 0.0], [0.0, 1.0, 0.0], mode=CameraMode.CAMERA_CUSTOM)
    camera = GameCamera(Vector3(18.0, 5.0, 18.0), [0.0, 0.0, 0.0], [0.0, 1.0, 0.0], projection=CameraProjection.CAMERA_PERSPECTIVE, mode=CameraMode.CAMERA_CUSTOM)
    # sm_action = SplineMoveAction(camera, 10.0, Vector3(-18.0, 2.5, -18.0), Vector3(18.0, 2.5, -20.0), Vector3(-18.0, 2.5, 20.0))
    dur = 12.0
    sm_action = SplineMoveAction(
        camera, 
        dur,
        Vector3(0.0, 6.5, 18.0),
        Vector3(18.0, 2.5, -10.0),
        Vector3(-25.0, 3.5, -40.0),
        Vector3(-8.0, 3.5, -60.0),
        Vector3(-45.0, 2.5, 55.0)
    )
    camera.queue_action(CompoundAction(camera, sm_action, LookRelativeAction(camera, dur, Vector3(1.0, 0.0, 1.0))))
    # camera.queue_action(sm_action)
    # camera.queue_action(SplineMoveAction(camera, 10.0, Vector3(-18.0, 5.5, -18.0), Vector3(-20.0, 4.0, 0.0)))
    # camera.queue_action(
    #     CompoundAction(
    #         camera, 
    #         SplineMoveAction(camera, 10.0, Vector3(10.0, 5.5, 0.0), Vector3(20.0, 4.0, 0.0)),
    #         LookAtAction(camera, entities[4], 5.0)
    #     )
    # )
    # camera.queue_action(
    #     CompoundAction(
    #         camera, 
    #         SplineMoveAction(camera, 10.0, Vector3(-18.0, 5.5, -18.0), Vector3(-20.0, 4.0, 0.0)),
    #         LookAtAction(camera, entities[4], 5.0)
    #     )
    # )
    # # camera.queue_action(MoveAction(camera, Vector3(-18.0, 16.0, -18.0),  5.0))

    # camera.queue_action(MoveAction(camera, Vector3(  7.5,  6.0,  -7.5), 10.0))
    scene = Scene(camera, entities)
    app.add_scene(scene, True)
    print("App Start")
    app.run()

if __name__ == "__main__":
    # test_actions()
    test_camera_movement()
