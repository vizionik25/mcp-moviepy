from moviepy import Effect
import numpy as np
from PIL import Image, ImageDraw, ImageFont

class Matrix(Effect):
    """
    A MoviePy effect that overlays a 'Matrix' digital rain animation on a clip.
    
    Parameters:
    -----------
    speed : float
        The speed of the falling characters in pixels per second.
    density : float
        The probability (0 to 1) that a column will have a falling drop.
    chars : str
        The set of characters to use for the digital rain.
    color : str
        The color of the rain. Options: 'red', 'green', 'blue', 'white'.
    font_size : int
        Size of the characters.
    seed : int
        Seed for the random number generator.
    """
    def __init__(self, speed=150, density=0.2, chars="0123456789ABCDEF", color="green", font_size=16, seed=42):
        self.seed = seed
        self.speed = speed
        self.density = density
        self.chars = chars
        self.color_name = color.lower()
        self.font_size = font_size
        self.seed = seed
        
        # Color mapping
        colors = {
            "red": (255, 0, 0),
            "green": (0, 255, 0),
            "blue": (0, 0, 255),
            "white": (255, 255, 255)
        }
        self.rgb = np.array(colors.get(self.color_name, (0, 255, 0)), dtype=np.uint8)
        
        # Internal state
        self._atlas = None
        self.char_w = 0
        self.char_h = 0

    def _init_atlas(self):
        """Pre-renders the character set into a font atlas for fast blitting."""
        try:
            # Try to load a monospace font
            font = ImageFont.truetype("DejaVuSansMono.ttf", self.font_size)
        except:
            font = ImageFont.load_default()
            
        # Fixed grid size based on font size
        self.char_w = self.font_size
        self.char_h = int(self.font_size * 1.3)
        
        num_chars = len(self.chars)
        self._atlas = np.zeros((num_chars, self.char_h, self.char_w), dtype=np.uint8)
        
        for i, char in enumerate(self.chars):
            img = Image.new('L', (self.char_w, self.char_h), 0)
            draw = ImageDraw.Draw(img)
            draw.text((0, 0), char, font=font, fill=255)
            self._atlas[i] = np.array(img)

    def apply(self, clip):
        if self._atlas is None:
            self._init_atlas()
            
        h, w = clip.h, clip.w
        rows = h // self.char_h + 1
        cols = w // self.char_w + 1
        
        # Pre-generate column offsets and speeds for consistency
        rng = np.random.default_rng(self.seed)
        col_offsets = rng.random(cols) * h * 2
        col_speeds = self.speed * (0.8 + 0.4 * rng.random(cols))
        col_active = (rng.random(cols) < self.density).astype(np.float32)
        
        # Static grid for character randomization
        base_char_grid = rng.integers(0, len(self.chars), size=(rows, cols))

        def filter(get_frame, t):
            frame = get_frame(t)
            
            # 1. Calculate the Brightness Grid (Vectorized)
            # Time-based position of the 'lead' for each column
            trail_len = max(1, h // 2)
            lead_y = (col_speeds * t + col_offsets) % (h + trail_len)
            
            # Create a Y-coordinate grid for the rows
            row_y = (np.arange(rows) * self.char_h).astype(np.int32)
            
            # Calculate distance from each cell to its column's lead position
            # Shape: (rows, cols)
            # Use integer arithmetic for distance
            lead_y_int = lead_y.astype(np.int32)
            dist = lead_y_int[None, :] - row_y[:, None]
            
            # Brightness decreases as we move away from the lead (upward)
            # brightness_val = 256 - (dist * 256) // trail_len
            brightness_val = 256 - ((dist << 8) // trail_len)

            # Apply bounds (0 to trail_len)
            mask_body = (dist >= 0) & (dist < trail_len)
            brightness_int = np.where(mask_body, brightness_val, 0)
            
            # Highlight the head of the drop (brightness 1.4 -> 358)
            mask_head = (dist >= 0) & (dist < self.char_h)
            brightness_int = np.where(mask_head, 358, brightness_int)
            
            # Apply column activity mask
            brightness_int = (brightness_int * col_active.astype(np.int32)[None, :]).astype(np.uint16)
            
            # 2. Randomize characters periodically
            # Characters change slightly over time to simulate shifting data
            char_tick = int(t * 12)
            char_indices = (base_char_grid + char_tick) % len(self.chars)
            
            # 3. Assemble the Rain Layer (Vectorized Blitting)
            # Pick character bitmaps from atlas: (rows, cols, char_h, char_w)
            char_slices = self._atlas[char_indices]
            
            # Apply brightness: (rows, cols, char_h, char_w)
            # Use fixed-point arithmetic (x256) for brightness application
            rain_mask = (char_slices.astype(np.uint16) * brightness_int[:, :, None, None]) >> 8
            
            # Reshape/Transpose to form the full rain image
            # (rows, cols, char_h, char_w) -> (rows, char_h, cols, char_w) -> (H, W)
            rain_layer = rain_mask.transpose(0, 2, 1, 3).reshape(rows * self.char_h, cols * self.char_w)
            
            # Crop to frame size
            rain_layer = rain_layer[:h, :w]
            
            # 4. Coloring and Compositing
            # Convert to RGB and apply color
            product = rain_layer[:, :, None].astype(np.uint32) * self.rgb
            rain_rgb = np.minimum(product >> 8, 255).astype(np.uint8)
            
            # Composite with original frame
            # We use an additive blend but slightly dim the background for visibility
            dimmed_bg = (frame.astype(np.uint16) * 205) >> 8
            dimmed_bg = dimmed_bg.astype(np.uint8)
            
            # Additive blend
            out = np.clip(dimmed_bg.astype(np.int16) + rain_rgb.astype(np.int16), 0, 255).astype(np.uint8)
            
            return out

        return clip.transform(filter)
