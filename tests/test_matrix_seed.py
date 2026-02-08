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
