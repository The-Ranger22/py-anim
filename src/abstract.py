from abc import abstractmethod, ABC
from itertools import count
from pyray import Vector3

class EntityI(ABC):
    _uid: int
    _pos: Vector3
    _orient: Vector3
    _count = count()
    _instances = {}
    def __init__(self, *args, **kwargs):
        self._uid = next(EntityI._count)
        EntityI._instances[self._uid] = self

    @property
    def pos(self) -> Vector3:
        return self._pos
    @pos.setter
    def pos(self, new_pos: Vector3):
        # assert isinstance(new_pos, Vector3)
        self._pos = new_pos 

    @property
    def orient(self) -> Vector3:
        return self._orient
    @orient.setter
    def orient(self, new_orient: Vector3):
        # assert isinstance(new_orient, Vector3)
        self._orient = new_orient

    @abstractmethod
    def update(self):
        pass

class EventI(ABC):
    _uid: int
    _count = count()
    _instances = {}
    def __init__(self, *args, **kwargs):
        self._uid = next(EventI._count)
        EventI._instances[self._uid] = self
    
    @property
    def uid(self):
        return self._uid    


    
    