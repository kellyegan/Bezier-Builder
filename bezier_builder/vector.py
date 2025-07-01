import numpy as np


class Vector(np.ndarray):
    def __new__(cls, x=0, y=0):
        obj = np.array([x, y], dtype=np.float64).view(cls)
        return obj
    
    def __array_finalize__(self, obj):
        if obj is None:
            return
    
    @property
    def x(self) -> float:
        return self[0]
    
    @x.setter
    def x(self, value: float):
        self[0] = value
    
    @property
    def y(self) -> float:
        return self[1]
    
    @y.setter
    def y(self, value: float):
        self[1] = value

    def magnitude(self) -> float:
        return np.linalg.norm(self)