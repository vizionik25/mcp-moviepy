import os
import pytest
from mcp_moviepy.tools.video_generation import create_color_clip

def test_create_color_clip_success():
    size = (640, 480)
    color = "red"
    duration = 2.0
    
    # Run the tool
    result_path = create_color_clip(size, color, duration)
    
    # Verify the result
    assert os.path.exists(result_path)
    assert result_path.endswith(".mp4")
    
    # Cleanup
    if os.path.exists(result_path):
        os.remove(result_path)

def test_create_color_clip_invalid_size():
    with pytest.raises(ValueError):
        create_color_clip("invalid", "red", 2.0)

def test_create_color_clip_invalid_duration():
    with pytest.raises(ValueError):
        create_color_clip((640, 480), "red", -1.0)
