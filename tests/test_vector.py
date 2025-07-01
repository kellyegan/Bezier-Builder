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
    assert isinstance(vector.magnitude(), float)

def test_normalize(vector):
    vector.x = 3
    vector.y = 4
    result = vector.normalize()
    desired_vector = Vector(3 /5, 4 / 5)
    np.testing.assert_almost_equal(result, desired_vector)
    
def test_parallel():
    vector1 = Vector(4, 6)
    vector2 = Vector(6, 9)
    assert vector1.is_parallel_to(vector2)
    vector2 = Vector(5, 9)
    assert not vector1.is_parallel_to(vector2)

def test_continuous():
    vector1 = Vector(4, 6)
    vector2 = Vector(-8, -12)
    assert vector1.is_continuous_with(vector2)
    vector2 = Vector(-3, -6)
    assert not vector1.is_continuous_with(vector2)
    vector2 = Vector(8, 12)
    assert not vector1.is_continuous_with(vector2)

def test_mirrors():
    vector1 = Vector(4, 6)
    vector2 = Vector(-4, -6)
    assert vector1.mirrors(vector2)  
    vector2 = Vector(-8, -12)
    assert not vector1.mirrors(vector2)  