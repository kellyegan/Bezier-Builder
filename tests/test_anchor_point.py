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
    np.testing.assert_array_equal(anchor._handle_in, np.array([0.0, 0.0]))
    np.testing.assert_array_equal(anchor._handle_out, np.array([0.0, 0.0]))
    
def test_initialize_with_args():
    """Tests initialization with specific coordinates."""
    x = 101.5
    y = -5.0
    ap = AnchorPoint(x, y)
    np.testing.assert_array_equal(ap.pos, np.array([x, y]))

def test_data_types_on_init(anchor):
    """Tests that vector attributes are numpy arrays with dtype=float32."""
    assert isinstance(anchor.pos, np.ndarray)
    assert isinstance(anchor._handle_in, np.ndarray)
    assert isinstance(anchor._handle_out, np.ndarray)

    assert anchor.pos.dtype == np.float32
    assert anchor._handle_in.dtype == np.float32
    assert anchor._handle_out.dtype == np.float32

def test_pos_setter_type_conversion(anchor):
    """Tests that the pos setter correctly converts lists/tuples to float32 ndarray."""
    anchor.pos = [100, 200]  # Set with a list of ints
    assert anchor.pos.dtype == np.float32
    np.testing.assert_array_equal(anchor.pos, np.array([100.0, 200.0]))