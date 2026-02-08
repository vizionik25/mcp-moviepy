import pytest
import numpy as np
from moviepy import ColorClip
from custom_fx import Matrix
from unittest.mock import MagicMock

def is_numpy_mocked():
    return isinstance(np, MagicMock) or hasattr(np, 'assert_called')

@pytest.mark.skipif(is_numpy_mocked(), reason="numpy is mocked")
def test_matrix_determinism():
    """Test that two Matrix effects with the same seed produce identical output."""
    clip = ColorClip(size=(100, 100), color=(0, 0, 0), duration=1)

    # Create two effects with the same seed
    matrix1 = Matrix(seed=42)
    matrix2 = Matrix(seed=42)

    clip1 = matrix1.apply(clip)
    clip2 = matrix2.apply(clip)

    # Get a frame from each at the same timestamp
    frame1 = clip1.get_frame(0.5)
    frame2 = clip2.get_frame(0.5)

    np.testing.assert_array_equal(frame1, frame2)

@pytest.mark.skipif(is_numpy_mocked(), reason="numpy is mocked")
def test_matrix_variability():
    """Test that two Matrix effects with different seeds produce different output."""
    clip = ColorClip(size=(100, 100), color=(0, 0, 0), duration=1)

    # Create two effects with different seeds
    matrix1 = Matrix(seed=42)
    matrix2 = Matrix(seed=123)

    clip1 = matrix1.apply(clip)
    clip2 = matrix2.apply(clip)

    # Get a frame from each at the same timestamp
    frame1 = clip1.get_frame(0.5)
    frame2 = clip2.get_frame(0.5)

    # They should NOT be equal
    with pytest.raises(AssertionError):
        np.testing.assert_array_equal(frame1, frame2)

# This test might pass even with mocks, but let's be safe
@pytest.mark.skipif(is_numpy_mocked(), reason="numpy is mocked")
def test_global_seed_safety():
    """Test that the global random seed is not modified."""
    # Set a global seed
    np.random.seed(999)
    val1 = np.random.random()

    clip = ColorClip(size=(100, 100), color=(0, 0, 0), duration=1)
    matrix = Matrix(seed=42)

    # Apply and get frame to trigger random generation
    new_clip = matrix.apply(clip)
    _ = new_clip.get_frame(0.5)

    val2 = np.random.random()

    # Reset seed to verify what val2 should be
    np.random.seed(999)
    _ = np.random.random()
    expected_val2 = np.random.random()

    assert val2 == expected_val2, "Global random state was modified!"

if __name__ == "__main__":
    pytest.main([__file__])
