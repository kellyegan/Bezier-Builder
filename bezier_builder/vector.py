import numpy as np


class Vector(np.ndarray):
    def __new__(cls, x=0, y=0):
        obj = np.array([x, y], dtype=np.float64).view(cls)
        return obj
    
    def __array_finalize__(self, obj):
        if obj is None:
            return
        
    @classmethod
    def as_vector(cls, obj: object) -> 'Vector':
        if hasattr(obj, 'x') and hasattr(obj, 'y'):
            return cls(obj.x, obj.y)
    
    @property
    def x(self) -> float:
        return self[0].item()
    
    @x.setter
    def x(self, value: float):
        self[0] = value
    
    @property
    def y(self) -> float:
        return self[1].item()
    
    @y.setter
    def y(self, value: float):
        self[1] = value

    def magnitude(self) -> float:
        return np.linalg.norm(self)
    
    def normalize(self) -> 'Vector':
        magnitude = self.magnitude()
        if magnitude == 0:
            return
        return self / magnitude