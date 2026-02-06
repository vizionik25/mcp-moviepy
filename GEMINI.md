# MCP MoviePy: Agentic Workflow & Documentation

This document provides essential context and instructions for AI agents using the `mcp-moviepy` server. It outlines tool usage, standard operating procedures, and safety boundaries.

---

## 1. Tool Definitions

The server maintains an in-memory state of `CLIPS`. Most tools return a `clip_id` (UUID string) which must be passed to subsequent tools.

### Clip Management
- `list_clips()`: Returns a mapping of `clip_id` to its Python type. Use this to audit memory usage.
- `delete_clip(clip_id)`: Explicitly closes and removes a clip from memory. **MANDATORY** for large projects to avoid OOM.
- `validate_path(filename)`: Ensures paths are within the project root or `/tmp`.

### Video/Image IO & Creation
- `video_file_clip(filename, ...)`: Loads a video file. Supports `target_resolution` for downscaling.
- `image_clip(filename, duration, ...)`: Loads a static image as a video clip.
- `text_clip(text, font, font_size, ...)`: Generates a clip from text. **Requires ImageMagick.**
- `image_sequence_clip(sequence, fps, ...)`: Creates a video from a list of images or a folder.
- `color_clip(size, color, duration)`: Creates a solid color background clip.
- `credits_clip(creditfile, width, ...)`: Creates scrolling credits from a text file.
- `subtitles_clip(filename, ...)`: Generates a subtitle overlay from an `.srt` file.

### Audio IO
- `audio_file_clip(filename)`: Loads an audio file.
- `write_audiofile(clip_id, filename, ...)`: Exports an audio clip.

### Transformations & Compositing
- `subclip(clip_id, start_time, end_time)`: Trims a clip.
- `set_position(clip_id, x, y, pos_str, ...)`: Sets the (x, y) coordinates or named position (e.g., "center").
- `set_audio(clip_id, audio_clip_id)`: Attaches an audio clip to a video clip.
- `composite_video_clips(clip_ids, size, ...)`: Layers multiple clips. The first clip in the list is the background if `use_bgclip=True`.
- `concatenate_video_clips(clip_ids, ...)`: Joins clips end-to-end.
- `tools_clips_array(clip_ids_rows, ...)`: Arranges clips in a grid (e.g., 2x2).

### Effects (VFX & AFX)
The server exposes over 50 effects. Key categories:
- **Time**: `vfx_loop`, `vfx_freeze`, `vfx_multiply_speed`, `vfx_accel_decel`.
- **Visual**: `vfx_black_white`, `vfx_fade_in`, `vfx_fade_out`, `vfx_lum_contrast`, `vfx_crop`, `vfx_resize`, `vfx_rotate`.
- **Advanced/Custom**: `vfx_chroma_key`, `vfx_auto_framing`, `vfx_matrix`, `vfx_kaleidoscope`, `vfx_rotating_cube`, `vfx_rgb_sync`.
- **Audio**: `afx_audio_fade_in`, `afx_audio_normalize`, `afx_multiply_volume`.

### Analysis & Export
- `tools_detect_scenes(clip_id)`: Returns timestamps of detected scene cuts.
- `write_videofile(clip_id, filename, ...)`: Renders the final video. This is a blocking, resource-intensive operation.
- `write_gif(clip_id, filename, ...)`: Renders to a GIF.
- `tools_ffmpeg_extract_subclip(...)`: Fast, lossless trimming of a file without re-encoding.

---

## 2. Workflow Specifications

### Standard Operating Procedure (SOP)
1.  **Initialize**: Load source assets using `video_file_clip` or `image_clip`.
2.  **Inspect**: (Optional) Use `tools_detect_scenes` or `tools_find_video_period` to understand asset structure.
3.  **Transform**: Apply trims (`subclip`), resizing (`vfx_resize`), and positioning (`set_position`).
4.  **Enhance**: Apply visual or audio effects (VFX/AFX).
5.  **Composite**: Combine clips using `composite_video_clips` or `concatenate_video_clips`.
6.  **Verify**: Check `list_clips` to ensure the pipeline is correctly constructed.
7.  **Export**: Call `write_videofile` to render the final result.
8.  **Cleanup**: Call `delete_clip` on all intermediate `clip_id`s to free memory.

### Decision Tree: Selection of Composite Tool
- Use `concatenate_video_clips` for sequential storytelling.
- Use `composite_video_clips` for overlays, watermarks, or PIP (Picture-in-Picture).
- Use `tools_clips_array` for comparisons, reaction videos, or multi-cam views.

---

## 3. Contextual Constraints

-   **Memory Limit**: The server allows a maximum of **100 concurrent clips**. Always delete unused clips.
-   **File System**: Paths must be absolute or relative to the project root. The server enforces basic path validation.
-   **Blocking Operations**: Rendering (`write_videofile`) and complex VFX (like `vfx_auto_framing`) are blocking and can take minutes.
-   **ImageMagick**: `text_clip` will fail if ImageMagick is not configured correctly on the host system.
-   **Clip Immutability**: MoviePy clips are semi-immutable. Most tools return a **new** `clip_id` rather than modifying the existing one.

---

## 4. Error Handling Protocols

### Common Errors & Diagnostics
-   **Clip Not Found**: Verify the `clip_id` exists in `list_clips()`. Note that applying an effect creates a *new* ID.
-   **FileNotFoundError**: Use `validate_path` or check if the file exists on the local disk before loading.
-   **ImageMagick Error**: If `text_clip` fails with a "convert" error, inform the user that ImageMagick is required.
-   **Max Clips Reached**: Run `delete_clip` on all unnecessary IDs.
-   **AttributeError (Audio)**: Some clips may not have audio. Use `set_audio` if a video file is loaded with `audio=False`.

### Troubleshooting Step
1.  Run `tools_check_installation()` to verify MoviePy and FFmpeg dependencies.
2.  Audit the current state with `list_clips()`.
3.  Check server stderr for detailed MoviePy/FFmpeg logs.

---

## 5. Security Directives

-   **Path Traversal**: Never accept raw user input for filenames without passing them through `validate_path`.
-   **Command Injection**: The server uses `numexpr` for math expressions in `vfx_head_blur` to avoid unsafe `eval()`. Do not implement custom math parsing using `eval`.
-   **Resource Exhaustion**: Monitor `MAX_CLIPS`. Do not create clips in infinite loops.
-   **Data Privacy**: Avoid writing sensitive information into `text_clip` or `credits_clip` that will be baked into the video.