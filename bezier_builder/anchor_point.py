import numpy as np
from bezier_builder.utils import unit_vector

class AnchorPoint:
   
    def __init__(self, x=0.0, y=0.0):
      self._handle_type = "corner"
      self._pos = np.array([x, y], dtype=np.float32)
      self._handle_in = np.array([0, 0], dtype=np.float32)
      self._handle_out = np.array([0, 0], dtype=np.float32)

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
    def pos(self) -> np.ndarray:
        return self._pos
    
    @pos.setter
    def pos(self, pos: np.ndarray):
        pos = np.array(pos)
        
        if not isinstance(pos, np.ndarray):
            raise TypeError(f"Invalid type for position. Expected numpy array, got {type(pos)}.")

        self._pos = pos.astype(np.float32)

    @property
    def handle_in(self) -> np.ndarray:
        return self._handle_in
    
    @handle_in.setter
    def handle_in(self, handle_in: np.ndarray):
        handle_in = np.array(handle_in)
        
        if not isinstance(handle_in, np.ndarray):
            raise TypeError(f"Invalid type for position. Expected numpy array, got {type(handle_in)}.")

        self._handle_in = handle_in.astype(np.float32)

    @property
    def handle_out(self) -> np.ndarray:
        return self._handle_out
    
    @handle_out.setter
    def handle_out(self, handle_out: np.ndarray):
        handle_out = np.array(handle_out)
        
        if not isinstance(handle_out, np.ndarray):
            raise TypeError(f"Invalid type for position. Expected numpy array, got {type(handle_out)}.")

        self._handle_out = handle_out.astype(np.float32)

    def reset_handles(self):
        self._handle_in = np.array([0, 0])
        self._handle_out = np.array([0, 0])

    def __repr__(self):
        return (f"AnchorPoint(pos=({str(self._pos[0])}, {str(self._pos[1])}, "
                f"in=({str(self._handle_in[0])}, {str(self._handle_in[1])}), "
                f"out=({self._handle_out[0]}, {self._handle_out[1]}), "
                f"handle_type='{self._handle_type}' )"
                )