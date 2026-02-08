
import pytest
import numpy as np
from moviepy import ColorClip
from custom_fx.matrix import Matrix

def test_matrix_consistency_default():
    """Test that the Matrix effect is consistent with the default seed (42)."""
    clip = ColorClip(size=(100, 100), color=(0, 0, 0), duration=1)

    effect1 = Matrix()
    res1 = effect1.apply(clip)
    frame1 = res1.get_frame(0)

    effect2 = Matrix()
    res2 = effect2.apply(clip)
    frame2 = res2.get_frame(0)

    np.testing.assert_array_equal(frame1, frame2)

def test_matrix_consistency_explicit_seed():
    """Test that the Matrix effect is consistent with an explicit seed."""
    clip = ColorClip(size=(100, 100), color=(0, 0, 0), duration=1)
    seed = 123

    effect1 = Matrix(seed=seed)
    res1 = effect1.apply(clip)
    frame1 = res1.get_frame(0)

    effect2 = Matrix(seed=seed)
    res2 = effect2.apply(clip)
    frame2 = res2.get_frame(0)

    np.testing.assert_array_equal(frame1, frame2)

def test_matrix_different_seeds():
    """Test that different seeds produce different results."""
    clip = ColorClip(size=(100, 100), color=(0, 0, 0), duration=1)

    effect1 = Matrix(seed=42)
    res1 = effect1.apply(clip)
    frame1 = res1.get_frame(0)

    effect2 = Matrix(seed=43)
    res2 = effect2.apply(clip)
    frame2 = res2.get_frame(0)

    with pytest.raises(AssertionError):
        np.testing.assert_array_equal(frame1, frame2)

def test_matrix_randomness_none_seed():
    """
    Test that seed=None produces different results (randomness).
    Note: It's theoretically possible for two random seeds to produce same result, but extremely unlikely.
    """
    clip = ColorClip(size=(100, 100), color=(0, 0, 0), duration=1)

    effect1 = Matrix(seed=None)
    res1 = effect1.apply(clip)
    frame1 = res1.get_frame(0)

    effect2 = Matrix(seed=None)
    res2 = effect2.apply(clip)
    frame2 = res2.get_frame(0)

    # Assert they are NOT equal
    with pytest.raises(AssertionError):
        np.testing.assert_array_equal(frame1, frame2)
