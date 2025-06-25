import pytest
import numpy as np

from bezier_builder.anchor_point import AnchorPoint

@pytest.fixture
def anchor():
    """
    This function is used to create an instance of the AnchorPoint class.
    """
    return AnchorPoint()

def test_initialize_defaults(anchor):
    """
    Test that the initialize method sets default values for x and y coordinates.
    """
    assert anchor.handle_type == "corner"
    np.testing.assert_array_equal(anchor.pos, np.array([0.0, 0.0]))
    