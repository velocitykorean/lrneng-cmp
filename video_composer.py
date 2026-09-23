import os
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import config
from audio_visualizer import AudioSpectrumVisualizer

def render_podcast_video(image_path: str, audio_path: str, subtitle_chunks: list, output_video_path: str, fps: int = 30, preview_seconds: float = None) -> str:
    """
    Renders high-quality 1080p podcast video with:
    - Base character background
    - Single-line centered subtitles with active spoken word highlighted in Cyan
    - Dynamic audio spectrum visualizer between microphones
    - Top-right podcast branding
    Directly streams frames into FFmpeg for maximum rendering speed and quality.
    """
    print(f"[VideoComposer] Initializing video render: {output_video_path}...")
    
    # 1. Initialize Visualizer
    print("[VideoComposer] Computing audio spectrum...")
    visualizer = AudioSpectrumVisualizer(audio_path, fps=fps)
    total_frames = visualizer.total_frames
    
    if preview_seconds:
        total_frames = min(total_frames, int(preview_seconds * fps))
        print(f"[VideoComposer] Preview mode active: rendering {total_frames} frames ({preview_seconds:.1f}s)...")

    # 2. Prepare Base Image with Static Branding
    base_img = Image.open(image_path).convert("RGBA")
    if base_img.size != (config.VIDEO_WIDTH, config.VIDEO_HEIGHT):
        base_img = base_img.resize((config.VIDEO_WIDTH, config.VIDEO_HEIGHT), Image.Resampling.LANCZOS)

    # Pre-render top-right podcast logo badge onto static base
    draw_base = ImageDraw.Draw(base_img)
    font_path = config.FONT_PATH if os.path.exists(config.FONT_PATH) else config.FALLBACK_FONT_PATH
    logo_bold = ImageFont.truetype(font_path, 32)
    logo_small = ImageFont.truetype(font_path, 16)
    sub_font = ImageFont.truetype(font_path, config.SUBTITLE_FONT_SIZE)

    logo_x, logo_y = 1660, 50
    draw_base.text((logo_x, logo_y), "ENGLISH", fill=(210, 215, 225, 220), font=logo_small)
    draw_base.text((logo_x, logo_y + 18), "PODCAST", fill=(255, 255, 255, 255), font=logo_bold)
    draw_base.ellipse((logo_x + 160, logo_y + 22, logo_x + 185, logo_y + 47), outline=(255, 255, 255, 220), width=3)
    draw_base.ellipse((logo_x + 167, logo_y + 29, logo_x + 178, logo_y + 40), fill=(0, 229, 255, 240))

    # Pre-calculate space width
    space_bbox = draw_base.textbbox((0, 0), " ", font=sub_font)
    space_width = space_bbox[2] - space_bbox[0]

    # Pre-compute word dimensions for all chunks to maximize per-frame rendering speed
    processed_chunks = []
    for chunk in subtitle_chunks:
        c_words = chunk["words"]
        word_metrics = []
        for w in c_words:
            wb = draw_base.textbbox((0, 0), w["word"], font=sub_font)
            w_w = wb[2] - wb[0]
            word_metrics.append({
                "word": w["word"],
                "start": w["start"],
                "end": w["end"],
                "width": w_w
            })
        total_w = sum(wm["width"] for wm in word_metrics) + max(0, len(word_metrics) - 1) * space_width
        processed_chunks.append({
            "start": chunk["start"],
            "end": chunk["end"],
            "total_width": total_w,
            "words": word_metrics
        })

    # Base RGB image as numpy array for fast copying
    base_rgb = base_img.convert("RGB")

    # 3. Setup FFmpeg Pipeline
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{config.VIDEO_WIDTH}x{config.VIDEO_HEIGHT}",
        "-pix_fmt", "bgr24",
        "-r", str(fps),
        "-i", "-",  # Stdin pipe
        "-i", audio_path,
        "-c:v", "libx264",
        "-preset", "ultrafast",  # Super fast rendering
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_video_path
    ]

    ffmpeg_log_path = os.path.join(config.TEMP_DIR, "ffmpeg.log")
    ffmpeg_log_file = open(ffmpeg_log_path, "w")

    print(f"[VideoComposer] Starting FFmpeg encoding process (ultrafast preset)...")
    proc = subprocess.Popen(
        ffmpeg_cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=ffmpeg_log_file
    )

    print(f"[VideoComposer] Rendering {total_frames} frames ({total_frames/fps:.1f}s)...")
    last_reported_pct = -1

    try:
        for f in range(total_frames):
            t = f / float(fps)

            # Copy base image
            frame = base_rgb.copy()
            draw = ImageDraw.Draw(frame)

            # 1. Render dynamic audio visualizer
            visualizer.draw_frame(draw, f)

            # 2. Render Single-Line Subtitle with Active Word Highlighting
            active_chunk = None
            for c in processed_chunks:
                if c["start"] <= t <= c["end"]:
                    active_chunk = c
                    break

            if active_chunk:
                start_x = (config.VIDEO_WIDTH - active_chunk["total_width"]) // 2
                curr_x = start_x
                sub_y = config.SUBTITLE_Y

                # Find which word is currently being spoken
                active_idx = -1
                for idx, w in enumerate(active_chunk["words"]):
                    if w["start"] <= t <= w["end"]:
                        active_idx = idx
                        break

                # If between words, keep the most recently spoken word highlighted
                if active_idx == -1:
                    for idx, w in enumerate(active_chunk["words"]):
                        if t >= w["end"]:
                            active_idx = idx

                for idx, w in enumerate(active_chunk["words"]):
                    # Highlight active word in Cyan (#00E5FF), others in White (#FFFFFF)
                    if idx == active_idx:
                        color = (0, 229, 255)
                    else:
                        color = (255, 255, 255)

                    # Soft drop shadow for legibility
                    draw.text((curr_x + 2, sub_y + 2), w["word"], fill=(10, 15, 25), font=sub_font)
                    draw.text((curr_x, sub_y), w["word"], fill=color, font=sub_font)

                    curr_x += w["width"] + space_width

            # Convert to BGR bytes and pipe to FFmpeg
            bgr_bytes = np.array(frame)[:, :, ::-1].tobytes()
            proc.stdin.write(bgr_bytes)

            pct = int((f + 1) / total_frames * 100)
            if pct % 10 == 0 and pct != last_reported_pct:
                print(f"  Encoding: {pct}% complete ({f+1}/{total_frames} frames)")
                last_reported_pct = pct

        proc.stdin.close()
        proc.wait()
        ffmpeg_log_file.close()

        file_size_mb = os.path.getsize(output_video_path) / (1024 * 1024)
        print(f"[VideoComposer] Video successfully created: {output_video_path} ({file_size_mb:.2f} MB)")
        return output_video_path

    except Exception as e:
        if proc and proc.stdin:
            try:
                proc.stdin.close()
            except Exception:
                pass
        ffmpeg_log_file.close()
        print(f"[VideoComposer] Error during rendering: {e}")
        raise e
