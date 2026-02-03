import os
from moviepy.video.VideoClip import ColorClip, TextClip, ImageClip
from moviepy.video.compositing.CompositeVideoClip import concatenate_videoclips as moviepy_concatenate
from moviepy.video.io.VideoFileClip import VideoFileClip
from PIL import ImageColor
from mcp_moviepy.utils.doc_validation import ensure_doc_reference
from mcp_moviepy.utils.file_utils import get_temp_file_path

@ensure_doc_reference
def create_color_clip(size: tuple[int, int], color: str, duration: float) -> str:
    """
    Generates a solid color video clip.
    
    Ref: html/reference/reference/moviepy.video.VideoClip.ColorClip.html
    
    Args:
        size (tuple): Width and height of the clip in pixels (e.g., (640, 480)).
        color (str): Color of the clip (e.g., 'red', '#FF0000').
        duration (float): Duration of the clip in seconds.
        
    Returns:
        str: Absolute path to the generated MP4 file.
    """
    if not isinstance(size, (tuple, list)) or len(size) != 2:
        raise ValueError("size must be a tuple of (width, height)")
    
    if duration <= 0:
        raise ValueError("duration must be positive")
        
    # MoviePy 2.x ColorClip requires RGB tuple, not string
    try:
        rgb_color = ImageColor.getrgb(color)
    except ValueError:
        raise ValueError(f"Invalid color: {color}")
        
    output_path = get_temp_file_path("color_clip", "mp4")
    
    clip = ColorClip(size=size, color=rgb_color, duration=duration)
    # We need to set fps for the clip to be writeable to file
    clip.fps = 24
    clip.write_videofile(output_path, logger=None)
    clip.close()
    
    return os.path.abspath(output_path)

@ensure_doc_reference
def create_text_clip(
    text: str, 
    duration: float,
    font: str = None,
    font_size: int = 50,
    color: str = "black",
    bg_color: str = None,
    size: tuple[int | None, int | None] = (None, None),
    method: str = "label",
    text_align: str = "left",
    horizontal_align: str = "center",
    vertical_align: str = "center"
) -> str:
    """
    Generates a video clip from a text string.
    
    Ref: html/reference/reference/moviepy.video.VideoClip.TextClip.html
    
    Args:
        text (str): The text to display.
        duration (float): Duration of the clip in seconds.
        font (str, optional): Path to the font to use. Must be an OpenType font.
        font_size (int, optional): Font size in point.
        color (str, optional): Color of the text. Default to "black".
        bg_color (str, optional): Color of the background. Default to None.
        size (tuple, optional): Size of the picture in pixels (width, height).
        method (str, optional): 'label' (default) or 'caption'.
        text_align (str, optional): center | left | right.
        horizontal_align (str, optional): center | left | right.
        vertical_align (str, optional): center | top | bottom.
        
    Returns:
        str: Absolute path to the generated MP4 file.
    """
    if duration <= 0:
        raise ValueError("duration must be positive")
        
    output_path = get_temp_file_path("text_clip", "mp4")
    
    clip = TextClip(
        text=text,
        duration=duration,
        font=font,
        font_size=font_size,
        color=color,
        bg_color=bg_color,
        size=size,
        method=method,
        text_align=text_align,
        horizontal_align=horizontal_align,
        vertical_align=vertical_align
    )
    
    clip.fps = 24
    clip.write_videofile(output_path, logger=None)
    clip.close()
    
    return os.path.abspath(output_path)

@ensure_doc_reference
def create_image_clip(img_path: str, duration: float) -> str:
    """
    Creates a video clip from a static image file.
    
    Ref: html/reference/reference/moviepy.video.VideoClip.ImageClip.html
    
    Args:
        img_path (str): Path to the image file.
        duration (float): Duration of the clip in seconds.
        
    Returns:
        str: Absolute path to the generated MP4 file.
    """
    if duration <= 0:
        raise ValueError("duration must be positive")
        
    if not os.path.exists(img_path):
        raise ValueError("Image file does not exist")
        
    output_path = get_temp_file_path("image_clip", "mp4")
    
    clip = ImageClip(img=img_path, duration=duration)
    clip.fps = 24
    clip.write_videofile(output_path, logger=None)
    clip.close()
    
    return os.path.abspath(output_path)

@ensure_doc_reference
def concatenate_videoclips(clip_paths: list[str], method: str = "compose") -> str:
    """
    Joins multiple video clips into a single sequence.
    
    Ref: html/reference/reference/moviepy.video.compositing.CompositeVideoClip.concatenate_videoclips.html
    
    Args:
        clip_paths (list[str]): List of paths to video files to concatenate.
        method (str, optional): 'chain' or 'compose'. Default to 'compose'.
        
    Returns:
        str: Absolute path to the generated MP4 file.
    """
    if not clip_paths:
        raise ValueError("clip_paths cannot be empty")
        
    for p in clip_paths:
        if not os.path.exists(p):
            raise ValueError(f"All clip paths must exist. Missing: {p}")
            
    clips = [VideoFileClip(p) for p in clip_paths]
    
    try:
        final_clip = moviepy_concatenate(clips, method=method)
        output_path = get_temp_file_path("concatenated", "mp4")
        final_clip.write_videofile(output_path, logger=None)
        return os.path.abspath(output_path)
    finally:
        for clip in clips:
            clip.close()