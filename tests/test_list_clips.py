import pytest
import main
from unittest.mock import MagicMock

# Rely on tests/conftest.py for mocking dependencies (moviepy, fastmcp, numpy, etc.)

@pytest.fixture(autouse=True)
def clear_clips():
    """Ensure CLIPS is empty before and after each test."""
    main.CLIPS.clear()
    yield
    main.CLIPS.clear()

def test_list_clips_empty():
    """Verify that list_clips returns an empty dictionary when no clips are registered."""
    result = main.list_clips.fn()
    assert result == {}
    assert isinstance(result, dict)

def test_list_clips_populated():
    """Verify that list_clips returns a dictionary with correct IDs and types."""
    # Create mock clip
    clip1 = MagicMock()

    # Manually populate CLIPS as per task rationale
    id1 = "test-id-1"
    main.CLIPS[id1] = clip1

    result = main.list_clips.fn()

    assert len(result) == 1
    assert id1 in result
    assert isinstance(result[id1], str)
    # The string representation depends on the mock object's type.

def test_list_clips_multiple_clips():
    """Verify list_clips with multiple manually registered clips."""
    c1 = MagicMock()
    c2 = MagicMock()

    id1 = "id-1"
    id2 = "id-2"

    main.CLIPS[id1] = c1
    main.CLIPS[id2] = c2

    result = main.list_clips.fn()

    assert len(result) == 2
    assert id1 in result
    assert id2 in result
    assert isinstance(result[id1], str)
    assert isinstance(result[id2], str)

def test_list_clips_type_string():
    """Verify the string representation of the clip type."""
    # We can control the type by creating a class
    class MyClip:
        pass

    c = MyClip()
    id1 = "type-test-id"
    main.CLIPS[id1] = c

    result = main.list_clips.fn()

    assert id1 in result
    assert "MyClip" in result[id1]
