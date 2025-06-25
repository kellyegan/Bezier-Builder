class AnchorPoint:
   
    def __init__(self):
      self._handle_type = "corner"

    @property
    def handle_type(self) -> str:
        return self._handle_type
   
    @handle_type.setter
    def handle_type(self, handle_type: str):
        if handle_type not in ["corner", "aligned", "symmetrical"]:
            raise ValueError(f"Invalid handle type: '{handle_type}'. Must be one of 'corner', 'aligned' or 'symmetrical'.")
        
        self._handle_type = handle_type