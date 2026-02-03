import os
import pytest
from mcp_moviepy.tools.video_generation import create_text_clip

def test_create_text_clip_success():
    text = "Hello MoviePy"
    duration = 2.0
    
    # Run the tool
    result_path = create_text_clip(text=text, duration=duration)
    
    # Verify the result
    assert os.path.exists(result_path)
    assert result_path.endswith(".mp4")
    
    # Cleanup
    if os.path.exists(result_path):
        os.remove(result_path)

def test_create_text_clip_with_options():
    text = "Styled Text"
    duration = 1.0
    result_path = create_text_clip(
        text=text, 
        duration=duration,
        font_size=70,
        color="yellow",
        bg_color="blue"
    )
    assert os.path.exists(result_path)
    if os.path.exists(result_path):
        os.remove(result_path)

def test_create_text_clip_invalid_duration():
    with pytest.raises(ValueError):
        create_text_clip(text="Test", duration=-1.0)
