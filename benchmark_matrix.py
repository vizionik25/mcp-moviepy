
import sys
import os
import time
import numpy as np
from PIL import Image

# Ensure we can import from the current directory
sys.path.append(os.getcwd())

try:
    from custom_fx.matrix import Matrix
except ImportError:
    pass

class MockClip:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.size = (w, h)

    def transform(self, filter_func):
        return filter_func

def main():
    w, h = 640, 480
    clip = MockClip(w, h)
    matrix_fx = Matrix(speed=150, density=0.2, font_size=16, seed=42)

    # Initialize the effect
    filter_func = matrix_fx.apply(clip)

    # Create a dummy frame (black)
    frame = np.zeros((h, w, 3), dtype=np.uint8)

    # Mock get_frame
    def get_frame(t):
        return frame

    # Measure performance
    # Warmup
    filter_func(get_frame, 0.0)

    start_time = time.time()
    num_frames = 50
    last_out = None

    for i in range(num_frames):
        t = i * 0.1
        out = filter_func(get_frame, t)
        last_out = out

    end_time = time.time()
    duration = end_time - start_time
    fps = num_frames / duration

    print(f"Time for {num_frames} frames: {duration:.4f}s")
    print(f"FPS: {fps:.2f}")

    # Save last frame
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        Image.fromarray(last_out).save(filename)
        print(f"Saved last frame to {filename}")

if __name__ == "__main__":
    main()
