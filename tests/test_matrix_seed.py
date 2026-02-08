
import pytest
import numpy as np
from moviepy import ColorClip
from custom_fx.matrix import Matrix

def test_matrix_reproducibility():
    """Test that Matrix effect produces identical output with the same seed."""
    clip = ColorClip(size=(100, 100), color=(0, 0, 0), duration=1)

    # Run with default seed (42)
    effect1 = Matrix(seed=42)
    out1 = effect1.apply(clip)
    frame1 = out1.get_frame(0.5)

    effect2 = Matrix(seed=42)
    out2 = effect2.apply(clip)
    frame2 = out2.get_frame(0.5)

    np.testing.assert_array_equal(frame1, frame2, err_msg="Frames should be identical for same seed")

def test_matrix_variability():
    """Test that Matrix effect produces different output with different seeds."""
    clip = ColorClip(size=(100, 100), color=(0, 0, 0), duration=1)

    # Run with seed 42
    effect1 = Matrix(seed=42)
    out1 = effect1.apply(clip)
    frame1 = out1.get_frame(0.5)

    # Run with seed 123
    effect2 = Matrix(seed=123)
    out2 = effect2.apply(clip)
    frame2 = out2.get_frame(0.5)

    with pytest.raises(AssertionError):
        np.testing.assert_array_equal(frame1, frame2, err_msg="Frames should be different for different seeds")

def test_default_seed_behavior():
    """Test that default seed is 42."""
    clip = ColorClip(size=(100, 100), color=(0, 0, 0), duration=1)

    effect1 = Matrix() # Should use default seed 42
    out1 = effect1.apply(clip)
    frame1 = out1.get_frame(0.5)

    effect2 = Matrix(seed=42)
    out2 = effect2.apply(clip)
    frame2 = out2.get_frame(0.5)

    np.testing.assert_array_equal(frame1, frame2, err_msg="Default seed should be 42")
