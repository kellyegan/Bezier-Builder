import pytest
import numpy as np

from bezier_builder.bezier_path import BezierPath, BezierShape
from bezier_builder.anchor_point import AnchorPoint
from bezier_builder.vector import Vector

@pytest.fixture
def path():
    """
    This function is used to create an instance of the BezierPath class.
    """
    return BezierPath()

@pytest.fixture
def shape():
    """
    This function is used to create an instance of the BezierShape class.
    """
    return BezierShape()

def test_initialize_path(path: BezierPath):
    """
    Test initializing BezierPath object and defaults
    """
    assert path != None
    assert isinstance(path.anchor_points, list)
    assert path.is_closed == False

def test_add_point(path: BezierPath):
    assert len(path.anchor_points) == 0
    point = AnchorPoint()
    path.append(point)
    assert len(path.anchor_points) == 1

def test_create_point_defaults(path: BezierPath):
    assert len(path.anchor_points) == 0
    path.create()
    assert len(path.anchor_points) == 1
    point = path.anchor_points[-1]
    assert isinstance(point, AnchorPoint)
    np.testing.assert_array_equal(point.pos, Vector())
    np.testing.assert_array_equal(point.handle_in, Vector())
    np.testing.assert_array_equal(point.handle_out,Vector())
    assert point.handle_type == "corner"

def test_create_point(path: BezierPath):
    pos = Vector(1,2)
    handle_in = Vector(-.5,-1)
    handle_out = Vector(2,4)
    path.create(pos=pos, handle_in=handle_in, handle_out=handle_out, type="aligned")
    point = path.anchor_points[-1]
    assert isinstance(point, AnchorPoint)
    np.testing.assert_array_equal(point.pos, Vector(1,2))
    np.testing.assert_array_equal(point.handle_in, Vector(-.5,-1))
    np.testing.assert_array_equal(point.handle_out, Vector(2, 4))
    assert point.handle_type == "aligned"

    pos = Vector(0,0)
    handle_in = Vector(-1,-2)
    handle_out = Vector(1,2)
    path.create(pos=pos, handle_in=handle_in, handle_out=handle_out, type="symmetric")
    point = path.anchor_points[-1]
    assert isinstance(point, AnchorPoint)
    np.testing.assert_array_equal(point.pos, Vector())
    np.testing.assert_array_equal(point.handle_in, Vector(-1,-2))
    np.testing.assert_array_equal(point.handle_out, Vector(1, 2))
    assert point.handle_type == "symmetric"

def test_start_end_previous_points():
    path = BezierPath()
    assert path.start is None, "Expected start to be None when no anchors in path"
    assert path.end is None, "Expected end to be None when no anchors in path"
    assert path.previous_point is None, "Expected previous to be None when no anchors in path"
    path.create(pos=Vector(0,0))
    assert isinstance(path.start, AnchorPoint)
    assert path.start is path.end, "Expected start and end to be the same point"
    assert path.previous_point is None, "Expected previous to be None when only 1 point in path"
    path.create(pos=Vector(15,20))
    assert isinstance(path.start, AnchorPoint)
    np.testing.assert_array_equal(path.start.pos, Vector(0,0))
    assert isinstance(path.end, AnchorPoint)
    np.testing.assert_array_equal(path.end.pos, Vector(15,20))
    assert path.start is path.previous_point, "Expected start to be previous when only 2 points in path"
    path.create(pos=Vector(35,40))
    assert isinstance(path.start, AnchorPoint)
    np.testing.assert_array_equal(path.start.pos, Vector(0,0))
    assert isinstance(path.previous_point, AnchorPoint)
    np.testing.assert_array_equal(path.previous_point.pos,  Vector(15,20))
    assert isinstance(path.end, AnchorPoint)
    np.testing.assert_array_equal(path.end.pos, Vector(35,40))

def test_initialize_shape(shape: BezierShape, path: BezierPath):
    """
    Test initializing BezierPath object and defaults
    """
    assert shape != None
    shape.append(path)
    assert len(shape) == 1
