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

def test_create_point(path: BezierPath):
    assert len(path.anchors) == 0
    path.create_point(pos=(1.0,51.0), handle_in=(7.0,20.5), handle_out=(40.0,60.0), type="aligned")
    assert len(path.anchors) == 1
    point = path.anchors[-1]
    assert isinstance(point, AnchorPoint)
    np.testing.assert_array_equal(point.pos, np.array([1.0, 51.0]))
    np.testing.assert_array_equal(point.handle_in, np.array([7.0,20.5]))
    np.testing.assert_array_equal(point.handle_out, np.array([40.0,60.0]))
    assert point.handle_type == "aligned"