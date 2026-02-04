from fastmcp import FastMCP
from moviepy import *
import os
import uuid
import numpy as np
from custom_fx import *

mcp = FastMCP("moviepy-mcp")

CLIPS = {}

def register_clip(clip):
    """Registers a clip in the global state and returns its ID."""
    clip_id = str(uuid.uuid4())
    CLIPS[clip_id] = clip
    return clip_id

def get_clip(clip_id: str):
    """Retrieves a clip by ID. Raises ValueError if not found."""
    if clip_id not in CLIPS:
        raise ValueError(f"Clip with ID {clip_id} not found.")
    return CLIPS[clip_id]

@mcp.tool
def list_clips() -> dict:
    """Lists all currently loaded clips and their types."""
    return {cid: str(type(c)) for cid, c in CLIPS.items()}

@mcp.tool
def delete_clip(clip_id: str) -> str:
    """Removes a clip from memory and closes it."""
    if clip_id in CLIPS:
        try:
            CLIPS[clip_id].close()
        except Exception:
            pass
        del CLIPS[clip_id]
        return f"Clip {clip_id} deleted."
    return f"Clip {clip_id} not found."

# --- Video IO ---

@mcp.tool
def video_file_clip(filename: str, audio: bool = True, fps_source: str = "fps", target_resolution: list[int] = None) -> str:
    """Load a video file."""
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File {filename} not found.")
    clip = VideoFileClip(
        filename=filename,
        audio=audio,
        fps_source=fps_source,
        target_resolution=tuple(target_resolution) if target_resolution else None
    )
    return register_clip(clip)

@mcp.tool
def image_clip(filename: str, duration: float = None, transparent: bool = True) -> str:
    """Load an image file."""
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File {filename} not found.")
    clip = ImageClip(img=filename, duration=duration, transparent=transparent)
    return register_clip(clip)

@mcp.tool
def image_sequence_clip(sequence: list[str], fps: float = None, durations: list[float] = None, with_mask: bool = True) -> str:
    """Create a clip from a sequence of images or a folder path."""
    if len(sequence) == 1 and os.path.isdir(sequence[0]):
        clip = ImageSequenceClip(sequence[0], fps=fps, durations=durations, with_mask=with_mask)
    else:
        clip = ImageSequenceClip(sequence, fps=fps, durations=durations, with_mask=with_mask)
    return register_clip(clip)

@mcp.tool
def text_clip(
    text: str,
    font: str = None,
    font_size: int = None,
    color: str = "black",
    bg_color: str = None,
    size: list[int] = None,
    method: str = "label",
    duration: float = None
) -> str:
    """Create a text clip."""
    clip = TextClip(
        text=text,
        font=font,
        font_size=font_size,
        color=color,
        bg_color=bg_color,
        size=tuple(size) if size else None,
        method=method,
        duration=duration
    )
    return register_clip(clip)

@mcp.tool
def color_clip(size: list[int], color: list[int], duration: float = None) -> str:
    """Create a solid color clip."""
    clip = ColorClip(size=tuple(size), color=tuple(color), duration=duration)
    return register_clip(clip)

@mcp.tool
def credits_clip(
    creditfile: str,
    width: int,
    stretch: int = 30,
    color: str = "white",
    stroke_color: str = "black",
    stroke_width: int = 2,
    font: str = "Amiri-Bold",
    font_size: int = 60
) -> str:
    """Create a scrolling credits clip from a text file."""
    if not os.path.exists(creditfile):
        raise FileNotFoundError(f"File {creditfile} not found.")
    clip = CreditsClip(
        creditfile,
        width,
        stretch=stretch,
        color=color,
        stroke_color=stroke_color,
        stroke_width=stroke_width,
        font=font,
        font_size=font_size
    )
    return register_clip(clip)

@mcp.tool
def subtitles_clip(filename: str, encoding: str = "utf-8", font: str = "Arial", font_size: int = 24, color: str = "white") -> str:
    """Create a subtitles clip from a .srt file."""
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File {filename} not found.")
    generator = lambda txt: TextClip(txt, font=font, font_size=font_size, color=color)
    clip = SubtitlesClip(filename, make_textclip=generator, encoding=encoding)
    return register_clip(clip)

@mcp.tool
def write_videofile(
    clip_id: str,
    filename: str,
    fps: float = None,
    codec: str = "libx264",
    audio_codec: str = "aac",
    bitrate: str = None,
    preset: str = "medium",
    threads: int = None,
    ffmpeg_params: list[str] = None
) -> str:
    """Write a video clip to a file."""
    clip = get_clip(clip_id)
    clip.write_videofile(
        filename=filename,
        fps=fps,
        codec=codec,
        audio_codec=audio_codec,
        bitrate=bitrate,
        preset=preset,
        threads=threads,
        ffmpeg_params=ffmpeg_params
    )
    return f"Successfully wrote video to {filename}"

@mcp.tool
def tools_ffmpeg_extract_subclip(filename: str, start_time: float, end_time: float, targetname: str = None) -> str:
    """Fast extraction of a subclip using ffmpeg (no decoding)."""
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File {filename} not found.")
    ffmpeg_extract_subclip(filename, start_time, end_time, targetname=targetname)
    return f"Extracted subclip to {targetname}"

# --- Audio IO ---

@mcp.tool
def audio_file_clip(filename: str, buffersize: int = 200000) -> str:
    """Load an audio file."""
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File {filename} not found.")
    clip = AudioFileClip(filename=filename, buffersize=buffersize)
    return register_clip(clip)

@mcp.tool
def write_audiofile(
    clip_id: str,
    filename: str,
    fps: int = 44100,
    nbytes: int = 2,
    codec: str = "libvorbis",
    bitrate: str = None
) -> str:
    """Write an audio clip to a file."""
    clip = get_clip(clip_id)
    clip.write_audiofile(
        filename=filename,
        fps=fps,
        nbytes=nbytes,
        codec=codec,
        bitrate=bitrate
    )
    return f"Successfully wrote audio to {filename}"

# --- Clip Configuration ---

@mcp.tool
def set_position(clip_id: str, x: int = None, y: int = None, pos_str: str = None, relative: bool = False) -> str:
    """Set clip position. Use x/y for pixels, or pos_str for 'center', 'left', etc."""
    clip = get_clip(clip_id)
    if pos_str:
        pos = pos_str
    elif x is not None and y is not None:
        pos = (x, y)
    elif x is not None:
        pos = (x, "center")
    elif y is not None:
        pos = ("center", y)
    else:
        raise ValueError("Provide x, y, or pos_str")
    return register_clip(clip.with_position(pos, relative=relative))

@mcp.tool
def set_audio(clip_id: str, audio_clip_id: str) -> str:
    """Set the audio of a video clip."""
    clip = get_clip(clip_id)
    audio = get_clip(audio_clip_id)
    return register_clip(clip.with_audio(audio))

@mcp.tool
def set_mask(clip_id: str, mask_clip_id: str) -> str:
    """Set the mask of a clip."""
    clip = get_clip(clip_id)
    mask = get_clip(mask_clip_id)
    return register_clip(clip.with_mask(mask))

@mcp.tool
def set_start(clip_id: str, t: float) -> str:
    """Set clip start time."""
    clip = get_clip(clip_id)
    return register_clip(clip.with_start(t))

@mcp.tool
def set_end(clip_id: str, t: float) -> str:
    """Set clip end time."""
    clip = get_clip(clip_id)
    return register_clip(clip.with_end(t))

@mcp.tool
def set_duration(clip_id: str, t: float) -> str:
    """Set clip duration."""
    clip = get_clip(clip_id)
    return register_clip(clip.with_duration(t))

# --- Transformations & Compositing ---

@mcp.tool
def subclip(clip_id: str, start_time: float = 0, end_time: float = None) -> str:
    """Cut a clip."""
    clip = get_clip(clip_id)
    new_clip = clip.subclipped(start_time, end_time)
    return register_clip(new_clip)

@mcp.tool
def composite_video_clips(clip_ids: list[str], size: list[int] = None, bg_color: list[int] = None, use_bgclip: bool = False) -> str:
    """Compose multiple clips."""
    clips = [get_clip(cid) for cid in clip_ids]
    comp_clip = CompositeVideoClip(
        clips=clips,
        size=tuple(size) if size else None,
        bg_color=tuple(bg_color) if bg_color else None,
        use_bgclip=use_bgclip
    )
    return register_clip(comp_clip)

@mcp.tool
def tools_clips_array(clip_ids_rows: list[list[str]], bg_color: list[int] = None) -> str:
    """Arrange clips in a grid (array)."""
    clips = [[get_clip(cid) for cid in row] for row in clip_ids_rows]
    comp_clip = clips_array(
        clips,
        bg_color=tuple(bg_color) if bg_color else None
    )
    return register_clip(comp_clip)

@mcp.tool
def concatenate_video_clips(clip_ids: list[str], method: str = "chain", transition: str = None) -> str:
    """Concatenate multiple clips."""
    clips = [get_clip(cid) for cid in clip_ids]
    concat_clip = concatenate_videoclips(clips, method=method, transition=transition)
    return register_clip(concat_clip)

@mcp.tool
def composite_audio_clips(clip_ids: list[str]) -> str:
    """Compose multiple audio clips."""
    clips = [get_clip(cid) for cid in clip_ids]
    comp_clip = CompositeAudioClip(clips)
    return register_clip(comp_clip)

@mcp.tool
def concatenate_audio_clips(clip_ids: list[str]) -> str:
    """Concatenate multiple audio clips."""
    clips = [get_clip(cid) for cid in clip_ids]
    concat_clip = concatenate_audioclips(clips)
    return register_clip(concat_clip)

# --- Video Effects ---

@mcp.tool
def vfx_accel_decel(clip_id: str, new_duration: float = None, abruptness: float = 1.0, soonness: float = 1.0) -> str:
    """Accelerate/Decelerate clip."""
    clip = get_clip(clip_id)
    return register_clip(clip.with_effects([vfx.AccelDecel(new_duration, abruptness, soonness)]))

@mcp.tool
def vfx_black_white(clip_id: str) -> str:
    """Convert to black and white."""
    clip = get_clip(clip_id)
    return register_clip(clip.with_effects([vfx.BlackAndWhite()]))

@mcp.tool
def vfx_blink(clip_id: str, duration_on: float, duration_off: float) -> str:
    """Make clip blink."""
    clip = get_clip(clip_id)
    return register_clip(clip.with_effects([vfx.Blink(duration_on, duration_off)]))

@mcp.tool
def vfx_crop(clip_id: str, x1: int = None, y1: int = None, x2: int = None, y2: int = None, width: int = None, height: int = None, x_center: int = None, y_center: int = None) -> str:
    """Crop clip."""
    clip = get_clip(clip_id)
    return register_clip(clip.with_effects([vfx.Crop(x1, y1, x2, y2, width, height, x_center, y_center)]))

@mcp.tool
def vfx_cross_fade_in(clip_id: str, duration: float) -> str:
    """Cross fade in."""
    clip = get_clip(clip_id)
    return register_clip(clip.with_effects([vfx.CrossFadeIn(duration)]))

@mcp.tool
def vfx_cross_fade_out(clip_id: str, duration: float) -> str:
    """Cross fade out."""
    clip = get_clip(clip_id)
    return register_clip(clip.with_effects([vfx.CrossFadeOut(duration)]))

@mcp.tool
def vfx_even_size(clip_id: str) -> str:
    """Make dimensions even."""
    clip = get_clip(clip_id)
    return register_clip(clip.with_effects([vfx.EvenSize()]))

@mcp.tool
def vfx_fade_in(clip_id: str, duration: float) -> str:
    """Fade in from black."""
    clip = get_clip(clip_id)
    return register_clip(clip.with_effects([vfx.FadeIn(duration)]))

@mcp.tool
def vfx_fade_out(clip_id: str, duration: float) -> str:
    """Fade out to black."""
    clip = get_clip(clip_id)
    return register_clip(clip.with_effects([vfx.FadeOut(duration)]))

@mcp.tool
def vfx_freeze(clip_id: str, t: float = 0, freeze_duration: float = None, total_duration: float = None, padding: float = 0) -> str:
    """Freeze a frame."""
    clip = get_clip(clip_id)
    return register_clip(clip.with_effects([vfx.Freeze(t, freeze_duration, total_duration, padding)]))

@mcp.tool
def vfx_freeze_region(clip_id: str, t: float = 0, region: list[int] = None, outside_region: list[int] = None, mask_clip_id: str = None) -> str:
    """Freeze a region."""
    clip = get_clip(clip_id)
    mask = get_clip(mask_clip_id) if mask_clip_id else None
    return register_clip(clip.with_effects([vfx.FreezeRegion(t, tuple(region) if region else None, tuple(outside_region) if outside_region else None, mask)]))

@mcp.tool
def vfx_gamma_correction(clip_id: str, gamma: float) -> str:
    """Gamma correction."""
    clip = get_clip(clip_id)
    return register_clip(clip.with_effects([vfx.GammaCorrection(gamma)]))

@mcp.tool
def vfx_head_blur(clip_id: str, fx_code: str, fy_code: str, radius: float, intensity: float = None) -> str:
    """Blur moving head (requires python code for fx/fy positions)."""
    try:
        fx = eval(fx_code, {"__builtins__": None, "t": 0}) if "lambda" in fx_code else eval(f"lambda t: {fx_code}", {"__builtins__": None})
        fy = eval(fy_code, {"__builtins__": None, "t": 0}) if "lambda" in fy_code else eval(f"lambda t: {fy_code}", {"__builtins__": None})
    except Exception as e:
        raise ValueError(f"Invalid function code: {e}")
    clip = get_clip(clip_id)
    return register_clip(clip.with_effects([vfx.HeadBlur(fx, fy, radius, intensity)]))

@mcp.tool
def vfx_invert_colors(clip_id: str) -> str:
    """Invert colors."""
    clip = get_clip(clip_id)
    return register_clip(clip.with_effects([vfx.InvertColors()]))

@mcp.tool
def vfx_loop(clip_id: str, n: int = None, duration: float = None) -> str:
    """Loop clip."""
    clip = get_clip(clip_id)
    return register_clip(clip.with_effects([vfx.Loop(n, duration)]))

@mcp.tool
def vfx_lum_contrast(clip_id: str, lum: float = 0, contrast: float = 0, contrast_threshold: float = 127) -> str:
    """Luminosity contrast."""
    clip = get_clip(clip_id)
    return register_clip(clip.with_effects([vfx.LumContrast(lum, contrast, contrast_threshold)]))

@mcp.tool
def vfx_make_loopable(clip_id: str, overlap_duration: float) -> str:
    """Make clip loopable with fade."""
    clip = get_clip(clip_id)
    return register_clip(clip.with_effects([vfx.MakeLoopable(overlap_duration)]))

@mcp.tool
def vfx_margin(clip_id: str, margin: int, color: list[int] = (0, 0, 0)) -> str:
    """Add margin."""
    clip = get_clip(clip_id)
    return register_clip(clip.with_effects([vfx.Margin(margin, color=tuple(color))]))

@mcp.tool
def vfx_mask_color(clip_id: str, color: list[int] = (0, 0, 0), threshold: float = 0, stiffness: float = 1) -> str:
    """Mask color."""
    clip = get_clip(clip_id)
    return register_clip(clip.with_effects([vfx.MaskColor(tuple(color), threshold, stiffness)]))

@mcp.tool
def vfx_masks_and(clip_id: str, other_clip_id: str) -> str:
    """Logical AND of masks."""
    clip = get_clip(clip_id)
    other = get_clip(other_clip_id)
    return register_clip(clip.with_effects([vfx.MasksAnd(other)]))

@mcp.tool
def vfx_masks_or(clip_id: str, other_clip_id: str) -> str:
    """Logical OR of masks."""
    clip = get_clip(clip_id)
    other = get_clip(other_clip_id)
    return register_clip(clip.with_effects([vfx.MasksOr(other)]))

@mcp.tool
def vfx_mirror_x(clip_id: str) -> str:
    """Mirror X."""
    clip = get_clip(clip_id)
    return register_clip(clip.with_effects([vfx.MirrorX()]))

@mcp.tool
def vfx_mirror_y(clip_id: str) -> str:
    """Mirror Y."""
    clip = get_clip(clip_id)
    return register_clip(clip.with_effects([vfx.MirrorY()]))

@mcp.tool
def vfx_multiply_color(clip_id: str, factor: float) -> str:
    """Multiply color."""
    clip = get_clip(clip_id)
    return register_clip(clip.with_effects([vfx.MultiplyColor(factor)]))

@mcp.tool
def vfx_multiply_speed(clip_id: str, factor: float) -> str:
    """Multiply speed."""
    clip = get_clip(clip_id)
    return register_clip(clip.with_effects([vfx.MultiplySpeed(factor)]))

@mcp.tool
def vfx_painting(clip_id: str, saturation: float = 1.4, black: float = 0.006) -> str:
    """Painting effect."""
    clip = get_clip(clip_id)
    return register_clip(clip.with_effects([vfx.Painting(saturation, black)]))

@mcp.tool
def vfx_quad_mirror(clip_id: str, x: int = None, y: int = None) -> str:
    """Apply quad mirror effect with custom axes."""
    clip = get_clip(clip_id)
    return register_clip(clip.with_effects([QuadMirror(x, y)]))

@mcp.tool
def vfx_chroma_key(clip_id: str, color: list[int] = (0, 255, 0), threshold: float = 50, softness: float = 20) -> str:
    """Apply an advanced Chroma Key effect to create transparency."""
    clip = get_clip(clip_id)
    return register_clip(clip.with_effects([ChromaKey(tuple(color), threshold, softness)]))

@mcp.tool
def vfx_rgb_sync(
    clip_id: str,
    r_offset: list[int] = (0, 0),
    g_offset: list[int] = (0, 0),
    b_offset: list[int] = (0, 0),
    r_time_offset: float = 0.0,
    g_time_offset: float = 0.0,
    b_time_offset: float = 0.0
) -> str:
    """Apply an RGB sync/split effect with spatial and temporal offsets."""
    clip = get_clip(clip_id)
    return register_clip(clip.with_effects([RGBSync(
        tuple(r_offset), tuple(g_offset), tuple(b_offset),
        r_time_offset, g_time_offset, b_time_offset
    )]))

@mcp.tool
def vfx_resize(clip_id: str, width: int = None, height: int = None, scale: float = None) -> str:
    """Resize clip."""
    clip = get_clip(clip_id)
    if scale is not None:
        new_size = scale
    elif width is not None and height is not None:
        new_size = (width, height)
    elif width is not None:
        new_size = (width, None)
    elif height is not None:
        new_size = (None, height)
    else:
        raise ValueError("Provide scale, width, or height.")
    return register_clip(clip.with_effects([vfx.Resize(new_size)]))

@mcp.tool
def vfx_rotate(clip_id: str, angle: float, resample: str = "bicubic", expand: bool = True) -> str:
    """Rotate clip."""
    clip = get_clip(clip_id)
    return register_clip(clip.with_effects([vfx.Rotate(angle, resample, expand)]))

@mcp.tool
def vfx_scroll(clip_id: str, w: int = None, h: int = None, x_speed: float = 0, y_speed: float = 0, x_start: float = 0, y_start: float = 0) -> str:
    """Scroll clip."""
    clip = get_clip(clip_id)
    return register_clip(clip.with_effects([vfx.Scroll(w, h, x_speed, y_speed, x_start, y_start)]))

@mcp.tool
def vfx_slide_in(clip_id: str, duration: float, side: str) -> str:
    """Slide in."""
    clip = get_clip(clip_id)
    return register_clip(clip.with_effects([vfx.SlideIn(duration, side)]))

@mcp.tool
def vfx_slide_out(clip_id: str, duration: float, side: str) -> str:
    """Slide out."""
    clip = get_clip(clip_id)
    return register_clip(clip.with_effects([vfx.SlideOut(duration, side)]))

@mcp.tool
def vfx_supersample(clip_id: str, d: float, nframes: int) -> str:
    """Supersample."""
    clip = get_clip(clip_id)
    return register_clip(clip.with_effects([vfx.SuperSample(d, nframes)]))

@mcp.tool
def vfx_time_mirror(clip_id: str) -> str:
    """Time mirror."""
    clip = get_clip(clip_id)
    return register_clip(clip.with_effects([vfx.TimeMirror()]))

@mcp.tool
def vfx_time_symmetrize(clip_id: str) -> str:
    """Time symmetrize."""
    clip = get_clip(clip_id)
    return register_clip(clip.with_effects([vfx.TimeSymmetrize()]))

# --- Audio Effects ---

@mcp.tool
def afx_audio_delay(clip_id: str, offset: float = 0.2, n_repeats: int = 8, decay: float = 1) -> str:
    """Audio delay."""
    clip = get_clip(clip_id)
    return register_clip(clip.with_effects([afx.AudioDelay(offset, n_repeats, decay)]))

@mcp.tool
def afx_audio_fade_in(clip_id: str, duration: float) -> str:
    """Audio fade in."""
    clip = get_clip(clip_id)
    return register_clip(clip.with_effects([afx.AudioFadeIn(duration)]))

@mcp.tool
def afx_audio_fade_out(clip_id: str, duration: float) -> str:
    """Audio fade out."""
    clip = get_clip(clip_id)
    return register_clip(clip.with_effects([afx.AudioFadeOut(duration)]))

@mcp.tool
def afx_audio_loop(clip_id: str, n_loops: int = None, duration: float = None) -> str:
    """Audio loop."""
    clip = get_clip(clip_id)
    return register_clip(clip.with_effects([afx.AudioLoop(n_loops, duration)]))

@mcp.tool
def afx_audio_normalize(clip_id: str) -> str:
    """Audio normalize."""
    clip = get_clip(clip_id)
    return register_clip(clip.with_effects([afx.AudioNormalize()]))

@mcp.tool
def afx_multiply_stereo_volume(clip_id: str, left: float = 1, right: float = 1) -> str:
    """Multiply stereo volume."""
    clip = get_clip(clip_id)
    return register_clip(clip.with_effects([afx.MultiplyStereoVolume(left, right)]))

@mcp.tool
def afx_multiply_volume(clip_id: str, factor: float) -> str:
    """Multiply volume."""
    clip = get_clip(clip_id)
    return register_clip(clip.with_effects([afx.MultiplyVolume(factor)]))

# --- Tools ---

@mcp.tool
def tools_detect_scenes(clip_id: str, luminosity_threshold: int = 10) -> list:
    """Detect scenes in a clip. Returns list of timestamps."""
    clip = get_clip(clip_id)
    cuts, luminosities = detect_scenes(clip, luminosity_threshold=luminosity_threshold)
    return [[float(start), float(end)] for start, end in cuts]

@mcp.tool
def tools_find_video_period(clip_id: str, start_time: float = 0.0) -> float:
    """Find video period."""
    clip = get_clip(clip_id)
    return float(find_video_period(clip, start_time=start_time))

@mcp.tool
def tools_drawing_color_gradient(size: list[int], p1: list[int], p2: list[int], col1: list[int], col2: list[int], shape: str = "linear", offset: float = 0) -> str:
    """Create a color gradient image clip."""
    img = drawing.color_gradient(tuple(size), tuple(p1), tuple(p2), tuple(col1), tuple(col2), shape, offset)
    clip = ImageClip(img)
    return register_clip(clip)

@mcp.tool
def tools_drawing_color_split(size: list[int], x: int, y: int, p1: list[int], p2: list[int], col1: list[int], col2: list[int], grad_width: int = 0) -> str:
    """Create a color split image clip."""
    img = drawing.color_split(tuple(size), x, y, tuple(p1), tuple(p2), tuple(col1), tuple(col2), grad_width)
    clip = ImageClip(img)
    return register_clip(clip)

@mcp.tool
def tools_file_to_subtitles(filename: str, encoding: str = "utf-8") -> list:
    """Convert subtitle file to list of (start, end, text)."""
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File {filename} not found.")
    subs = file_to_subtitles(filename, encoding=encoding)
    return [[float(s), float(e), txt] for s, e, txt in subs]

@mcp.tool
def write_gif(
    clip_id: str,
    filename: str,
    fps: float = None,
    program: str = "imageio",
    opt: str = "OptimizePlus",
    fuzz: int = 1,
    loop: int = 0,
    dispose: bool = False,
    colors: int = None
) -> str:
    """Write a video clip to a GIF file."""
    clip = get_clip(clip_id)
    clip.write_gif(
        filename,
        fps=fps,
        program=program,
        opt=opt,
        fuzz=fuzz,
        loop=loop,
        dispose=dispose,
        colors=colors
    )
    return f"Successfully wrote GIF to {filename}"

@mcp.tool
def tools_find_audio_period(clip_id: str, start_time: float = 0.0) -> float:
    """Find the period of the audio signal."""
    from moviepy.audio.tools.cuts import find_audio_period
    clip = get_clip(clip_id)
    return float(find_audio_period(clip, start_time=start_time))

@mcp.tool
def tools_check_installation() -> str:
    """Check MoviePy installation and dependencies."""
    from moviepy.config import check
    try:
        check()
        return "Installation check ran (check server logs)."
    except Exception as e:
        return f"Check failed: {e}"

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8080)
