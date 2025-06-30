from bezier_builder.anchor_point import AnchorPoint

class BezierPath:
    def __init__(self):
        self._anchors = []
        self._is_closed = False

    @property
    def anchors(self) -> list:
        return self._anchors
    
    @anchors.setter
    def anchors(self, anchors:list[AnchorPoint]):
        self._anchors = anchors

    @property
    def is_closed(self) -> bool:
        return self._is_closed
    
    @is_closed.setter
    def is_closed(self, is_closed:bool):
        self._is_closed = is_closed
    
    def add_point(self, anchor):
        self._anchors.append(anchor)

    def create_point(self, pos=(0.0,0.0), handle_in=(0.0,0.0), handle_out=(0.0,0.0), type="corner"):
        point = AnchorPoint()
        point.pos = pos
        point.handle_in = handle_in
        point.handle_out = handle_out
        point.handle_type = type
        self.anchors.append(point)
        pass

    