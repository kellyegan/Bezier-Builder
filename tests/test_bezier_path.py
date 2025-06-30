import pytest
import numpy as np

from bezier_builder.bezier_path import BezierPath
from bezier_builder.anchor_point import AnchorPoint

@pytest.fixture
def path():
    """
    This function is used to create an instance of the AnchorPoint class.
    """
    return BezierPath()

def test_initialize(path: BezierPath):
    """
    Test initializing BezierPath object and defaults
    """
    assert path != None
    assert isinstance(path.anchors, list)
    assert path.closed == False

def test_add_point(path: BezierPath):
    assert len(path.anchors) == 0
    point = AnchorPoint()
    path.add_point(point)
    assert len(path.anchors) == 1

def test_create_point_defaults(path: BezierPath):
    assert len(path.anchors) == 0
    path.create_point()
    assert len(path.anchors) == 1
    point = path.anchors[-1]
    assert isinstance(point, AnchorPoint)
    np.testing.assert_array_equal(point.pos, np.array([0,0]))
    np.testing.assert_array_equal(point.handle_in, np.array([0,0]))
    np.testing.assert_array_equal(point.handle_out, np.array([0,0]))
    assert point.handle_type == "corner"

def test_create_point(path: BezierPath):
    path.create_point(pos=(1,2), handle_in=(-.5,-1), handle_out=(2,4), type="aligned")
    point = path.anchors[-1]
    assert isinstance(point, AnchorPoint)
    np.testing.assert_array_equal(point.pos, np.array([1,2]))
    np.testing.assert_array_equal(point.handle_in, np.array([-0.5,-1]))
    np.testing.assert_array_equal(point.handle_out, np.array([2,4]))
    assert point.handle_type == "aligned"

    path.create_point(pos=(0,0), handle_in=(-1,-2), handle_out=(1,2), type="symmetrical")
    point = path.anchors[-1]
    assert isinstance(point, AnchorPoint)
    np.testing.assert_array_equal(point.pos, np.array([0,0]))
    np.testing.assert_array_equal(point.handle_in, np.array([-1,-2]))
    np.testing.assert_array_equal(point.handle_out, np.array([1,2]))
    assert point.handle_type == "symmetrical"