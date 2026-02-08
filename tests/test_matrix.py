
import pytest
import numpy as np
from moviepy import ColorClip
from custom_fx.matrix import Matrix

def test_matrix_consistency_default():
    # Two instances with default seed (42) should be identical
    m1 = Matrix()
    m2 = Matrix()

    clip = ColorClip(size=(100, 100), color=(0, 0, 0), duration=2)

    c1 = m1.apply(clip)
    c2 = m2.apply(clip)

    # Use t=1.0 to ensure rain has fallen
    f1 = c1.get_frame(1.0)
    f2 = c2.get_frame(1.0)

    np.testing.assert_array_equal(f1, f2, err_msg="Default seed should produce identical frames")

def test_matrix_different_seeds():
    # Two instances with different seeds should be different
    m1 = Matrix(seed=42)
    m2 = Matrix(seed=123)

    clip = ColorClip(size=(200, 200), color=(0, 0, 0), duration=2) # Larger size to ensure hits

    c1 = m1.apply(clip)
    c2 = m2.apply(clip)

    # Check multiple frames to be sure
    t = 1.0
    f1 = c1.get_frame(t)
    f2 = c2.get_frame(t)

    # Assert at least some pixels are different
    # If both are completely black, then it's not a good test of randomness, but rather of density/visibility.
    if f1.max() == 0 and f2.max() == 0:
        pytest.fail("Both frames are empty (black), cannot test difference. Increase density or size.")

    with pytest.raises(AssertionError):
        np.testing.assert_array_equal(f1, f2)

def test_matrix_consistency_custom_seed():
    # Two instances with same custom seed should be identical
    m1 = Matrix(seed=999)
    m2 = Matrix(seed=999)

    clip = ColorClip(size=(100, 100), color=(0, 0, 0), duration=2)

    c1 = m1.apply(clip)
    c2 = m2.apply(clip)

    f1 = c1.get_frame(1.0)
    f2 = c2.get_frame(1.0)

    np.testing.assert_array_equal(f1, f2, err_msg="Same custom seed should produce identical frames")

def test_global_seed_untouched():
    np.random.seed(123)
    pre_val = np.random.random()

    m = Matrix(seed=555)
    clip = ColorClip(size=(100, 100), color=(0, 0, 0), duration=1)
    c = m.apply(clip)
    c.get_frame(0)

    post_val = np.random.random()

    # Reset seed to verify prediction
    np.random.seed(123)
    np.random.random() # consume pre_val
    expected_post_val = np.random.random()

    assert post_val == expected_post_val, "Global random seed was modified!"
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
