# Specification: Expose Core Video Creation Tools

## Overview
This track focuses on exposing the fundamental video creation and manipulation capabilities of MoviePy as MCP tools. The goal is to provide a comprehensive set of tools that allow for the programmatic creation of video clips from various sources (text, colors, images) and the ability to combine them.

## Target Tools

### 1. `create_text_clip`
- **MoviePy Class:** `TextClip`
- **Functionality:** Generates a video clip from a text string.
- **Parameters:**
    - `text` (str): The text to display.
    - `font` (str, optional): Font name.
    - `fontsize` (int, optional): Size of the font.
    - `color` (str, optional): Text color (e.g., 'white', '#FFFFFF').
    - `bg_color` (str, optional): Background color.
    - `duration` (float): Duration of the clip in seconds.
    - `method` (str, optional): 'label' or 'caption'.

### 2. `create_color_clip`
- **MoviePy Class:** `ColorClip`
- **Functionality:** Generates a solid color video clip.
- **Parameters:**
    - `size` (tuple): Width and height of the clip.
    - `color` (str or list): Color of the clip.
    - `duration` (float): Duration of the clip.

### 3. `create_image_clip`
- **MoviePy Class:** `ImageClip`
- **Functionality:** Creates a video clip from a static image file.
- **Parameters:**
    - `img_path` (str): Path to the image file.
    - `duration` (float): Duration of the clip.

### 4. `concatenate_videoclips`
- **MoviePy Function:** `concatenate_videoclips`
- **Functionality:** Joins multiple video clips into a single sequence.
- **Parameters:**
    - `clip_paths` (list[str]): List of paths to video files to concatenate.
    - `method` (str, optional): 'chain' or 'compose'.

## Technical Requirements
- **Mapping:** Each tool must map directly to its MoviePy counterpart.
- **Docstrings:** Must reference the specific sections in the local `html/` documentation.
- **File Handling:** Tools should handle temporary file creation and return paths to generated files.
- **Validation:** Input parameters must be validated against MoviePy expectations.

## Reference
- See `html/ref/VideoClip/TextClip.html` (example path)
- See `html/ref/VideoClip/ColorClip.html`
- See `html/ref/VideoClip/ImageClip.html`
- See `html/ref/functions/concatenate_videoclips.html`
