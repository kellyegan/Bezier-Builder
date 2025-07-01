# svg_converter.py

from typing import List
import numpy as np
from svgelements import Path, Move, Line, CubicBezier, QuadraticBezier, Close


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
                current_path.add_point(current_point)

            if isinstance(segment, CubicBezier):
                # The segment's start point corresponds to our *previous* AnchorPoint.
                # Its control1 defines the outgoing handle of that previous point.

                # Get absolute coordinates from the segment
                start = Vector.as_vector(segment.start)
                abs_handle_1 = Vector.as_vector(segment.control1)
                abs_handle_2 = Vector.as_vector(segment.control2)
                end = Vector.as_vector(segment.end)

                # Modify the previous points handle_out
                current_path.end_point.handle_out = abs_handle_1 - start

                handle_in = current_path.end_point.handle_in
                handle_out = current_path.end_point.handle_out
                
                if handle_in.mirrors(handle_out):
                    current_path.end_point.handle_type = "symmetric"
                elif handle_in.is_continuous_with(handle_out):
                    current_path.end_point.handle_type = "aligned"

                # Create the new anchor point for the end of the curve
                current_point = AnchorPoint(segment.end.x, segment.end.y)
                current_point.handle_in = abs_handle_2 - end

                current_path.add_point(current_point)

            if isinstance(segment, QuadraticBezier):
                start = Vector.as_vector(segment.start)
                control = Vector.as_vector(segment.control)
                end = Vector.as_vector(segment.end)

                # Modify the previous points handle_out
                current_path.end_point.handle_out = (2/3) * (control - start)

                # handle_in = current_path.end_point.handle_in
                # handle_out = -1 * current_path.end_point.handle_out
                
                # if np.isclose(handle_in.all(), handle_out.all()):
                #     current_path.end_point.handle_type = "symmetric"

                current_point = AnchorPoint(segment.end.x, segment.end.y)
                current_point.handle_in = (2/3) * (control - end)
                current_path.add_point(current_point)
            
            if isinstance(segment, (Line, Close)):
                current_point = AnchorPoint(segment.end.x, segment.end.y)
                current_path.add_point(current_point)

            if isinstance(segment, Close):
                current_path.is_closed = True

        is_closed = isinstance(subpath[-1], Close)
        path_list.append(current_path)
    return path_list
                
            
                

def build_svg_path(paths: List[BezierPath]) -> str:
    """
    Builds an SVG path 'd' attribute string from a list of BezierPath objects.

    Args:
        paths: A list of BezierPath objects.

    Returns:
        A string suitable for use in an SVG <path> 'd' attribute.
    """
    # The core logic will live here. It will need to:
    # 1. Iterate through each BezierPath in the list.
    # 2. For each path, start with a 'M' command for the first anchor point.
    # 3. Iterate through the remaining anchor points.
    # 4. **Crucially:** Decide whether to use a 'L' (Line) or 'C' (Curve) command.
    #    - If the previous point's handle_out and the current point's handle_in are both zero, use 'L'.
    #    - Otherwise, use 'C'.
    # 5. When building a 'C' command, convert the AnchorPoint's relative handles back to absolute SVG coordinates.
    #    - SVG `C` needs `(handle_out_absolute, handle_in_absolute, new_pos_absolute)`.
    #    - `handle_out_absolute = previous_point.pos + previous_point.handle_out`.
    #    - `handle_in_absolute = current_point.pos + current_point.handle_in`.
    # 6. If a path's 'is_closed' flag is True, append 'Z' to its command string.
    # 7. Join all command strings together.

    # Placeholder implementation
    pass