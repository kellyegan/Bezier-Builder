import numpy as np
from bezier_builder.utils import unit_vector
from bezier_builder.vector import Vector

class AnchorPoint:
   
    def __init__(self, x=0.0, y=0.0):
      self._handle_type = "corner"
      self._pos = Vector(x, y) 
      self._handle_in = Vector() 
      self._handle_out = Vector()

    @property
    def handle_type(self) -> str:
        return self._handle_type
   
    @handle_type.setter
    def handle_type(self, handle_type: str):
        if handle_type not in ["corner", "aligned", "symmetric"]:
            raise ValueError(f"Invalid handle type: '{handle_type}'. Must be one of 'corner', 'aligned' or 'symmetric'.")
        
        self._handle_type = handle_type

        if self._handle_type == "corner":
            return

        # For aligned and symmetric align self._handle_out direction to self._handle_in
        direction = -1 * unit_vector(self._handle_in)

        # If handles are symmetric set the length of self_handle_out to the magnitude of self._handle_in
        magnitude = np.linalg.norm(self._handle_in) if self.handle_type == "symmetric" else np.linalg.norm(self._handle_out)
        self._handle_out = direction * magnitude

    @property
    def pos(self) -> Vector:
        return self._pos
    
    @pos.setter
    def pos(self, pos: Vector):
        if not isinstance(pos, Vector):
            raise TypeError(f"Invalid type for position. Expected numpy array, got {type(pos)}.")

        self._pos = pos

    @property
    def handle_in(self) -> Vector:
        return self._handle_in
    
    @handle_in.setter
    def handle_in(self, handle_in: Vector):
        if not isinstance(handle_in, Vector):
            raise TypeError(f"Invalid type for position. Expected numpy array, got {type(handle_in)}.")

        self._handle_in = handle_in

    @property
    def handle_out(self) -> Vector:
        return self._handle_out
    
    @handle_out.setter
    def handle_out(self, handle_out: Vector):
        if not isinstance(handle_out, Vector):
            raise TypeError(f"Invalid type for position. Expected numpy array, got {type(handle_out)}.")

        self._handle_out = handle_out

    def reset_handles(self):
        self._handle_in = Vector()
        self._handle_out = Vector()

    def __repr__(self):
        return (f"AnchorPoint(pos=({str(self._pos[0])}, {str(self._pos[1])}, "
                f"in=({str(self._handle_in[0])}, {str(self._handle_in[1])}), "
                f"out=({self._handle_out[0]}, {self._handle_out[1]}), "
                f"handle_type='{self._handle_type}' )"
                )