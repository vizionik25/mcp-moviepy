import sys
from unittest.mock import MagicMock

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

# Configure FastMCP mock to act as a transparent decorator so we can test the function logic
sys.modules["fastmcp"].FastMCP.return_value.tool.side_effect = lambda func: func

import pytest
from main import delete_clip, CLIPS

@pytest.fixture(autouse=True)
def clear_clips():
    """Ensure CLIPS is empty before and after each test."""
    CLIPS.clear()
    yield
    CLIPS.clear()

def test_delete_clip_success():
    """Verify that a clip is correctly removed and closed."""
    clip_id = "test_clip_id"
    mock_clip = MagicMock()
    CLIPS[clip_id] = mock_clip

    result = delete_clip(clip_id)

    assert result == f"Clip {clip_id} deleted."
    assert clip_id not in CLIPS
    mock_clip.close.assert_called_once()

def test_delete_clip_not_found():
    """Verify behavior when trying to delete a non-existent clip."""
    clip_id = "non_existent_id"
    result = delete_clip(clip_id)
    assert result == f"Clip {clip_id} not found."

def test_delete_clip_close_exception():
    """Verify that deletion succeeds even if clip.close() raises an exception."""
    clip_id = "test_clip_id"
    mock_clip = MagicMock()
    # Simulate an exception during close
    mock_clip.close.side_effect = Exception("Close error")
    CLIPS[clip_id] = mock_clip

    result = delete_clip(clip_id)

    assert result == f"Clip {clip_id} deleted."
    assert clip_id not in CLIPS
    # Ensure close was attempted despite the exception
    mock_clip.close.assert_called_once()
