
import numpy as np
import pytest
from moviepy import ColorClip
from custom_fx.matrix import Matrix

def test_matrix_determinism():
    """Verify that two matrix effects with same seed produce same results."""
    # Use density=1.0 to ensure rain is visible
    clip = ColorClip(size=(100, 100), color=(0, 0, 0), duration=1)

    # Effect 1
    m1 = Matrix(seed=42, density=1.0)
    clip1 = m1.apply(clip)
    frame1 = clip1.get_frame(0)

    # Effect 2
    m2 = Matrix(seed=42, density=1.0)
    clip2 = m2.apply(clip)
    frame2 = clip2.get_frame(0)

    assert np.any(frame1 > 0), "Frame should have some content"
    assert np.array_equal(frame1, frame2), "Same seed should produce same result"

def test_matrix_seed_variance():
    """Verify that two matrix effects with different seeds produce different results."""
    # Use density=1.0 to ensure rain is visible
    clip = ColorClip(size=(100, 100), color=(0, 0, 0), duration=1)

    # Effect 1
    m1 = Matrix(seed=42, density=1.0)
    clip1 = m1.apply(clip)
    frame1 = clip1.get_frame(0)

    # Effect 2
    m2 = Matrix(seed=123, density=1.0)
    clip2 = m2.apply(clip)
    frame2 = clip2.get_frame(0)

    assert np.any(frame1 > 0), "Frame 1 should have some content"
    assert np.any(frame2 > 0), "Frame 2 should have some content"
    assert not np.array_equal(frame1, frame2), "Different seeds should produce different results"

def test_global_seed_preservation():
    """Verify that global random state is not modified."""

    clip = ColorClip(size=(100, 100), color=(0, 0, 0), duration=1)
    m = Matrix(seed=42)

    np.random.seed(555)
    r1 = np.random.random()
    r2 = np.random.random()

    np.random.seed(555)
    r1_dup = np.random.random()

    m.apply(clip).get_frame(0)

    r2_dup = np.random.random()

    assert r1 == r1_dup
    assert r2 == r2_dup, "Global random state was modified!"
