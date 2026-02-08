import numpy as np
from custom_fx.matrix import Matrix
from moviepy import ColorClip

def test_matrix_determinism():
    """Test that Matrix effect is deterministic with the same seed."""
    clip = ColorClip(size=(100, 100), color=(0, 0, 0), duration=1)

    # Run 1 with seed 42
    effect1 = Matrix(seed=42)
    res1 = effect1.apply(clip)
    frame1 = res1.get_frame(0.5)

    # Run 2 with seed 42
    effect2 = Matrix(seed=42)
    res2 = effect2.apply(clip)
    frame2 = res2.get_frame(0.5)

    # Run 3 with seed 123
    effect3 = Matrix(seed=123)
    res3 = effect3.apply(clip)
    frame3 = res3.get_frame(0.5)

    # Check equality for same seed
    np.testing.assert_array_equal(frame1, frame2, err_msg="Frames should be identical for same seed")

    # Check inequality for different seed
    # Note: It's theoretically possible but highly unlikely that they are identical.
    # We check if they differ.
    assert not np.array_equal(frame1, frame3), "Frames should differ for different seeds"

def test_matrix_default_seed():
    """Test that default seed is 42."""
    clip = ColorClip(size=(100, 100), color=(0, 0, 0), duration=1)

    effect1 = Matrix() # Default seed
    effect2 = Matrix(seed=42)

    res1 = effect1.apply(clip)
    res2 = effect2.apply(clip)

    frame1 = res1.get_frame(0)
    frame2 = res2.get_frame(0)

    np.testing.assert_array_equal(frame1, frame2, err_msg="Default seed should be 42")

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
import pytest
import numpy as np
from moviepy import ColorClip
from custom_fx import Matrix

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
