
import unittest
from unittest.mock import MagicMock
import numpy as np
from custom_fx.rgb_sync import RGBSync

class MockClip:
    def __init__(self):
        self.duration = 1.0
        self.w = 100
        self.h = 100
        # Create a real array to allow slicing
        self.get_frame = MagicMock(return_value=np.zeros((100, 100, 3), dtype=np.uint8))

    def transform(self, func):
        self.func = func
        return self

class TestRGBSyncOptimization(unittest.TestCase):
    def test_redundant_fetches_avoided(self):
        clip = MockClip()
        # Case 1: All offsets zero
        effect = RGBSync(r_time_offset=0, g_time_offset=0, b_time_offset=0)

        # Apply effect to get the filter function
        # Note: RGBSync.apply returns clip.transform(filter)
        # We mocked transform to capture the function
        result_clip = effect.apply(clip)
        filter_func = clip.func

        # Call the filter function for t=0
        # The filter function signature in RGBSync.apply is: def filter(get_frame, t)
        # So we pass clip.get_frame and t

        res = filter_func(clip.get_frame, 0)

        # Verify get_frame was called exactly ONCE
        self.assertEqual(clip.get_frame.call_count, 1, "get_frame should be called once when all offsets are zero")

        # Verify output shape is correct (H, W, 3)
        self.assertEqual(res.shape, (100, 100, 3), "Output shape should be preserved")

        # Case 2: Different offsets
        clip.get_frame.reset_mock()
        effect = RGBSync(r_time_offset=0, g_time_offset=0.1, b_time_offset=0.2)
        effect.apply(clip) # updates clip.func
        filter_func = clip.func

        filter_func(clip.get_frame, 0)
        # Should be called 3 times: t=0, t=0.1, t=0.2
        self.assertEqual(clip.get_frame.call_count, 3, "get_frame should be called 3 times for different offsets")

        # Case 3: Mixed zero and non-zero
        clip.get_frame.reset_mock()
        effect = RGBSync(r_time_offset=0, g_time_offset=0.1, b_time_offset=0)
        effect.apply(clip)
        filter_func = clip.func

        filter_func(clip.get_frame, 0)
        # R (offset=0) -> calls get_frame(0) (primary)
        # G (offset=0.1) -> calls get_frame(0.1)
        # B (offset=0) -> reuses primary_frame
        # Total 2 calls.
        self.assertEqual(clip.get_frame.call_count, 2, "get_frame should be called 2 times for mixed offsets")

if __name__ == '__main__':
    unittest.main()
