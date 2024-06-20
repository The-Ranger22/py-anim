# MaiyaWitness

> Why god?


## Concept

- Recreation of the eyewitness intro using clips from the DinoDonothon



## 
- App -> Singleton
    - App has scenes
    - App inits and cleans up window
    - App can switch between scenes
    - has target fps
    - has a title
- Scene
    - Scene has Entities
    - Scene polls entities
    - Scene renders models in frame
    - Scene has 1 or more cameras
    - Scene has an active camera
    - has a list of Events
- Event
    - has a eventID
    - has a Trigger
    - has a target Entity 
    - has a EventState
        - EventState -> Reflects the events current status
            - INITIAL
            - ACTIVE
            - COMPLETE
            - FAILED
    - is updated every game tick

    
- EntityI
    - has an gameID
    - has a position (Vec3)
    - has an orientation (Vec3)
    - is updated every game tick
- GameCamera
    - extends EntityI
    - can look at a point (Vec3)
- GameModel
    - Extends EntityI
    - has a mesh
    - has a texture
        - Texture can be static
        - Texture can be animated
    - has a shader (TODO eventually)
- ATexture -> Describes 
    - has a texID
    - has px_width (int)
    - has px_height (int)
- StaticTexture
    - extends ATexture
- VideoTexture
    - extends ATexture
    - has a list of frames
    - has a frame rate
    - can interpolate frames to match target, global FPS
    - loads frames from video file into memory
    - can cycle through frames
    - can be updated


--- 

Entities are updated by Events
