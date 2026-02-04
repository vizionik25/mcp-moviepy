# Custom MoviePy Effects

This document provides documentation for the custom effects implemented in the `custom_fx/` directory of the `mcp-moviepy` project.

## Table of Contents
1. [Matrix Digital Rain](#matrix-digital-rain)
2. [Kaleidoscope](#kaleidoscope)
3. [RGB Sync (Glitch)](#rgb-sync-glitch)
4. [Chroma Key (Green Screen)](#chroma-key-green-screen)
5. [Quad Mirror](#quad-mirror)

---

## Matrix Digital Rain
**File:** `custom_fx/matrix.py`  
**Class:** `Matrix`

Overlays a "Matrix" style digital rain animation on the clip. The rain features falling characters with a bright leading edge and a fading trail.

### Parameters
- `speed` (float, default: `150`): Speed of falling characters in pixels per second.
- `density` (float, default: `0.2`): Probability (0.0 to 1.0) that a column will contain a falling drop.
- `chars` (str, default: `"0123456789ABCDEF"`): The character set used for the digital rain.
- `color` (str, default: `"green"`): Color of the rain. Supported options: `red`, `green`, `blue`, `white`.
- `font_size` (int, default: `16`): Size of the characters.

---

## Kaleidoscope
**File:** `custom_fx/kaleidoscope.py`  
**Class:** `Kaleidoscope`

Creates a radial symmetry effect by taking a wedge of the source image and mirroring/rotating it around a center point.

### Parameters
- `n_slices` (int, default: `6`): Number of radial slices. Even numbers are recommended for seamless mirroring.
- `x` (int, optional): Horizontal center of the effect. Defaults to the clip's center.
- `y` (int, optional): Vertical center of the effect. Defaults to the clip's center.

---

## RGB Sync (Glitch)
**File:** `custom_fx/rgb_sync.py`  
**Class:** `RGBSync`

Splits the RGB channels and applies spatial and/or temporal offsets to create a chromatic aberration or glitch effect.

### Parameters
- `r_offset`, `g_offset`, `b_offset` (tuple, default: `(0, 0)`): (x, y) pixel offsets for each channel.
- `r_time_offset`, `g_time_offset`, `b_time_offset` (float, default: `0.0`): Time offset in seconds for each channel.

---

## Chroma Key (Green Screen)
**File:** `custom_fx/chroma_key.py`  
**Class:** `ChromaKey`

An advanced chroma key effect that generates a transparency mask based on Euclidean distance from a target color.

### Parameters
- `color` (tuple, default: `(0, 255, 0)`): Target RGB color to remove.
- `threshold` (float, default: `50`): Distance threshold below which pixels are fully transparent.
- `softness` (float, default: `20`): Range over which pixels transition from transparent to opaque.

---

## Quad Mirror
**File:** `custom_fx/quad_mirror.py`  
**Class:** `QuadMirror`

Mirrors the clip both horizontally and vertically based on a custom center point, effectively creating four mirrored versions of the source quadrant.

### Parameters
- `x` (int, optional): Horizontal axis for mirroring. Defaults to the clip's center.
- `y` (int, optional): Vertical axis for mirroring. Defaults to the clip's center.
