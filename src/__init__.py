from src.scene import Scene
from pyray import init_window, init_audio_device, close_window, window_should_close, set_target_fps


class App:
    _scenes: list[Scene]
    _active_scene: Scene

    def __init__(self, win_width: int, win_height: int, title: str, target_fps: int = 60):
        self._scenes = list()
        self._active_scene = None
        self._w = win_width
        self._h = win_height
        self._title = title
        self._t_fps = target_fps

    def _main_loop(self):
        while not window_should_close():
            self._active_scene.poll_events()
            self._active_scene.render()

    def init_context(self):
        init_window(self._w, self._h, self._title)
        set_target_fps(self._t_fps)

    def add_scene(self, new_scene: Scene, set_active=False):
        self._scenes.append(new_scene)
        if set_active:
            print(f"Set active scene to {new_scene}")
            self._active_scene = self._scenes[-1]

    def run(self):
        set_target_fps(self._t_fps)
        try:
            self._main_loop()
        except Exception as e:
            print(e)
            raise e
        finally:
            close_window()