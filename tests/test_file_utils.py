import os
import pytest
from mcp_moviepy.utils.file_utils import get_temp_file_path, cleanup_temp_file

def test_get_temp_file_path():
    path = get_temp_file_path("test_video", "mp4")
    assert path.endswith(".mp4")
    assert "test_video" in path
    assert os.path.isabs(path)

def test_cleanup_temp_file():
    # Create a dummy file
    path = get_temp_file_path("cleanup_test", "txt")
    with open(path, "w") as f:
        f.write("test")
    
    assert os.path.exists(path)
    
    cleanup_temp_file(path)
    
    assert not os.path.exists(path)

def test_cleanup_nonexistent_file():
    # Should not raise exception
    cleanup_temp_file("/tmp/nonexistent_file_12345.txt")
