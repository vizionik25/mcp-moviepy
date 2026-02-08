import sys
from unittest.mock import MagicMock
import pytest

# Mock dependencies before importing main
mock_modules = [
    "fastmcp",
    "moviepy",
    "moviepy.video.tools.drawing",
    "moviepy.video.tools.cuts",
    "moviepy.video.io.ffmpeg_tools",
    "moviepy.video.tools.subtitles",
    "moviepy.video.tools.credits",
    "mcp_ui_server",
    "ui",
    "custom_fx",
    "numpy",
    "numexpr",
    "pydantic"
]

for module_name in mock_modules:
    sys.modules[module_name] = MagicMock()

import main
from main import get_clip

@pytest.fixture(autouse=True)
def clear_clips():
    """Ensure CLIPS is empty before and after each test."""
    main.CLIPS.clear()
    yield
    main.CLIPS.clear()

def test_get_clip_success():
    """Verify that a clip is correctly retrieved from CLIPS."""
    mock_clip = MagicMock()
    clip_id = "test-clip-id"
    main.CLIPS[clip_id] = mock_clip

    retrieved_clip = get_clip(clip_id)
    assert retrieved_clip == mock_clip

def test_get_clip_not_found():
    """Verify that ValueError is raised when clip ID is not found."""
    clip_id = "non-existent-id"
    with pytest.raises(ValueError) as excinfo:
        get_clip(clip_id)

    assert f"Clip with ID {clip_id} not found." in str(excinfo.value)

def test_get_clip_empty_clips():
    """Verify that ValueError is raised when CLIPS is empty."""
    main.CLIPS.clear()
    clip_id = "any-id"
    with pytest.raises(ValueError) as excinfo:
        get_clip(clip_id)

    assert f"Clip with ID {clip_id} not found." in str(excinfo.value)
