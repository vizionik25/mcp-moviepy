import os
import pytest
from mcp_moviepy.tools.video_generation import create_image_clip
from PIL import Image

def test_create_image_clip_success(tmp_path):
    # Create a dummy image
    img_path = str(tmp_path / "test_image.png")
    img = Image.new("RGB", (100, 100), color="red")
    img.save(img_path)
    
    duration = 1.5
    
    # Run the tool
    result_path = create_image_clip(img_path=img_path, duration=duration)
    
    # Verify the result
    assert os.path.exists(result_path)
    assert result_path.endswith(".mp4")
    
    # Cleanup
    if os.path.exists(result_path):
        os.remove(result_path)

def test_create_image_clip_nonexistent_file():
    with pytest.raises(ValueError, match="Image file does not exist"):
        create_image_clip(img_path="nonexistent.png", duration=1.0)

def test_create_image_clip_invalid_duration():
    with pytest.raises(ValueError, match="duration must be positive"):
        create_image_clip(img_path="some_image.png", duration=-1.0)
