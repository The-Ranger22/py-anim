from src.abstract import EntityI
from abc import ABC, abstractmethod
from enum import Enum, auto
from itertools import count
from pyray import Vector3, vector3_add 
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
    
    def is_complete(self) -> bool:
        return self._step_count >= self._num_steps

    def resolve_state(self):
        if self.is_complete():
            self.complete()


class HasActionQueue(object):
    def __init__(self):
        self._actions: list[ActionBase] = []
        self._active_action: ActionBase = None
    
    def queue_action(self, new_action: ActionBase):
        self._actions.append(new_action)

    def deque_action(self, idx=0):
        return self._actions.pop(idx)

    def start_aq(self):
        self._active_action = self._actions.pop(0)

    def resolve_current_action(self):
        if not self._active_action and len(self._actions) <= 0:
            return
        elif not self._active_action:
            self.start_aq()
        match self._active_action._state:
            case ActionState.INITIAL:
                self._active_action.activate()
            case ActionState.ACTIVE:
                self._active_action.step()
            case ActionState.PAUSED:
                ... # Do nothing
            case ActionState.COMPLETE:
                self._active_action = None

        

class WaitAction(ActionBase):
    def __init__(self, target, duration_seconds: float):
        super().__init__(self, target=target, duration_seconds=duration_seconds)
        self._step_count = 0
        self._num_steps = self._duration_sec * 60.0
    
    def step(self):
        self._step_count += 1
        self.resolve_state()
         
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
    
        

        

# class ActionQueue:
#     _queue: list[ActionBase]

#     def __init__(self, *actions: ActionBase):
