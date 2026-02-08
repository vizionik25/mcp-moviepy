import sys
from unittest.mock import MagicMock
import pytest

# Improved Mock for FastMCP
class MockFastMCP:
    def __init__(self, name=None):
        self.name = name

    def tool(self, func=None, **kwargs):
        # If used as @mcp.tool
        if func and callable(func):
            func.fn = func
            return func
        # If used as @mcp.tool() - not used in main.py but good for completeness
        def wrapper(f):
            f.fn = f
            return f
        return wrapper

    def prompt(self, func=None, **kwargs):
        if func and callable(func):
            func.fn = func
            return func
        def wrapper(f):
            f.fn = f
            return f
        return wrapper

    def run(self, *args, **kwargs):
        pass

# Create the mock module
mock_fastmcp_module = MagicMock()
mock_fastmcp_module.FastMCP = MockFastMCP
sys.modules["fastmcp"] = mock_fastmcp_module

# Mock other dependencies
mock_modules = [
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

# Import the module under test
import main
from main import list_clips

@pytest.fixture(autouse=True)
def clear_clips():
    """Ensure CLIPS is empty before and after each test."""
    main.CLIPS.clear()
    yield
    main.CLIPS.clear()

def test_list_clips_empty():
    """Verify that list_clips returns an empty dictionary when no clips are registered."""
    # Since we mocked the decorator to set .fn, we can call it.
    # However, if the decorator returns the function itself, we can call it directly too.
    # main.py usage: @mcp.tool def list_clips...
    # with our mock: list_clips is the function itself, and it has .fn pointing to itself.

    result = list_clips.fn()
    assert result == {}
    assert isinstance(result, dict)

def test_list_clips_populated():
    """Verify that list_clips returns a dictionary with correct IDs and types."""
    # Create mock clips
    clip1 = MagicMock()
    # We want type(clip1) to be something predictable, but MagicMock's type is tricky to mock directly in this context
    # without deeper python magic. However, list_clips calls str(type(c)).
    # Let's just verify that we get *some* string representation of the type.

    clip2 = MagicMock()

    # Manually populate CLIPS
    id1 = "clip-1"
    id2 = "clip-2"
    main.CLIPS[id1] = clip1
    main.CLIPS[id2] = clip2

    result = list_clips.fn()

    assert len(result) == 2
    assert id1 in result
    assert id2 in result

    # Verify the value is a string representation of a type
    assert "unittest.mock.MagicMock" in result[id1]
    assert "unittest.mock.MagicMock" in result[id2]

def test_list_clips_structure():
    """Verify the structure of the returned dictionary items."""
    clip = MagicMock()
    cid = "test-clip"
    main.CLIPS[cid] = clip

    result = list_clips.fn()

    assert cid in result
    assert isinstance(result[cid], str)
    assert str(type(clip)) == result[cid]
