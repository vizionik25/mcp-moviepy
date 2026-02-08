import os
import pytest
from unittest.mock import patch, MagicMock
import sys

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
    "numexpr",
    "pydantic",
    "numpy"
]

for module_name in mock_modules:
    sys.modules[module_name] = MagicMock()

import main
from main import validate_path

def test_validate_path_valid_cwd():
    """Test that a file in the current working directory is valid."""
    filename = "test_file.txt"
    assert validate_path(filename) == filename

def test_validate_path_valid_subdir():
    """Test that a file in a subdirectory is valid."""
    filename = "subdir/test_file.txt"
    assert validate_path(filename) == filename

def test_validate_path_valid_tmp():
    """Test that a file in /tmp is valid."""
    filename = "/tmp/test_file.txt"
    assert validate_path(filename) == filename

def test_validate_path_valid_empty_is_cwd():
    """Test that empty string resolves to CWD and is valid."""
    assert validate_path("") == ""

def test_validate_path_valid_dot_is_cwd():
    """Test that '.' resolves to CWD and is valid."""
    assert validate_path(".") == "."

def test_validate_path_invalid_parent():
    """Test that accessing parent directory raises ValueError."""
    filename = "../secret.txt"
    with pytest.raises(ValueError, match="Access denied to path"):
        validate_path(filename)

def test_validate_path_invalid_absolute():
    """Test that accessing an absolute path outside allowed dirs raises ValueError."""
    filename = "/etc/passwd"
    with pytest.raises(ValueError, match="Access denied to path"):
        validate_path(filename)

def test_validate_path_traversal_trick():
    """Test a tricky traversal path."""
    filename = "subdir/../../etc/passwd"
    with pytest.raises(ValueError, match="Access denied to path"):
        validate_path(filename)

def test_validate_path_traversal_in_tmp():
    """Test traversal out of /tmp."""
    filename = "/tmp/../etc/passwd"
    with pytest.raises(ValueError, match="Access denied to path"):
        validate_path(filename)

def test_validate_path_sibling_directory():
    """Test that a path in a sibling directory with a common prefix is invalid."""
    cwd = os.getcwd()
    # Construct a path that starts with CWD but is a sibling directory
    # e.g. /app -> /app_suffix
    sibling_dir = cwd + "_suffix"
    filename = os.path.join(sibling_dir, "secret.txt")
    with pytest.raises(ValueError, match="Access denied to path"):
        validate_path(filename)

def test_validate_path_symlink_traversal():
    """Test that a symlink pointing outside allowed dirs is detected."""
    # Create a symlink in CWD that points to /etc/passwd
    symlink_path = "link_to_passwd"
    if os.path.exists(symlink_path):
        os.remove(symlink_path)
    try:
        os.symlink("/etc/passwd", symlink_path)
        # Should raise ValueError because it resolves to /etc/passwd which is outside CWD
        with pytest.raises(ValueError, match="Access denied to path"):
            validate_path(symlink_path)
    finally:
        if os.path.exists(symlink_path):
            os.remove(symlink_path)
