import os

# Project root directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Subdirectories
INPUT_DIR = os.path.join(BASE_DIR, "input")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
TEMP_DIR = os.path.join(BASE_DIR, "temp")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

for d in [INPUT_DIR, OUTPUT_DIR, TEMP_DIR, ASSETS_DIR]:
    os.makedirs(d, exist_ok=True)

# Default base scene image
DEFAULT_IMAGE_PATH = os.path.join(INPUT_DIR, "podcast_scene.png")

# Video settings
VIDEO_WIDTH = 1920
VIDEO_HEIGHT = 1080
VIDEO_FPS = 30

# Subtitle settings
SUBTITLE_Y = 310          # Centered horizontally, at Y=310 (upper-center gap)
SUBTITLE_FONT_SIZE = 52
FONT_PATH = r"C:\Windows\Fonts\arialbd.ttf"
FALLBACK_FONT_PATH = r"C:\Windows\Fonts\arial.ttf"

# Colors (R, G, B, A)
COLOR_TEXT_NORMAL = (255, 255, 255, 255)       # Crisp White
COLOR_TEXT_HIGHLIGHT = (0, 229, 255, 255)      # Vibrant Cyan / Teal (#00E5FF)
COLOR_TEXT_SHADOW = (10, 15, 25, 200)          # Soft dark shadow

# Visualizer settings (Audio Waveform)
VIS_CENTER_X = 960         # Centered horizontally between the microphones
VIS_BASE_Y = 920           # Y coordinate level with mic stands
VIS_NUM_BARS = 42          # Number of bars across spectrum
VIS_BAR_WIDTH = 4          # Thickness of each bar
VIS_BAR_SPACING = 10       # Spacing between bars
VIS_MIN_HEIGHT = 4         # Dot/rest height during pauses
VIS_MAX_HEIGHT = 50        # Peak height during speech
VIS_COLOR = (245, 245, 245, 235)  # Slightly translucent white

# TTS Settings (Microsoft Natural Neural Voices)
VOICE_FEMALE = "en-US-JennyNeural"    # Expressive, natural female voice
VOICE_MALE = "en-US-GuyNeural"        # Warm, friendly male voice
TTS_RATE = "+0%"
PAUSE_BETWEEN_TURNS = 0.45            # Natural conversational pause in seconds

# Subtitle formatting
MAX_WORDS_PER_LINE = 6                # Strictly single-line subtitles (3-6 words per chunk)

# Pollinations AI settings
POLLINATIONS_API_KEY = os.environ.get("POLLINATIONS_API_KEY", "")
POLLINATIONS_ENDPOINT = "https://text.pollinations.ai/openai/chat/completions"
POLLINATIONS_MODEL = "openai"
