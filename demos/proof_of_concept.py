import ctypes
import pyray as pr
import numpy as np
import cv2
import itertools


WIN_DETAILS = (1200, 800, 'MaiyaWitness')


C_VOID_POINTER = ctypes.POINTER(ctypes.c_void_p)
# C_VOID_POINTER = ctypes.c_void_p


def mpeg_to_texture(texture: pr.Texture):
    pass

class FrameCycler(object):
    def __init__(self, frames, fmt):
        self._cycler = itertools.cycle([
            pr.Image(f, f.shape[1], f.shape[0], 1, fmt)
            for f in frames
        ])
        self.tex = pr.load_texture_from_image(next(self._cycler))
    
    def __iter__(self):
        return self
    
    def __next__(self):
        return self.next()

    def next(self):
        pr.update_texture(self.tex, next(self._cycler).data)
        # return next(self._cycler)
class FrameGenerator(object):
    def __init__(self, video: str):
        self._video = video
        self._cap = cv2.VideoCapture(video)

    def __iter__(self):
        return self
    
    def __next__(self):
        return self.next()
    def next(self):
        ret, frame = self._cap.read()
        if not ret:
            self._cap.release()
            self._cap = cv2.VideoCapture(self._video)
            _, frame = self._cap.read()
        return frame

class AnimLoopFrames(object):
    def __init__(self, video_path: str, vid_fps: int, global_fps: int):
        self._img = None
        self._tex = None
        self._fg = FrameGenerator(video_path)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        return self.next()
    
    def _load_imtex(self):
        pass

    def _unload_imtex(self):
        pass

    def next(self):
        pass

def __main__():


    raw_img = cv2.imread('resources/textures/maiyaMorph1.png')
    cap = cv2.VideoCapture('resources/video/twister480p.mp4')
    print(cap.get(cv2.CAP_PROP_FPS))
    frames = []
    mx_val = -1
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        red = frame[:,:,0].copy()
        blue = frame[:,:,2].copy()
        frame[:,:,0] = blue
        frame[:,:,2] = red
        # print(frame[0][0])
        frames.append(frame)
        # print('AAAAAA', type(frame))

    print(frames[0].shape)

    fg = FrameGenerator('resources/video/twister480p.mp4')

    # print(frames[0])
    pr.init_window(*WIN_DETAILS)
    fc = FrameCycler(frames, pr.PixelFormat.PIXELFORMAT_UNCOMPRESSED_R8G8B8)
    # img = pr.Image(raw_img, raw_img.shape[1], raw_img.shape[0], 1, pr.PixelFormat.PIXELFORMAT_COMPRESSED_PVRT_RGBA)
    # texture = pr.Texture()
    camera = pr.Camera3D([18.0, 16.0, 18.0], [0.0, 0.0, 0.0], [0.0, 1.0, 0.0], 45.0, 0)
    mesh = pr.gen_mesh_cube(1, 1, 1)
    model = pr.load_model_from_mesh(mesh)
    sphere_mesh = pr.gen_mesh_sphere(1.0, 12, 12)
    sphere_model = pr.load_model_from_mesh(sphere_mesh)

    # pr.model
    ang = pr.Vector3(0,0,0)
    period = 0
    current_period = 1
    frame = next(fg)
    img5 = pr.Image(frame, frame.shape[1], frame.shape[0], 1, pr.PixelFormat.PIXELFORMAT_UNCOMPRESSED_R8G8B8)
    texture5 = pr.load_texture_from_image(img5)
    pr.set_target_fps(60)
    # sphere_model.materials[0].maps[pr.MaterialMapIndex.MATERIAL_MAP_ALBEDO].texture = texture
    sphere_model.materials[0].maps[pr.MaterialMapIndex.MATERIAL_MAP_ALBEDO].texture = fc.tex
    model.materials[0].maps[pr.MaterialMapIndex.MATERIAL_MAP_ALBEDO].texture = fc.tex
    
    # model.materials[0].maps[pr.MaterialMapIndex.MATERIAL_MAP_ALBEDO].texture = texture3 
    try:
        while not pr.window_should_close():
            ang.x += 0.01
            ang.y += 0.02
            ang.z += 0.005

            model.transform = pr.matrix_rotate_xyz(ang)
            sphere_model.transform = pr.matrix_rotate_xyz(ang)
            if period > 1:
                # frame = next(fg)
                # img5 = pr.Image(frame, frame.shape[1], frame.shape[0], 1, pr.PixelFormat.PIXELFORMAT_UNCOMPRESSED_R8G8B8)
                # texture5 = pr.load_texture_from_image(img5)
                # frame_data = next(fg).astype(np.void)
                # frame_img = pr.Image(frame_data, frame_data.shape[1], frame_data.shape[0], 1, pr.PixelFormat.PIXELFORMAT_UNCOMPRESSED_R8G8B8)
                # pr.rl_update_texture(
                #     texture5.id, 
                #     0, 
                #     0, 
                #     frame_data.shape[1], 
                #     frame_data.shape[0], 
                #     pr.PixelFormat.PIXELFORMAT_UNCOMPRESSED_R8G8B8, 
                #     frame_data
                # )
                # pr.update_texture(texture5, frame_data.ctypes.data_as(C_VOID_POINTER))
                # pr.update_texture(texture5, frame_img.data)
                fc.next()
                # pr.unload_image(frame_img)
                period = 0 
            pr.update_camera(camera, pr.CAMERA_ORBITAL)
            pr.begin_drawing()
            pr.clear_background(pr.RAYWHITE)
            pr.draw_texture_pro(
                fc.tex, 
                pr.Rectangle(0,0,fc.tex.width,fc.tex.height), 
                pr.Rectangle(0,0,pr.get_screen_width(), pr.get_screen_height()),
                pr.Vector2(0,0), 0, pr.WHITE
            )
            
            pr.begin_mode_3d(camera)
            pr.draw_model(model, pr.Vector3(0,0,0), 1, pr.WHITE)
            pr.draw_model(sphere_model, pr.Vector3(2, 0, 0), 1, pr.WHITE)
            pr.end_mode_3d()
            pr.draw_fps(30, 30)
            pr.end_drawing()
            period += 1
    except Exception as e:
        print(e)
    finally:

        pr.close_window()


if __name__ == "__main__":
    __main__()