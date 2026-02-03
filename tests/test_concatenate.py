import os
import pytest
from mcp_moviepy.tools.video_generation import concatenate_videoclips, create_color_clip

def test_concatenate_videoclips_success():
    # Create two small clips
    clip1_path = create_color_clip((100, 100), "red", 1.0)
    clip2_path = create_color_clip((100, 100), "blue", 1.0)
    
    # Run the tool
    result_path = concatenate_videoclips(clip_paths=[clip1_path, clip2_path])
    
    # Verify the result
    assert os.path.exists(result_path)
    assert result_path.endswith(".mp4")
    
    # Cleanup
    for p in [clip1_path, clip2_path, result_path]:
        if os.path.exists(p):
            os.remove(p)

def test_concatenate_videoclips_invalid_paths():
    with pytest.raises(ValueError, match="All clip paths must exist"):
        concatenate_videoclips(clip_paths=["nonexistent.mp4"])

def test_concatenate_videoclips_empty_list():
    with pytest.raises(ValueError, match="clip_paths cannot be empty"):
        concatenate_videoclips(clip_paths=[])
