# mcp-moviepy Gemini-CLI Extension

[![MCP](https://img.shields.io/badge/MCP-Compatible-blue)](https://modelcontextprotocol.io)
[![Python](https://img.shields.io/badge/Python-3.12+-green.svg)](https://www.python.org/)
[![MoviePy](https://img.shields.io/badge/MoviePy-2.2+-orange.svg)](https://zulko.github.io/moviepy/)

A Model Context Protocol (MCP) server that provides a comprehensive interface to the [MoviePy](https://zulko.github.io/moviepy/) video editing library. 

This server exposes **over 70 tools** allowing LLMs to perform professional-grade video editing, compositing, effects application, and audio processing.

## 🚀 Features

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

### Custom Advanced Effects
This server includes several high-performance custom effects:
- **`vfx_matrix`**: Classic "Matrix" digital rain overlay.
- **`vfx_kaleidoscope`**: Radial symmetry effect with custom slices.
- **`vfx_rgb_sync`**: Chromatic aberration and glitch temporal offsets.
- **`vfx_chroma_key`**: Advanced green screen removal with threshold and softness.
- **`vfx_auto_framing`**: Intelligent face/subject tracking and cropping for vertical video.
- **`vfx_clone_grid`**: Multi-clone grid layout (2x2, 4x4, etc.).
- **`vfx_rotating_cube`**: 3D perspective cube mapping.
- **`vfx_quad_mirror`**: Four-way mirror symmetry.
- **`vfx_kaleidoscope_cube`**: Hybrid effect combining radial symmetry with 3D rotation.

### Audio Effects (afx)
- `afx_volume_multiply`, `afx_multiply_stereo_volume`, `afx_audio_fade_in`, `afx_audio_fade_out`, `afx_audio_delay`, `afx_audio_loop`, `afx_audio_normalize`.

### Analysis & Utilities
- `tools_detect_scenes`: Automatic scene cut detection.
- `tools_find_video_period`: Frequency analysis for repetitive motion.
- `tools_find_audio_period`: Tempo/period detection for audio.
- `tools_file_to_subtitles`: Parse subtitle files.

## 🛠 Prerequisites

- **Python 3.12+**
- **FFmpeg**: Required by MoviePy for video processing.
- **ImageMagick**: Required for `text_clip` and `credits_clip`.
- **uv**: Recommended Python package manager.

### Gemini-CLI Exclusive Includes 2 custom skills moviepy-effects & mcp-prompt-generator 

moviepy-effects is for generating custom effects for the moviepy package and will automatically create the file in the custom_fx directory plus will also
add it to the mcp-moviepy server as a tool & will automatically generate test scripts for it. mcp-prompt-generator is for generating custom prompts for gemini-cli
but is only for working with mcp-moviepy MCP server it has hardcoded within its instructions documentation from moviepy's docs. 

## 📦 Installation

### As a Gemini-CLI Extension

```bash
gemini extensions install https://github.com/vizionik25/mcp-moviepy.git
```

### Or Install it as a Standalone MCP Server to be used with other clients (e.g. Claude Code, Windsurf, Cursor)

```bash
git clone https://github.com/your-repo/mcp-moviepy.git
cd mcp-moviepy
uv sync
```
the uv sync will handle venv creation and install all python packages in a single step but you will still need to activate it.

```bash
source .venv/bin/activate
```

## 🏃 Running the Server

The server is built with `fastmcp` and runs over HTTP by default.

```bash
uv run main.py
```

### Adding to MCP Hosts

```json
{
  "mcpServers": {
    "moviepy": {
      "url": "http://localhost:8080/mcp"
    }
  }
}
```

## 🐳 Docker Support

You can run this MCP server as a containerized service. This is the recommended approach as it handles all complex system dependencies like FFmpeg, ImageMagick (with correct security policies), and OpenCV libraries automatically.

### Build and Run with Docker

1. **Prepare your data**: Create a `data` directory in the project root and place the video/image files you want to edit inside it:
   ```bash
   mkdir -p data
   # Copy your media files into ./data
   ```

2. **Build the image:**
   ```bash
   docker build -t mcp-moviepy .
   ```

3. **Run the container:**
   ```bash
   docker run -p 8080:8080 -v $(pwd)/data:/app/data mcp-moviepy
   ```

### Using Docker Compose (Recommended)

The included `docker-compose.yml` simplifies setup and persistence:

```bash
docker compose up --build
```

### Configuration Details

- **Port Mapping**: The container exposes port `8080`. The MCP endpoint will be accessible at `http://localhost:8080/mcp`.
- **Volume Mounts**: The `./data` directory on your host is mapped to `/app/data` in the container. 
  - **Important**: Place your source videos/images in `./data` and reference them as `/app/data/filename.mp4` when using MCP tools.
- **Environment Variables**:
  - `PYTHONUNBUFFERED=1`: Ensures Python logs are flushed to the terminal immediately.

## 🧠 State Management

The server maintains an in-memory state of `CLIPS`. 

1. **Clip IDs**: Tools that create or modify clips return a `clip_id` (UUID string).
2. **Chaining**: Pass the `clip_id` to subsequent tools to perform further operations.
3. **Memory**: Use `list_clips` to see active objects and `delete_clip` to free system memory.
4. **Auto Memory Cleanup**: It has file count and total file size limits in place to prevent filling up all your ram
and ultimately prevent crashing your machine.

## 💡 Prompts

The server includes several "Prompt Templates" that guide the LLM in performing complex tasks:
- `slideshow_wizard`: Create a professional slideshow from images with transitions.
- `glitch_effect_preset`: Apply a high-energy glitch aesthetic.
- `auto_framing_for_tiktok`: Convert horizontal video to vertical for social media.
- `matrix_intro_preset`: Apply the classic code-rain overlay.
- `rotating_cube_transition`: Create a 3D spinning transition.

## 🧪 Development

Run tests to verify installation:

```bash
uv run pytest tests/test_e2e.py
```

## 📄 License

MIT
