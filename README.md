# mcp-moviepy

A Model Context Protocol (MCP) server that provides a comprehensive interface to the [MoviePy v2.0](https://zulko.github.io/moviepy/) video editing library. 

This server exposes **over 70 tools** allowing LLMs to perform professional-grade video editing, compositing, effects application, and audio processing.

## Features

### IO & Creation
- **Load**: `video_file_clip`, `audio_file_clip`, `image_clip`, `image_sequence_clip`.
- **Generate**: `text_clip`, `color_clip`, `credits_clip`, `subtitles_clip`, `tools_drawing_color_gradient`, `tools_drawing_color_split`.
- **Export**: `write_videofile`, `write_audiofile`, `write_gif`.
- **Fast Tools**: `tools_ffmpeg_extract_subclip` (lossless trimming).

### Compositing & Transformation
- **Combine**: `composite_video_clips`, `concatenate_video_clips`, `tools_clips_array` (grid layout), `composite_audio_clips`, `concatenate_audio_clips`.
- **Refine**: `subclip`, `vfx_resize`, `vfx_crop`, `vfx_rotate`.
- **Configure**: `set_position`, `set_audio`, `set_mask`, `set_start`, `set_end`, `set_duration`.

### Video Effects (vfx)
- **Time**: `vfx_freeze`, `vfx_freeze_region`, `vfx_multiply_speed`, `vfx_time_mirror`, `vfx_time_symmetrize`, `vfx_loop`, `vfx_make_loopable`, `vfx_accel_decel`.
- **Color**: `vfx_black_white`, `vfx_invert_colors`, `vfx_fade_in`, `vfx_fade_out`, `vfx_gamma_correction`, `vfx_lum_contrast`, `vfx_multiply_color`, `vfx_painting`, `vfx_blink`.
- **Geometry**: `vfx_mirror_x`, `vfx_mirror_y`, `vfx_even_size`, `vfx_margin`, `vfx_scroll`, `vfx_supersample`.
- **Motion**: `vfx_slide_in`, `vfx_slide_out`, `vfx_head_blur`.
- **Masking**: `vfx_mask_color`, `vfx_masks_and`, `vfx_masks_or`.

### Audio Effects (afx)
- `afx_volume_multiply`, `afx_multiply_stereo_volume`, `afx_audio_fade_in`, `afx_audio_fade_out`, `afx_audio_delay`, `afx_audio_loop`, `afx_audio_normalize`.

### Analysis
- `tools_detect_scenes`, `tools_find_video_period`, `tools_find_audio_period`, `tools_file_to_subtitles`.

## Configuration

### Running the Server
The server is built with `fastmcp` and is configured to run over HTTP by default.

```bash
uv run main.py
```

### Adding to MCP Hosts
To use this server with an MCP-compatible host (e.g., Claude Desktop), add it to your configuration:

```json
{
  "mcpServers": {
    "moviepy": {
      "command": "uv",
      "args": ["run", "path/to/mcp-moviepy/main.py"]
    }
  }
}
```

## State Management
The server maintains an in-memory state of `CLIPS`. 
1. Tools that create or modify clips return a `clip_id` (UUID).
2. Subsequent tools accept this `clip_id` to perform further operations.
3. Use `list_clips` to see active objects and `delete_clip` to free system memory.
