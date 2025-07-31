from bezier_builder.anchor_point import AnchorPoint
from bezier_builder.vector import Vector


class BezierPath:
    """
    Class to define a single cubic bezier path with a list of anchor points 
    rather than bezier segments
    """
    def __init__(self):
        self._anchor_points = []
        self._is_closed = False

    def __iter__(self):
        return iter(self._anchor_points)

    @property
    def anchor_points(self) -> list:
        return self._anchor_points
    
    @anchor_points.setter
    def anchor_points(self, anchors:list[AnchorPoint]):
        self._anchor_points = anchors

    @property
    def is_closed(self) -> bool:
        return self._is_closed
    
    @is_closed.setter
    def is_closed(self, is_closed:bool):
        self._is_closed = is_closed

    @property
    def start(self) -> AnchorPoint:
        if len(self._anchor_points) > 0:
            return self._anchor_points[0]
        return None
        
    @property
    def end(self) -> AnchorPoint:
        if len(self._anchor_points) > 0:
           return self._anchor_points[-1]
        return None
        
    @property
    def previous_point(self) -> AnchorPoint:
        if len(self._anchor_points) > 1:
            return self._anchor_points[-2]
        return None
    
    def append(self, anchor: AnchorPoint):
        if not isinstance(anchor, AnchorPoint):
            raise TypeError("Anchor must be an instance of AnchorPoint")
        self._anchor_points.append(anchor)

    def create(self, pos=Vector(0.0,0.0), handle_in=Vector(0.0,0.0), handle_out=Vector(0.0,0.0), type="corner"):
        point = AnchorPoint()
        point.pos = pos
        point.handle_in = handle_in
        point.handle_out = handle_out
        point.handle_type = type
        self.anchor_points.append(point)
        pass

    def __repr__(self):
        return f"BezierPath(points={len(self._anchor_points)}, is_closed={self.is_closed})"

