import numpy as np

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
        if handle_type not in ["corner", "aligned", "symmetrical"]:
            raise ValueError(f"Invalid handle type: '{handle_type}'. Must be one of 'corner', 'aligned' or 'symmetrical'.")
        
        self._handle_type = handle_type

    @property
    def pos(self) -> np.ndarray:
        return self._pos
    
    @pos.setter
    def pos(self, pos: np.ndarray):
        if isinstance(pos, list):
            pos = np.array(pos)
        
        if not isinstance(pos, np.ndarray):
            raise TypeError(f"Invalid type for position. Expected numpy array, got {type(pos)}.")

        self._pos = pos.astype(np.float32)