import pytest
import numpy as np

from bezier_builder.vector import Vector

@pytest.fixture
def vector():
    return Vector()

def test_initialize_defaults(vector):
    assert vector.shape == (2,)
    assert vector.dtype == np.float64
    assert vector.x == 0.0
    assert vector.y == 0.0

def test_initialize_with_args(vector):
    vector = Vector(1, 2)
    assert vector.x == 1.0 
    assert vector.y == 2.0

def test_setter_methods(vector):
    vector.x = 3
    vector.y = 4
    assert vector[0] == 3.0
    assert vector[1] == 4.0

def test_add_vectors(vector):
    vector = Vector(1, 2)
    other_vector = Vector(5, 6)
    result = vector + other_vector
    np.testing.assert_array_equal(result, np.array([6.0, 8.0]))
    assert isinstance(result, Vector)

def test_magnitude(vector):
    vector.x = 3
    vector.y = 4
    assert vector.magnitude() == 5.0

