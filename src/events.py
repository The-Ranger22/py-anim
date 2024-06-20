from src.abstract import EntityI
from abc import ABC, abstractmethod
from enum import Enum, auto
from itertools import count
from pyray import Vector3, get_fps, vector3_add, vector3_max, vector3_min, vector3_subtract, vector3_scale
class ActionState(Enum):
    INITIAL = auto()
    ACTIVE = auto()
    PAUSED = auto()
    COMPLETE = auto()
    FAILED = auto()


class ActionBase(ABC):
    _target: EntityI 
    _count = count()
    _instances = {}
    _state: ActionState
    def __init__(self, *args, **kwargs):
        self._uid = next(ActionBase._count)
        ActionBase._instances[self._uid] = self._uid
        self._duration_sec = kwargs['duration_seconds']
        self._target = kwargs['target']
        self._state = ActionState.INITIAL

    @property
    def target(self) -> EntityI:
        return self._target

    @property
    def state(self) -> ActionState:
        return self._state
    
    @abstractmethod
    def step(self):
        pass
    

    def activate(self):
        self._state = ActionState.ACTIVE

    def complete(self):
        self._state = ActionState.COMPLETE

    def pause(self):
        self._state = ActionState.PAUSED
    
    def resume(self):
        if self._state == ActionState.PAUSED:
            self.activate()
    

class MoveAction(ActionBase):
    _p1: Vector3
    _p2: Vector3
    def __init__(self, target, move_to: Vector3, duration_seconds: float):
        super().__init__(self, target=target, duration_seconds=duration_seconds)
        self._p1 = self.target.pos
        self._p2 = move_to
        self._step_count = 0
        self._num_steps = self._duration_sec * 60.0
        # self._st = vector3_scale(vector3_subtract(self._p2, self._p1), 1/self._num_steps)
        self._st = Vector3(
            (self._p2.x - self._p1.x)/self._num_steps,
            (self._p2.y - self._p1.y)/self._num_steps,
            (self._p2.z - self._p1.z)/self._num_steps,
        )

    def activate(self):
        super().activate()
        self._p1 = self.target.pos
        # self._p1 = vector3_min(self.target.pos, self._p2)
        # self._p2 = vector3_max(self.target.pos, self._p2)
        self._st = Vector3(
            (self._p2.x - self._p1.x)/self._num_steps,
            (self._p2.y - self._p1.y)/self._num_steps,
            (self._p2.z - self._p1.z)/self._num_steps,
        )

    def step(self):
        if self._step_count == 0:
            self.activate()
        self._target.pos = vector3_add(self._target.pos, self._st)
        self._step_count += 1
        self.resolve_state()
    
    def is_complete(self) -> bool:
        return self._step_count >= self._num_steps

    def resolve_state(self):
        if self.is_complete():
            
            print(f"x: {self._p1.x:.06f} y: {self._p1.y:.06f} z: {self._p1.z:.06f}")
            print(f"x: {self._p2.x:.06f} y: {self._p2.y:.06f} z: {self._p2.z:.06f}")
            self.complete()
        

        

# class ActionQueue:
#     _queue: list[ActionBase]

#     def __init__(self, *actions: ActionBase):
