import sys
from unittest.mock import MagicMock, patch
import uuid
import pytest

# Import the module under test
import main
from main import register_clip

@pytest.fixture(autouse=True)
def clear_clips():
    """Ensure CLIPS is empty before and after each test."""
    main.CLIPS.clear()
    yield
    main.CLIPS.clear()

def test_register_clip_success():
    """Verify that a clip is correctly added to CLIPS and returns a valid ID."""
    mock_clip = MagicMock()
    clip_id = register_clip(mock_clip)

    assert clip_id in main.CLIPS
    assert main.CLIPS[clip_id] == mock_clip
    assert isinstance(clip_id, str)

def test_register_clip_uuid_format():
    """Verify that the returned ID is a valid UUID4 string."""
    mock_clip = MagicMock()
    clip_id = register_clip(mock_clip)

    # This will raise ValueError if not a valid UUID
    val = uuid.UUID(clip_id, version=4)
    assert str(val) == clip_id

def test_register_clip_max_limit():
    """Verify that RuntimeError is raised when MAX_CLIPS is reached."""
    # Temporarily set MAX_CLIPS to a small value for testing
    original_max = main.MAX_CLIPS
    main.MAX_CLIPS = 3
    try:
        register_clip(MagicMock())
        register_clip(MagicMock())
        register_clip(MagicMock())

        with pytest.raises(RuntimeError) as excinfo:
            register_clip(MagicMock())

        assert "Maximum number of clips" in str(excinfo.value)
        assert str(main.MAX_CLIPS) in str(excinfo.value)
    finally:
        main.MAX_CLIPS = original_max

@patch("uuid.uuid4")
def test_register_clip_mock_uuid(mock_uuid4):
    """Verify that uuid.uuid4 is used to generate the clip ID."""
    fixed_uuid = uuid.UUID('12345678-1234-5678-1234-567812345678')
    mock_uuid4.return_value = fixed_uuid

    mock_clip = MagicMock()
    clip_id = register_clip(mock_clip)

    assert clip_id == str(fixed_uuid)
    assert main.CLIPS[clip_id] == mock_clip
    mock_uuid4.assert_called_once()
