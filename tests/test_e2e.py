import sys
from unittest.mock import MagicMock, patch
import os
import pytest
import shutil
import types
import importlib

# Define MockClip (needed by test_max_clips and potentially other tests)
class MockClip(MagicMock):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.duration = kwargs.get('duration', 1.0)
        self.close = MagicMock()
        self.write_videofile = MagicMock()
        self.write_audiofile = MagicMock()
        self.with_position = MagicMock(return_value=self)
        self.with_start = MagicMock(return_value=self)
        self.with_end = MagicMock(return_value=self)
        self.with_duration = MagicMock(return_value=self)
        self.with_mask = MagicMock(return_value=self)
        self.with_audio = MagicMock(return_value=self)
        self.with_effects = MagicMock(return_value=self)
        self.subclipped = MagicMock(return_value=self)
        self.fps = 24
        self.h = 100
        self.w = 100
        self.size = (100, 100)

# Create a mock module for moviepy that allows "from moviepy import *"
mock_moviepy = types.ModuleType("moviepy")
mock_moviepy.VideoFileClip = MockClip
mock_moviepy.ImageClip = MockClip
mock_moviepy.ImageSequenceClip = MockClip
mock_moviepy.TextClip = MockClip
mock_moviepy.ColorClip = MockClip
mock_moviepy.AudioFileClip = MockClip
mock_moviepy.CompositeVideoClip = MockClip
mock_moviepy.clips_array = MagicMock(return_value=MockClip())
mock_moviepy.concatenate_videoclips = MagicMock(return_value=MockClip())
mock_moviepy.CompositeAudioClip = MockClip
mock_moviepy.concatenate_audioclips = MagicMock(return_value=MockClip())
mock_moviepy.vfx = MagicMock()
mock_moviepy.afx = MagicMock()
mock_moviepy.Effect = MagicMock

# Overwrite moviepy
sys.modules["moviepy"] = mock_moviepy

# Create mock for custom_fx
mock_custom_fx = types.ModuleType("custom_fx")
mock_custom_fx.RGBSync = MagicMock()
mock_custom_fx.Kaleidoscope = MagicMock()
mock_custom_fx.Matrix = MagicMock()
mock_custom_fx.AutoFraming = MagicMock()
mock_custom_fx.CloneGrid = MagicMock()
mock_custom_fx.RotatingCube = MagicMock()
mock_custom_fx.KaleidoscopeCube = MagicMock()
mock_custom_fx.QuadMirror = MagicMock()
mock_custom_fx.ChromaKey = MagicMock()

sys.modules["custom_fx"] = mock_custom_fx

# Mock other modules but NOT numpy etc (use conftest mocks)
mock_modules = [
    # "fastmcp", # Use conftest
    "moviepy.video.tools.drawing",
    "moviepy.video.tools.cuts",
    "moviepy.video.io.ffmpeg_tools",
    "moviepy.video.tools.subtitles",
    "moviepy.video.tools.credits",
    "mcp_ui_server",
    "ui",
    # "custom_fx", # Handled above
    # "numpy", # Use conftest
    # "numexpr", # Use conftest
    # "pydantic", # Use conftest
    # "PIL" # Use conftest
]

for module_name in mock_modules:
    sys.modules[module_name] = MagicMock()

import main
importlib.reload(main)
from main import *

# Re-assign mocked modules to local names if used
np = sys.modules["numpy"]
Image = sys.modules["PIL"].Image

import main
from main import (
    validate_path,
    get_clip,
    delete_clip,
    list_clips,
    video_file_clip,
    image_clip,
    image_sequence_clip,
    text_clip,
    color_clip,
    credits_clip,
    subtitles_clip,
    write_videofile,
    tools_ffmpeg_extract_subclip,
    write_gif,
    audio_file_clip,
    write_audiofile,
    set_position,
    set_audio,
    set_mask,
    set_start,
    set_end,
    set_duration,
    subclip,
    composite_video_clips,
    tools_clips_array,
    concatenate_video_clips,
    vfx_accel_decel,
    vfx_black_white,
    vfx_blink,
    vfx_crop,
    vfx_cross_fade_in,
    vfx_cross_fade_out,
    vfx_fade_in,
    vfx_fade_out,
    vfx_gamma_correction,
    vfx_head_blur,
    vfx_invert_colors,
    vfx_multiply_color,
    vfx_resize,
    vfx_rotate,
    vfx_rgb_sync,
    tools_detect_scenes,
    tools_find_video_period,
    tools_drawing_color_gradient,
    tools_drawing_color_split,
    tools_file_to_subtitles,
    tools_find_audio_period,
    CLIPS
)

@pytest.fixture(autouse=True)
def cleanup():
    CLIPS.clear()
    yield
    CLIPS.clear()
    for f in ["temp.mp4", "temp.wav", "test.png", "credits.txt", "sub.srt", "test.gif", "temp2.mp4"]:
        if os.path.exists(f):
            try: os.remove(f)
            except: pass
    if os.path.exists("test_img_dir"): shutil.rmtree("test_img_dir")

def test_system():
    validate_path("test.mp4")
    validate_path("/tmp/test.mp4")
    cid = color_clip.fn([10,10], [0,0,0], duration=1)
    get_clip(cid)
    with pytest.raises(ValueError): get_clip("missing")
    delete_clip.fn(cid)
    with pytest.raises(ValueError): get_clip(cid)
    cid = color_clip.fn([1,1], [0,0,0])
    CLIPS[cid].close.side_effect = Exception()
    delete_clip.fn(cid)
    delete_clip.fn("missing")
    list_clips.fn()

def test_io():
    Image.fromarray.return_value.save = MagicMock()
    with open("test.png", "w") as f: f.write("")
    image_clip.fn("test.png", duration=0.5)
    with pytest.raises(FileNotFoundError): image_clip.fn("missing.png")
    with pytest.raises(ValueError): color_clip.fn([10,10], [0,0,0], duration=-1)
    image_sequence_clip.fn(["test.png"], fps=5)
    os.makedirs("test_img_dir", exist_ok=True)
    with open("test_img_dir/1.png", "w") as f: f.write("")
    image_sequence_clip.fn(["test_img_dir"], fps=5)
    with pytest.raises(ValueError): image_sequence_clip.fn([], fps=5)
    vid = color_clip.fn([10,10], [0,0,0], duration=0.5)
    with open("temp.mp4", "w") as f: f.write("")
    write_videofile.fn(vid, "temp.mp4", fps=5)
    video_file_clip.fn("temp.mp4")
    video_file_clip.fn("temp.mp4", target_resolution=[5,5])
    with pytest.raises(FileNotFoundError): video_file_clip.fn("missing.mp4")
    tools_ffmpeg_extract_subclip.fn("temp.mp4", 0, 0.1, "temp2.mp4")
    with pytest.raises(ValueError): tools_ffmpeg_extract_subclip.fn("temp.mp4", 0.5, 0.1, "temp2.mp4")
    write_gif.fn(vid, "test.gif", fps=5)

def test_audio_io():
    with open("temp.wav", "w") as f: f.write("")
    aid = audio_file_clip.fn("temp.wav")
    with pytest.raises(FileNotFoundError): audio_file_clip.fn("missing.wav")
    write_audiofile.fn(aid, "temp.mp3")

@patch("main.CreditsClip")
@patch("main.SubtitlesClip")
def test_special_clips(ms, mc):
    text_clip.fn("hi")
    with pytest.raises(ValueError): text_clip.fn("hi", duration=0)
    sys.modules["moviepy.video.tools.credits"].CreditsClip.return_value = MockClip()
    with open("credits.txt", "w") as f: f.write("A")
    credits_clip.fn("credits.txt", width=100)
    with pytest.raises(ValueError): credits_clip.fn("credits.txt", width=0)
    with pytest.raises(FileNotFoundError): credits_clip.fn("missing.txt", 100)
    sys.modules["moviepy.video.tools.subtitles"].SubtitlesClip.return_value = MockClip()
    sys.modules["moviepy.video.tools.subtitles"].file_to_subtitles.return_value = []
    with open("sub.srt", "w") as f: f.write("1\n00:00:00,000 --> 00:00:01,000\nX")
    subtitles_clip.fn("sub.srt")
    with pytest.raises(FileNotFoundError): subtitles_clip.fn("missing.srt")
    tools_file_to_subtitles.fn("sub.srt")

def test_vfx_config():
    cid = color_clip.fn([10,10], [0,0,0], duration=1)
    set_position.fn(cid, pos_str="center")
    set_position.fn(cid, x=1)
    set_position.fn(cid, y=1)
    set_position.fn(cid, x=1, y=1)
    set_position.fn(cid, x=1, y=1, relative=True)
    with pytest.raises(ValueError): set_position.fn(cid)
    set_start.fn(cid, 0.1)
    set_end.fn(cid, 0.9)
    set_duration.fn(cid, 0.5)
    set_mask.fn(cid, cid)
    set_audio.fn(cid, cid)
    concatenate_video_clips.fn([cid])
    with pytest.raises(ValueError): concatenate_video_clips.fn([])
    composite_video_clips.fn([cid])
    with pytest.raises(ValueError): composite_video_clips.fn([])
    tools_clips_array.fn([[cid]])
    with pytest.raises(ValueError): tools_clips_array.fn([])
    subclip.fn(cid, 0.1, 0.5)
    with pytest.raises(ValueError): subclip.fn(cid, 0.5, 0.1)

def test_vfx_hit():
    cid = color_clip.fn([10,10], [0,0,0], duration=1)
    vfx_accel_decel.fn(cid, new_duration=2)
    vfx_black_white.fn(cid)
    vfx_blink.fn(cid, 0.1, 0.1)
    vfx_crop.fn(cid, x1=0, y1=0, x2=5, y2=5)
    vfx_cross_fade_in.fn(cid, 0.1)
    vfx_cross_fade_out.fn(cid, 0.1)
    vfx_fade_in.fn(cid, 0.1)
    vfx_fade_out.fn(cid, 0.1)
    vfx_gamma_correction.fn(cid, 1.1)
    vfx_invert_colors.fn(cid)
    vfx_multiply_color.fn(cid, 0.5)
    vfx_rgb_sync.fn(cid)
    vfx_resize.fn(cid, width=5)
    vfx_resize.fn(cid, height=5)
    vfx_resize.fn(cid, scale=0.5)
    with pytest.raises(ValueError): vfx_resize.fn(cid)
    vfx_head_blur.fn(cid, "t", "t", 2)
    vfx_rotate.fn(cid, 45)
    for name, tool in main.__dict__.items():
        if name.startswith("vfx_") and hasattr(tool, 'fn'):
            try:
                if name in ["vfx_masks_and", "vfx_masks_or"]: tool.fn(cid, cid)
                elif name == "vfx_freeze_region": tool.fn(cid, 0.1, region=[0,0,5,5])
                else: tool.fn(cid)
            except: pass

def test_afx_hit():
    cid = color_clip.fn([10,10], [0,0,0], duration=1)
    for name, tool in main.__dict__.items():
        if name.startswith("afx_") and hasattr(tool, 'fn'):
            try:
                if "fade" in name: tool.fn(cid, 0.1)
                elif "loop" in name: tool.fn(cid, 2)
                elif "stereo" in name: tool.fn(cid, 0.5, 0.5)
                elif "volume" in name: tool.fn(cid, 0.5)
                else: tool.fn(cid)
            except: pass

def test_tools_hit():
    vid = color_clip.fn([10,10], [0,0,0], duration=1)

    # We must patch the function where it is USED in main (because it was imported via from ... import ...)
    # But wait, main.py imports it as:
    # from moviepy.video.tools.cuts import detect_scenes, find_video_period
    # So main.detect_scenes IS the object that was in the mock module AT IMPORT TIME.

    # We need to access that specific mock object and set its return value.
    # We can get it from main.
    main.detect_scenes.return_value = ([], [])
    main.find_video_period.return_value = 1.0

    tools_detect_scenes.fn(vid)
    tools_find_video_period.fn(vid)

    # find_audio_period is imported at top level
    with patch('main.find_audio_period') as mock_find:
        mock_find.return_value = 1.0
        tools_find_audio_period.fn(vid)

    tools_drawing_color_gradient.fn([10,10], [0,0], [10,10], [0,0,0], [255,255,255])
    tools_drawing_color_split.fn([10,10], 5, 5, [0,0], [10,10], [0,0,0], [255,255,255])

def test_max_clips():
    from main import MAX_CLIPS, register_clip
    CLIPS.clear()
    for _ in range(MAX_CLIPS): register_clip(MockClip())
    with pytest.raises(RuntimeError): register_clip(MockClip())

def test_prompts():
    from main import slideshow_wizard, title_card_generator
    slideshow_wizard.fn(images=["a.jpg"], duration_per_image=5, transition_duration=1.0, resolution=[1920, 1080], fps=30)
    title_card_generator.fn(text="hi", resolution=[1920, 1080])

def test_kaleidoscope_cube():
    from main import vfx_kaleidoscope_cube
    cid = color_clip.fn([100,100], [255,0,0], duration=1)

    mock_fx = sys.modules["custom_fx"].KaleidoscopeCube.return_value
    mock_fx.apply.return_value = MockClip()

    new_cid = vfx_kaleidoscope_cube.fn(
        cid,
        kaleidoscope_params={'n_slices': 12},
        cube_params={'speed_x': 90, 'speed_y': 30}
    )
    
    write_videofile.fn(new_cid, "kaleidoscope_cube.mp4", fps=30)
