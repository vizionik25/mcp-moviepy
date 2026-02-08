import pytest
from unittest.mock import MagicMock
# Note: Dependencies like moviepy, fastmcp, etc., are mocked in tests/conftest.py
# before this module is imported.
from main import get_clip, CLIPS

@pytest.fixture(autouse=True)
def clear_clips_fixture():
    """
    Ensure CLIPS is empty before and after each test.
    This fixture ensures local isolation for tests in this file.
    """
    CLIPS.clear()
    yield
    CLIPS.clear()

def test_get_clip_success():
    """
    Verify that get_clip retrieves an existing clip correctly.
    """
    # Create a mock clip
    mock_clip = MagicMock()
    clip_id = "test-clip-1"

    # Store it directly in CLIPS
    CLIPS[clip_id] = mock_clip

    # Retrieve it using get_clip
    retrieved_clip = get_clip(clip_id)

    # Assert it is the same object
    assert retrieved_clip is mock_clip

def test_get_clip_failure_missing():
    """
    Verify that get_clip raises ValueError when the clip ID does not exist.
    """
    clip_id = "non-existent-id"

    # Ensure it's not in CLIPS (though clear_clips_fixture handles this)
    if clip_id in CLIPS:
        del CLIPS[clip_id]

    with pytest.raises(ValueError) as excinfo:
        get_clip(clip_id)

    assert f"Clip with ID {clip_id} not found." in str(excinfo.value)

def test_get_clip_failure_empty():
    """
    Verify that get_clip raises ValueError when CLIPS is empty.
    """
    # CLIPS should be cleared by fixture, but we can double check
    CLIPS.clear()

    clip_id = "any-id"

    with pytest.raises(ValueError) as excinfo:
        get_clip(clip_id)

    assert f"Clip with ID {clip_id} not found." in str(excinfo.value)

def test_get_clip_invalid_type():
    """
    Verify behavior when passing an invalid type (e.g. None).
    Although type hint says str, at runtime it might be anything.
    """
    clip_id = None

    # None is not in CLIPS
    with pytest.raises(ValueError) as excinfo:
        get_clip(clip_id)

    assert f"Clip with ID {clip_id} not found." in str(excinfo.value)
