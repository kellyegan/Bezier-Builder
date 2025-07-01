import pytest
import numpy as np
from bezier_builder.svg_converter import parse_svg_path
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
    d="M 190 0 C 150 -20, 80 90, 100 110, C 120 130, 160 200, 200 210 C 240 220, 300 130, 280 100 C 260 70, 230 20, 190 0"
    path_list = parse_svg_path(d)
    bezier_path = path_list[0]
    assert len(bezier_path.anchor_points) == 4
    assert bezier_path.is_closed == True
    