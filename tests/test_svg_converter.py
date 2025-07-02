import pytest
import numpy as np
from bezier_builder.svg_converter import parse_svg_path, build_svg_path
from bezier_builder.bezier_path import BezierPath
from bezier_builder.anchor_point import AnchorPoint
from bezier_builder.vector import Vector

def test_move_to_line_to():
    d = "M 10 20 L 30 40"
    path_list = parse_svg_path(d)
    assert len(path_list) == 1, "Expected list of one BezierPath"
    bezier_path = path_list[0]
    assert isinstance(bezier_path, BezierPath)
    assert len(bezier_path.anchor_points) == 2, "Expected two AnchorPoints"
    assert bezier_path.is_closed == False
    anchor_1 = bezier_path.anchor_points[0]
    anchor_2 = bezier_path.anchor_points[1]
    np.testing.assert_array_equal(anchor_1.pos, Vector(10.0,20.0))
    np.testing.assert_array_equal(anchor_2.pos, Vector(30.0,40.0))
    np.testing.assert_array_equal(anchor_1.handle_in, Vector(0.0,0.0))
    np.testing.assert_array_equal(anchor_1.handle_out, Vector(0.0,0.0))
    np.testing.assert_array_equal(anchor_2.handle_in, Vector(0.0,0.0))
    np.testing.assert_array_equal(anchor_2.handle_out, Vector(0.0,0.0))

def test_move_to_line_to_relative():
    d="M 10 20 l 20 20"
    path_list = parse_svg_path(d)
    assert len(path_list) == 1, "Expected list of one BezierPath"
    bezier_path = path_list[0]
    assert isinstance(bezier_path, BezierPath)
    assert len(bezier_path.anchor_points) == 2, "Expected two AnchorPoints"
    assert bezier_path.is_closed == False
    anchor_1 = bezier_path.anchor_points[0]
    anchor_2 = bezier_path.anchor_points[1]
    np.testing.assert_array_equal(anchor_1.pos, Vector(10.0,20.0))
    np.testing.assert_array_equal(anchor_2.pos, Vector(30.0,40.0))
    np.testing.assert_array_equal(anchor_1.handle_in, Vector(0.0,0.0))
    np.testing.assert_array_equal(anchor_1.handle_out, Vector(0.0,0.0))
    np.testing.assert_array_equal(anchor_2.handle_in, Vector(0.0,0.0))
    np.testing.assert_array_equal(anchor_2.handle_out, Vector(0.0,0.0))

def test_cubic_bezier():
    d="M 100 100 C 120 80, 180 80, 200 100"
    path_list = parse_svg_path(d)
    assert len(path_list) == 1, "Expected list of one BezierPath"
    bezier_path = path_list[0]
    assert isinstance(bezier_path, BezierPath)
    assert len(bezier_path.anchor_points) == 2, "Expected two AnchorPoints"
    assert bezier_path.is_closed == False
    anchor_1 = bezier_path.anchor_points[0]
    anchor_2 = bezier_path.anchor_points[1]
    np.testing.assert_array_equal(anchor_1.pos, Vector(100,100))
    np.testing.assert_array_equal(anchor_2.pos, Vector(200,100))
    np.testing.assert_array_equal(anchor_1.handle_out, Vector(20,-20))
    np.testing.assert_array_equal(anchor_2.handle_in, Vector(-20,-20))

def test_cubic_bezier_relative():
    d="M 100 100 c 20 -20, 80 -20, 100 0"
    path_list = parse_svg_path(d)
    assert len(path_list) == 1, "Expected list of one BezierPath"
    bezier_path = path_list[0]
    assert isinstance(bezier_path, BezierPath)
    assert len(bezier_path.anchor_points) == 2, "Expected two AnchorPoints"
    assert bezier_path.is_closed == False
    anchor_1 = bezier_path.anchor_points[0]
    anchor_2 = bezier_path.anchor_points[1]
    np.testing.assert_array_equal(anchor_1.pos, Vector(100.0,100.0))
    np.testing.assert_array_equal(anchor_1.handle_out, np.array([20, -20]))
    np.testing.assert_array_equal(anchor_2.pos, Vector(200.0,100.0))
    np.testing.assert_array_equal(anchor_2.handle_in, np.array([-20, -20]))

def test_quadratic_bezier():
    d="M 40 70 Q 70 91, 100 70"
    path_list = parse_svg_path(d)
    assert len(path_list) == 1
    bezier_path = path_list[0]
    assert isinstance(bezier_path, BezierPath)
    assert len(bezier_path.anchor_points) == 2, "Expected two AnchorPoints"
    anchor_1 = bezier_path.anchor_points[0]
    anchor_2 = bezier_path.anchor_points[1]  
    np.testing.assert_array_equal(anchor_1.pos, Vector(40.0,70.0))
    np.testing.assert_array_equal(anchor_1.handle_out, np.array([20, 14]))
    np.testing.assert_array_equal(anchor_2.pos, np.array([100, 70]))
    np.testing.assert_array_equal(anchor_2.handle_in, np.array([-20, 14]))

def test_closed_path():
    d="M 0 0 L 10 0 L 10 10 Z"
    path_list = parse_svg_path(d)
    assert len(path_list) == 1, "Expected list of one BezierPath"
    bezier_path = path_list[0]
    assert isinstance(bezier_path, BezierPath)
    assert bezier_path.is_closed == True

def test_multiple_subpaths():
    d="M 0 0 L 10 10 M 50 50 L 60 60"
    path_list = parse_svg_path(d)
    assert len(path_list) == 2, "Expected list of two BezierPath"
    bezier_path_1 = path_list[0]
    assert isinstance(bezier_path_1, BezierPath)
    anchor_1 = bezier_path_1.anchor_points[0]
    anchor_2 = bezier_path_1.anchor_points[1]
    np.testing.assert_array_equal(anchor_1.pos, [0.0, 0.0])
    np.testing.assert_array_equal(anchor_2.pos, [10.0, 10.0])
    bezier_path_2 = path_list[1]
    assert isinstance(bezier_path_2, BezierPath)
    anchor_1 = bezier_path_2.anchor_points[0]
    anchor_2 = bezier_path_2.anchor_points[1]
    np.testing.assert_array_equal(anchor_1.pos, [50.0, 50.0])
    np.testing.assert_array_equal(anchor_2.pos, [60.0, 60.0])

def test_symmetric_anchor():
    d="M 10 6 C 12 10, 17 20, 20 18 C 23 16, 24 8, 28 8"
    path_list = parse_svg_path(d)
    assert len(path_list) == 1, "Expected list of one BezierPath"
    bezier_path = path_list[0]
    assert isinstance(bezier_path, BezierPath)
    assert len(bezier_path.anchor_points) == 3
    anchor = bezier_path.anchor_points[1]
    np.testing.assert_array_equal(anchor.pos, [20.0, 18.0])
    np.testing.assert_array_equal(anchor.handle_in, [-3, 2.0])
    np.testing.assert_array_equal(anchor.handle_out, [3, -2.0])
    assert anchor.handle_type == "symmetric"

def test_aligned_anchor():
    d="M 10 6 C 12 10, 14 22, 20 18 C 23 16, 24 8, 28 8"
    path_list = parse_svg_path(d)
    bezier_path = path_list[0]
    assert len(bezier_path.anchor_points) == 3
    anchor = bezier_path.anchor_points[1]
    assert anchor.handle_type == "aligned"

def test_closed_smoothly():
    d="M 190, 0 L 100, 110 L 200, 210 L 280, 100 L 190, 0"
    path_list = parse_svg_path(d)
    bezier_path = path_list[0]
    assert len(bezier_path.anchor_points) == 4
    assert bezier_path.is_closed == True

    # Create a path with a SYMMETRIC transition between start and end
    d="M 95 0 C 75 10, 80 100, 100 105 C 120 110, 140 65, 140 50 C 140 35, 115 -10, 95 0"
    path_list = parse_svg_path(d)
    bezier_path = path_list[0]
    assert len(bezier_path.anchor_points) == 3
    assert bezier_path.is_closed == True

    for anchor in bezier_path.anchor_points:
        assert anchor.handle_type == "symmetric"

    # Create a path with a ALIGNED transition between start and end
    d="M 95 0 C 65 15, 80 100, 100 105 C 140 115, 140 65, 140 50 C 140 25, 115 -10, 95 0"
    path_list = parse_svg_path(d)
    bezier_path = path_list[0]
    assert len(bezier_path.anchor_points) == 3
    assert bezier_path.is_closed == True

    for anchor in bezier_path:
        assert anchor.handle_type == "aligned"

    # Check SYMMETRIC closed paths on quadratic beziers
    d="M -50 0 Q -50 50 0 50 Q 50, 50 50 0 Q 50 -50 0 -50 Q -50 -50 -50 0"
    path_list = parse_svg_path(d)
    bezier_path = path_list[0]
    assert len(bezier_path.anchor_points) == 4
    assert bezier_path.is_closed == True

    for anchor in bezier_path:
        assert anchor.handle_type == "symmetric"

    # Check ALIGNED closed paths on quadratic beziers
    d="M -50 0 Q -60 30 0 50 Q 30, 60 50 0 Q 60 -30 0 -50 Q -30 -60 -50 0"
    path_list = parse_svg_path(d)
    bezier_path = path_list[0]
    assert len(bezier_path.anchor_points) == 4
    assert bezier_path.is_closed == True

    for anchor in bezier_path:
        assert anchor.handle_type == "aligned"
    

def test_build_line_string():
    path = BezierPath()
    path.create(pos=Vector(10, 20))
    path.create(pos=Vector(30, 40))
    svg_string = build_svg_path([path])
    assert svg_string == "M 10 20 L 30 40"

def test_build_curve_string():
    path = BezierPath()
    path.create(pos=Vector(100, 100), handle_out=Vector(20, -20))
    path.create(pos=Vector(200, 100), handle_in=Vector(-20, -20))
    svg_string = build_svg_path([path])
    assert svg_string == "M 100 100 C 120 80 180 80 200 100"

def test_closed_path():
    # Closed linear path
    path = BezierPath()
    path.create(pos=Vector(60, 20))
    path.create(pos=Vector(10, 70))
    path.create(pos=Vector(110, 70))
    path.is_closed = True
    svg_string = build_svg_path([path])
    assert svg_string == "M 60 20 L 10 70 L 110 70 L 60 20"

    # Closed curved path
    path = BezierPath()
    path.create(pos=Vector(60, 20), handle_in=Vector(20,0), handle_out=Vector(-20,0))
    path.create(pos=Vector(10, 70), handle_in=Vector(-10,-20), handle_out=Vector(10,20))
    path.create(pos=Vector(110, 70), handle_in=Vector(-10,20), handle_out=Vector(10,-20))
    path.is_closed = True
    svg_string = build_svg_path([path])
    assert svg_string == "M 60 20 C 40 20 0 50 10 70 C 20 90 100 90 110 70 C 120 50 80 20 60 20"

def test_multiple_paths():
    # Closed linear path
    path1 = BezierPath()
    path1.create(pos=Vector(60, 20))
    path1.create(pos=Vector(10, 70))
    path1.create(pos=Vector(110, 70))
    path1.is_closed = True

    # Closed curved path
    path2 = BezierPath()
    path2.create(pos=Vector(60, 20), handle_in=Vector(20,0), handle_out=Vector(-20,0))
    path2.create(pos=Vector(10, 70), handle_in=Vector(-10,-20), handle_out=Vector(10,20))
    path2.create(pos=Vector(110, 70), handle_in=Vector(-10,20), handle_out=Vector(10,-20))
    path2.is_closed = True
    svg_string = build_svg_path([path1, path2])
    assert svg_string == "M 60 20 L 10 70 L 110 70 L 60 20 M 60 20 C 40 20 0 50 10 70 C 20 90 100 90 110 70 C 120 50 80 20 60 20"    