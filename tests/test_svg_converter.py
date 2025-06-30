import pytest
import numpy as np
from bezier_builder.svg_converter import parse_svg_path
from bezier_builder.bezier_path import BezierPath

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
    np.testing.assert_array_equal(anchor_1.pos, np.array([10.0,20.0]))
    np.testing.assert_array_equal(anchor_2.pos, np.array([30.0,40.0]))
    np.testing.assert_array_equal(anchor_1.handle_in, np.array([0.0,0.0]))
    np.testing.assert_array_equal(anchor_1.handle_out, np.array([0.0,0.0]))
    np.testing.assert_array_equal(anchor_2.handle_in, np.array([0.0,0.0]))
    np.testing.assert_array_equal(anchor_2.handle_out, np.array([0.0,0.0]))

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
    np.testing.assert_array_equal(anchor_1.pos, np.array([10.0,20.0]))
    np.testing.assert_array_equal(anchor_2.pos, np.array([30.0,40.0]))
    np.testing.assert_array_equal(anchor_1.handle_in, np.array([0.0,0.0]))
    np.testing.assert_array_equal(anchor_1.handle_out, np.array([0.0,0.0]))
    np.testing.assert_array_equal(anchor_2.handle_in, np.array([0.0,0.0]))
    np.testing.assert_array_equal(anchor_2.handle_out, np.array([0.0,0.0]))

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
    np.testing.assert_array_equal(anchor_1.pos, np.array([100.0,100.0]))
    np.testing.assert_array_equal(anchor_2.pos, np.array([200.0,100.0]))
    np.testing.assert_array_equal(anchor_1.handle_out, np.array([20, -20]))
    np.testing.assert_array_equal(anchor_2.handle_in, np.array([-20, -20]))

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
    np.testing.assert_array_equal(anchor_1.pos, np.array([100.0,100.0]))
    np.testing.assert_array_equal(anchor_2.pos, np.array([200.0,100.0]))
    np.testing.assert_array_equal(anchor_1.handle_out, np.array([20, -20]))
    np.testing.assert_array_equal(anchor_2.handle_in, np.array([-20, -20]))

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
    assert len(path_list) == 2, "Expected list of one BezierPath"
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