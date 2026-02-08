import sys
import os
import types
from unittest.mock import MagicMock

# Helper to create dummy file
def create_dummy_file(filename, *args, **kwargs):
    with open(filename, 'w') as f:
        f.write('dummy')

# Mock numpy
if 'numpy' not in sys.modules:
    numpy = MagicMock()
    numpy.uint8 = 'uint8'
    numpy.array = MagicMock(side_effect=lambda x, dtype=None: x)
    numpy.zeros = MagicMock(return_value=MagicMock())
    # Mock testing module for asserts
    class FakeTesting:
        def assert_array_equal(self, *args, **kwargs):
            pass
    numpy.testing = FakeTesting()
    sys.modules['numpy'] = numpy

# Mock PIL
if 'PIL' not in sys.modules:
    PIL = MagicMock()
    # Mock Image.save to create a file
    image_mock = MagicMock()
    image_mock.save = MagicMock(side_effect=create_dummy_file)
    PIL.Image = MagicMock()
    PIL.Image.fromarray = MagicMock(return_value=image_mock)
    sys.modules['PIL'] = PIL

# Mock moviepy
if 'moviepy' not in sys.modules:
    moviepy = MagicMock()
    moviepy.__version__ = '1.0.3'
    sys.modules['moviepy'] = moviepy

    # Mock moviepy submodules
    sys.modules['moviepy.video'] = MagicMock()
    sys.modules['moviepy.video.io'] = MagicMock()
    sys.modules['moviepy.video.io.ffmpeg_tools'] = MagicMock()
    sys.modules['moviepy.video.tools'] = MagicMock()
    sys.modules['moviepy.video.tools.drawing'] = MagicMock()
    sys.modules['moviepy.video.tools.cuts'] = MagicMock()
    sys.modules['moviepy.video.tools.subtitles'] = MagicMock()
    sys.modules['moviepy.video.tools.credits'] = MagicMock()
    sys.modules['moviepy.audio'] = MagicMock()
    sys.modules['moviepy.audio.tools'] = MagicMock()
    sys.modules['moviepy.audio.tools.cuts'] = MagicMock()

    # Configure return values for specific tools
    sys.modules['moviepy.video.tools.cuts'].detect_scenes = MagicMock(return_value=([], []))
    sys.modules['moviepy.video.tools.cuts'].find_video_period = MagicMock(return_value=1.0)
    sys.modules['moviepy.audio.tools.cuts'].find_audio_period = MagicMock(return_value=1.0)

    # Mock instance that behaves like a clip
    mock_clip_instance = MagicMock()
    mock_clip_instance.write_videofile.side_effect = create_dummy_file
    mock_clip_instance.write_audiofile.side_effect = create_dummy_file
    mock_clip_instance.write_gif.side_effect = create_dummy_file
    mock_clip_instance.fps = 24
    mock_clip_instance.duration = 10
    mock_clip_instance.w = 100
    mock_clip_instance.h = 100
    mock_clip_instance.size = (100, 100)

    # Fluent interface mocks
    mock_clip_instance.with_position.return_value = mock_clip_instance
    mock_clip_instance.with_audio.return_value = mock_clip_instance
    mock_clip_instance.with_mask.return_value = mock_clip_instance
    mock_clip_instance.with_start.return_value = mock_clip_instance
    mock_clip_instance.with_end.return_value = mock_clip_instance
    mock_clip_instance.with_duration.return_value = mock_clip_instance
    mock_clip_instance.subclipped.return_value = mock_clip_instance
    mock_clip_instance.with_effects.return_value = mock_clip_instance

    # Classes return this instance
    moviepy.VideoFileClip.return_value = mock_clip_instance
    moviepy.ImageClip.return_value = mock_clip_instance
    moviepy.ImageSequenceClip.return_value = mock_clip_instance
    moviepy.TextClip.return_value = mock_clip_instance
    moviepy.ColorClip.return_value = mock_clip_instance
    moviepy.CreditsClip.return_value = mock_clip_instance
    moviepy.SubtitlesClip.return_value = mock_clip_instance
    moviepy.CompositeVideoClip.return_value = mock_clip_instance
    moviepy.clips_array.return_value = mock_clip_instance
    moviepy.concatenate_videoclips.return_value = mock_clip_instance
    moviepy.CompositeAudioClip.return_value = mock_clip_instance
    moviepy.concatenate_audioclips.return_value = mock_clip_instance
    moviepy.AudioFileClip.return_value = mock_clip_instance
    moviepy.AudioClip.return_value = mock_clip_instance

    # vfx and afx
    vfx = MagicMock()
    moviepy.vfx = vfx

    afx = MagicMock()
    moviepy.afx = afx

    moviepy.__all__ = [
        'VideoFileClip', 'ImageClip', 'ImageSequenceClip', 'TextClip', 'ColorClip',
        'CreditsClip', 'SubtitlesClip', 'CompositeVideoClip', 'clips_array',
        'concatenate_videoclips', 'CompositeAudioClip', 'concatenate_audioclips',
        'AudioFileClip', 'AudioClip', 'vfx', 'afx'
    ]


# Mock fastmcp
if 'fastmcp' not in sys.modules:
    fastmcp = MagicMock()

    class MockFastMCP:
        def __init__(self, name):
            self.name = name

        def tool(self, func):
            func.fn = func
            return func

        def prompt(self, func):
            func.fn = func
            return func

        def run(self, **kwargs):
            pass

    fastmcp.FastMCP = MockFastMCP
    sys.modules['fastmcp'] = fastmcp

# Mock mcp_ui_server
if 'mcp_ui_server' not in sys.modules:
    sys.modules['mcp_ui_server'] = MagicMock()

# Mock numexpr
if 'numexpr' not in sys.modules:
    sys.modules['numexpr'] = MagicMock()

# Mock pydantic
if 'pydantic' not in sys.modules:
    pydantic = MagicMock()
    pydantic.Field = MagicMock(return_value=None)
    sys.modules['pydantic'] = pydantic

# Mock custom_fx
if 'custom_fx' not in sys.modules:
    custom_fx = MagicMock()

    class MockEffect:
        def __init__(self, *args, **kwargs): pass
        def apply(self, clip): return clip

    custom_fx.KaleidoscopeCube = MagicMock(return_value=MockEffect())
    custom_fx.RGBSync = MagicMock()
    custom_fx.QuadMirror = MagicMock()
    custom_fx.ChromaKey = MagicMock()
    custom_fx.Kaleidoscope = MagicMock()
    custom_fx.Matrix = MagicMock()
    custom_fx.AutoFraming = MagicMock()
    custom_fx.CloneGrid = MagicMock()
    custom_fx.RotatingCube = MagicMock()

    sys.modules['custom_fx'] = custom_fx

    # Mock submodules to allow imports like `from custom_fx.matrix import Matrix`
    def mock_submodule(name, class_name):
        m = MagicMock()
        setattr(m, class_name, getattr(custom_fx, class_name))
        sys.modules[f'custom_fx.{name}'] = m

    mock_submodule('matrix', 'Matrix')
    mock_submodule('kaleidoscope', 'Kaleidoscope')
    mock_submodule('kaleidoscope_cube', 'KaleidoscopeCube')
    mock_submodule('rgb_sync', 'RGBSync')
    mock_submodule('quad_mirror', 'QuadMirror')
    mock_submodule('chroma_key', 'ChromaKey')
    mock_submodule('auto_framing', 'AutoFraming')
    mock_submodule('clone_grid', 'CloneGrid')
    mock_submodule('rotating_cube', 'RotatingCube')

    custom_fx.__all__ = [
        'KaleidoscopeCube', 'RGBSync', 'QuadMirror', 'ChromaKey',
        'Kaleidoscope', 'Matrix', 'AutoFraming', 'CloneGrid', 'RotatingCube'
    ]

# Mock ui
if 'ui' not in sys.modules:
    sys.modules['ui'] = MagicMock()
    sys.modules['ui'].DASHBOARD_HTML = "<html></html>"
