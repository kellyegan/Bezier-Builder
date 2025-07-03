# svg_converter.py

from typing import List
import re
import math
from svgelements import Path, Move, Line, CubicBezier, QuadraticBezier, Arc, Close

from bezier_builder.bezier_path import BezierPath
from bezier_builder.anchor_point import AnchorPoint
from bezier_builder.vector import Vector


def parse_svg_path(d_string: str) -> List[BezierPath]:
    """
    Parses an SVG path 'd' attribute string into a list of BezierPath objects
    using the 'svgelements' library.

    Args:
        d_string: The string from the 'd' attribute of an SVG <path> element.

    Returns:
        A list of BezierPath objects.
    """
    path_list = []
    svg_path = Path(d_string)

    for subpath in svg_path.as_subpaths():
        current_path = BezierPath()

        if not subpath:
            continue

        for segment in subpath:
            # 'segment' is an object like Move, Line, CubicBezier, Close, etc.
            
            # The first point of any subpath is always a Move
            if isinstance(segment, Move):
                current_point = AnchorPoint(segment.end.x, segment.end.y)
                current_path.append(current_point)
            elif isinstance(segment, CubicBezier):
                # Get coordinates from the segment
                start = Vector.as_vector(segment.start)
                end = Vector.as_vector(segment.end)

                append_bezier_to_path(
                    handle_1=Vector.as_vector(segment.control1) - start,
                    handle_2=Vector.as_vector(segment.control2) - end,
                    end=end,
                    path=current_path
                    )
            elif isinstance(segment, QuadraticBezier):
                start = Vector.as_vector(segment.start)
                control = Vector.as_vector(segment.control)
                end = Vector.as_vector(segment.end)

                append_bezier_to_path(
                    handle_1=(2/3) * (control - start), 
                    handle_2=(2/3) * (control - end), 
                    end=end, 
                    path=current_path
                    )
            elif isinstance(segment, Arc):
                # Calculate number of segments based on angle approximatly 1 per 90 degrees
                num_segments = int(math.ceil(abs(segment.sweep) / (math.pi/2)))
                for bezier in segment.as_cubic_curves(arc_required=num_segments):
                    start = Vector.as_vector(bezier.start)
                    end = Vector.as_vector(bezier.end)

                    append_bezier_to_path(
                        handle_1=Vector.as_vector(bezier.control1) - start,
                        handle_2=Vector.as_vector(bezier.control2) - end,
                        end=end,
                        path=current_path
                        )
            elif isinstance(segment, (Line, Close)):
                current_point = AnchorPoint(segment.end.x, segment.end.y)
                current_path.append(current_point)

            if isinstance(segment, Close):
                current_path.is_closed = True

            if len(current_path.anchor_points) > 1:
                start = current_path.start
                end = current_path.end

                # If start and end points are the same remove extra point and mark is closed
                if start.pos.x == end.pos.x and start.pos.y == end.pos.y:
                    if(start.handle_out.mirrors(end.handle_in)):
                        current_path.start.handle_type = "symmetric"
                    elif(start.handle_out.is_continuous_with(end.handle_in)):
                        current_path.start.handle_type = "aligned"

                    current_path.start.handle_in = end.handle_in
                    current_path.anchor_points.pop()
                    current_path.is_closed = True

        path_list.append(current_path)
    return path_list

def append_bezier_to_path(handle_1: AnchorPoint, handle_2: AnchorPoint, end: AnchorPoint, path: BezierPath):
    """
    Appends a bezier curve to the given path object.

    Args:
        handle_1 (AnchorPoint): The relative handle point at the start of the bezier curve.
        handle_2 (AnchorPoint): The relative handle point at the end of the bezier curve.
        end (AnchorPoint): The end point of the bezier curve.
        path (BezierPath): The path object to which the bezier curve will be appended.
    """
    # Set previous anchors handle_out 
    path.end.handle_out = handle_1
    # Check if handles are aligned or symmetric
    path.end.detect_handle_type()

    current_point = AnchorPoint(end.x, end.y)
    current_point.handle_in = handle_2 
    path.append(current_point)

def build_svg_path(paths: List[BezierPath]) -> str:
    """
    Builds an SVG path 'd' attribute string from a list of BezierPath objects.

    Args:
        paths: A list of BezierPath objects.

    Returns:
        str: A string suitable for use in an SVG <path> 'd' attribute.
    """

    svg_string = ""
    
    for path in paths:
        svg_string += f"M {nf(path.start.pos.x)} {nf(path.start.pos.y)} "
        previous = path.start

        for i in range(1, len(path.anchor_points)):
            current = path.anchor_points[i]
            svg_string += bezier_string(previous, current)
            previous = current

        if path.is_closed:
            svg_string += bezier_string(path.end, path.start)
            
    return svg_string.rstrip()

def nf(value):
    """
    Format numbers to 5 decimal places, but remove trailing zeros.
    """
    s = f"{value:.5f}"
    s = re.sub("\.?0+$", "", s)
    return s

def bezier_string(prev, curr):
    """
    Generate a Bezier curve string for the given two points.
    If the handles are both zero, then we're just drawing a line.
    """
    str = ""
    
    if prev.handle_out.magnitude() == 0 and curr.handle_in.magnitude() == 0:
        str += f"L {nf(curr.pos.x)} {nf(curr.pos.y)} "
    else:
        c1 = prev.pos + prev.handle_out
        c2 = curr.pos + curr.handle_in
        str += f"C {nf(c1.x)} {nf(c1.y)} "
        str += f"{nf(c2.x)} {nf(c2.y)} "
        str += f"{nf(curr.pos.x)} {nf(curr.pos.y)} "

    return str

