import numpy as np

def unit_vector(vector: np.ndarray) -> np.ndarray:
    """
    Returns the unit vector of the given vector.
    """
    magnitude = np.linalg.norm(vector)
    return vector / magnitude if magnitude != 0 else vector