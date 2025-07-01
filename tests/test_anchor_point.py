import pytest
import numpy as np

from bezier_builder.anchor_point import AnchorPoint
from bezier_builder.vector import Vector

@pytest.fixture
def anchor():
    """
    This function is used to create an instance of the AnchorPoint class.
    """
    return AnchorPoint()

# Test that the initialize method sets default values for properties

def test_initialize_defaults(anchor):
    """
    Test that the initialize method sets default values for x and y coordinates.
    """
    assert anchor.handle_type == "corner"
    np.testing.assert_array_equal(anchor.pos, Vector(0.0, 0.0))
    np.testing.assert_array_equal(anchor._handle_in, Vector(0.0, 0.0))
    np.testing.assert_array_equal(anchor._handle_out, Vector(0.0, 0.0))
    
def test_initialize_with_args():
    """Tests initialization with specific coordinates."""
    x = 101.5
    y = -5.0
    ap = AnchorPoint(x, y)
    np.testing.assert_array_equal(ap.pos, np.array([x, y]))

def test_data_types_on_init(anchor):
    """Tests that vector attributes are numpy arrays with dtype=float32."""
    assert isinstance(anchor.pos, Vector)
    assert isinstance(anchor._handle_in, Vector)
    assert isinstance(anchor._handle_out, Vector)

# Test handle type logic

def test_handle_type_symmetrical(anchor):
    """Tests the behavior of the 'symmetrical' handle type."""
    anchor._handle_in = Vector(15.0, -25.0)
    
    # Set the type to symmetrical, which should trigger the alignment logic
    anchor.handle_type = "symmetric"
    
    # handle_out should be the exact opposite of handle_in
    expected_out = Vector(-15.0, 25.0)
    np.testing.assert_allclose(anchor._handle_out, expected_out)
    
    # Magnitudes should be equal
    assert np.linalg.norm(anchor._handle_in) == np.linalg.norm(anchor._handle_out)

def test_handle_type_aligned(anchor):
    """Tests the behavior of the 'aligned' handle type."""
    anchor._handle_in = Vector(10.0, 0.0)
    anchor._handle_out = Vector(0.0, -20.0) # A completely different vector
    
    original_out_magnitude = np.linalg.norm(anchor._handle_out)
    assert original_out_magnitude == 20.0 # Verify initial magnitude
    
    # Set the type to aligned
    anchor.handle_type = "aligned"

    # handle_out should now be aligned with handle_in but keep its magnitude
    expected_out_direction = -1 * anchor._handle_in.normalize()
    expected_out = expected_out_direction * original_out_magnitude

    np.testing.assert_allclose(anchor._handle_out, expected_out) # Checks direction
    assert np.isclose(np.linalg.norm(anchor._handle_out), original_out_magnitude) # Checks magnitude

def test_handle_type_corner(anchor):
    """Tests the behavior of the 'corner' handle type (independence)."""
    # 'corner' is the default, but we set it explicitly to be sure
    anchor.handle_type = "corner"
    
    handle_in_val = Vector(10, 20)
    handle_out_val = Vector(-30, 40)
    
    anchor._handle_in = handle_in_val
    anchor._handle_out = handle_out_val
    
    # In 'corner' mode, handles should be completely independent
    np.testing.assert_array_equal(anchor._handle_in, handle_in_val)
    np.testing.assert_array_equal(anchor._handle_out, handle_out_val)

# Test edge cases

def test_invalid_handle_type_raises_value_error(anchor):
    """Tests that setting an invalid handle type raises a ValueError."""
    with pytest.raises(ValueError) as excinfo:
        anchor.handle_type = "invalid_type"
    # Optionally check the error message
    assert "Invalid handle type" in str(excinfo.value)

def test_handle_type_change_with_zero_vector(anchor):
    """Tests alignment logic when the source handle is a zero vector."""
    anchor._handle_in = Vector(0.0, 0.0)
    anchor._handle_out = Vector(10.0, 10.0) # Give handle_out a value
    
    anchor.handle_type = "symmetric"
    
    # If handle_in is zero, handle_out should also become zero
    np.testing.assert_allclose(anchor._handle_out, Vector(0.0, 0.0))

def test_state_transition_to_corner(anchor):
    """Tests that handles become independent after switching back to 'corner'."""
    # 1. First, make them symmetric and linked
    anchor._handle_in = Vector(10, 10)
    anchor.handle_type = "symmetric"
    np.testing.assert_allclose(anchor._handle_out, Vector(-10, -10))
    
    # 2. Switch back to corner
    anchor.handle_type = "corner"
    
    # 3. Modify handle_in and verify handle_out is NOT affected
    original_out = anchor._handle_out.copy()
    anchor._handle_in = Vector(50, 50) # New value for handle_in
    
    np.testing.assert_allclose(anchor._handle_out, original_out)

def test_reset_handles(anchor):
    """Tests that the reset_handles method works correctly."""
    anchor._handle_in = Vector(10, 20)
    anchor._handle_out = Vector(30, 40)
    
    anchor.reset_handles()
    
    np.testing.assert_array_equal(anchor._handle_in, Vector(0, 0))
    np.testing.assert_array_equal(anchor._handle_out, Vector(0, 0))
