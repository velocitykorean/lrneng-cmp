# 🎙️ Automated English Learning Podcast Video & Thumbnail Generator

An automated AI pipeline that transforms a 2-character podcast scene image into a full-fledged, broadcast-ready 1080p English learning video and YouTube thumbnail.

Designed specifically for educational English learning YouTube channels, matching the high-engagement style of popular conversational podcast series.

---

## 🌟 Key Features

1. **AI Dialogue Generation (Pollinations AI)**:
   - Automatically writes lively, engaging English learning conversations between two hosts (Emma & Alex).
   - Explains real-world idioms, natural phrasing, pronunciation, and common mistakes.
   - Built-in curated scripts fallback for 100% offline reliability.

2. **Ultra-Realistic Microsoft Neural Voices (`edge-tts`)**:
   - Expressive female (`en-US-JennyNeural`) and male (`en-US-GuyNeural`) conversational voices.
   - Precise millisecond word-level timing captured via `boundary="WordBoundary"`.

3. **Pixel-Perfect Single-Line Subtitles with Word Highlighting**:
   - Positioned in the upper-center gap space (matching reference layout).
   - **Strictly single-line** display (3-6 words per chunk) to eliminate clutter and maximize readability on mobile and desktop.
   - **Active Spoken Word Highlighting**: As the host speaks each word, that specific word lights up in vibrant Cyan (`#00E5FF`), while unsaid words remain crisp White (`#FFFFFF`).

4. **Dynamic Audio Spectrum Visualizer**:
   - Centered between the microphones at the bottom.
   - 42 rounded bars reacting in real time to speech frequencies via Short-Time FFT.
   - Smooth attack/decay filter so the waveform bounces naturally and rests cleanly during speech pauses.

5. **High-CTR YouTube Thumbnail Generator**:
   - Utilizes the spacious gap in the center of the image.
   - Adds soft glowing radial lighting, episode badge pill, high-contrast multi-colored title with heavy outlines and drop-shadows, and a catchy topic hook.

6. **Direct FFmpeg Pipe Streaming**:
   - Zero temporary video frames written to disk.
   - Renders at 30-60+ fps directly into H.264 + AAC MP4.

---

## 📁 Project Structure

```text
E english podcast generator/
├── config.py                 # Central configuration (fonts, colors, coordinates, voices)
├── story_generator.py        # Pollinations AI English learning script generator
├── tts_engine.py             # edge-tts synthesis & word-level timing chunker
├── audio_visualizer.py       # Audio FFT analysis and animated spectrum renderer
├── video_composer.py         # FFmpeg video renderer with active word highlighting
├── thumbnail_generator.py    # High-CTR YouTube thumbnail generator
├── main.py                   # Master pipeline CLI
├── Launch_Generator.bat      # 1-Click launcher for Windows
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── .gitignore                # Git ignore rules
├── assets/                   # Fonts, logos, badges
├── input/                    # Character scene images (podcast_scene.png)
└── output/                   # Rendered MP4 videos and PNG thumbnails
```

---

## 🚀 Quick Start

### 1. Requirements
Ensure you have Python 3.10+ and FFmpeg installed and in your PATH.

Install Python dependencies:
```bash
pip install -r requirements.txt
```

### 2. Run the Generator
To generate a video and thumbnail using the default image:
```bash
python main.py
```
Or double-click `Launch_Generator.bat`.

### 3. Custom Topic or Custom Image
```bash
python main.py --image "input/podcast_scene.png" --topic "Common English Idioms for Work" --turns 6
```

### 4. Fast Preview Mode
Render only the first 5 seconds to inspect visual styling quickly:
```bash
python main.py --preview 5
```

---

## 🎨 Visual Styling Specs

| Element | Specification |
| :--- | :--- |
| **Resolution** | 1920 x 1080 (1080p Full HD, 16:9) |
| **Subtitle Position** | Upper-Center (`Y = 310`), centered between hosts |
| **Active Word Color** | `#00E5FF` (Vibrant Cyan / Teal) |
| **Normal Word Color** | `#FFFFFF` (Crisp Pure White) |
| **Visualizer Position** | Lower-Center (`Y = 920`, `X = 960`), between mic stands |
| **Visualizer Style** | 42 rounded bars, dynamic FFT response, minimal idle dots |
| **Thumbnail** | Center gap aura + 3D stroke typography + episode badge pill |
