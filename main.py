import os
import sys

# Ensure current script directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import argparse
import asyncio
from datetime import datetime
import config
from story_generator import generate_story
from tts_engine import generate_podcast_audio
from thumbnail_generator import generate_thumbnail
from video_composer import render_podcast_video

def run_pipeline(
    image_path: str = None,
    topic: str = None,
    num_turns: int = 6,
    output_video_path: str = None,
    output_thumbnail_path: str = None,
    preview_seconds: float = None
):
    print("=" * 65)
    print("      AUTOMATED ENGLISH PODCAST VIDEO GENERATOR")
    print("=" * 65)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 1. Resolve image
    if not image_path:
        image_path = config.DEFAULT_IMAGE_PATH
    if not os.path.exists(image_path):
        print(f"Error: Input image not found: {image_path}")
        sys.exit(1)

    print(f"[Step 1/4] Using character scene image:\n  {image_path}")

    # 2. Generate Story / Dialogue
    print(f"\n[Step 2/4] Generating English Learning Dialogue...")
    story = generate_story(topic=topic, num_turns=num_turns)
    print(f"  Topic: {story.get('topic')}")
    print(f"  Turns: {len(story.get('dialogue', []))}")

    # 3. Generate Audio & Subtitle Timing
    print(f"\n[Step 3/4] Synthesizing Natural Voices & Word Timings...")
    master_audio_path, subtitle_chunks, total_duration = asyncio.run(
        generate_podcast_audio(story["dialogue"])
    )
    print(f"  Total Audio Duration: {total_duration:.2f} seconds")
    print(f"  Single-Line Subtitle Chunks: {len(subtitle_chunks)}")

    # 4. Generate Thumbnail
    if not output_thumbnail_path:
        output_thumbnail_path = os.path.join(config.OUTPUT_DIR, f"thumbnail_{timestamp}.png")
    
    title_1 = story.get("thumbnail_title_1", "SPEAK ENGLISH")
    title_2 = story.get("thumbnail_title_2", "LIKE A NATIVE!")
    hook = story.get("thumbnail_hook", "Daily English Practice")
    
    print(f"\n[Step 4/5] Creating High-CTR YouTube Thumbnail...")
    generate_thumbnail(
        image_path=image_path,
        title_1=title_1,
        title_2=title_2,
        hook=hook,
        output_path=output_thumbnail_path
    )

    # 5. Render Video
    if not output_video_path:
        output_video_path = os.path.join(config.OUTPUT_DIR, f"podcast_video_{timestamp}.mp4")

    print(f"\n[Step 5/5] Rendering 1080p Video (Single-line highlighted subtitles + dynamic visualizer)...")
    final_video = render_podcast_video(
        image_path=image_path,
        audio_path=master_audio_path,
        subtitle_chunks=subtitle_chunks,
        output_video_path=output_video_path,
        fps=config.VIDEO_FPS,
        preview_seconds=preview_seconds
    )

    print("\n" + "=" * 65)
    print("            GENERATION COMPLETE!")
    print("=" * 65)
    print(f"Final Video:     {final_video}")
    print(f"Final Thumbnail: {output_thumbnail_path}")
    print(f"Master Audio:    {master_audio_path}")
    print("=" * 65)

    return {
        "video_path": final_video,
        "thumbnail_path": output_thumbnail_path,
        "audio_path": master_audio_path,
        "duration": total_duration,
        "topic": story.get("topic")
    }

def main():
    parser = argparse.ArgumentParser(description="Automated English Learning Podcast Video Generator")
    parser.add_argument("--image", type=str, default=None, help="Path to character scene image")
    parser.add_argument("--topic", type=str, default=None, help="English learning topic")
    parser.add_argument("--turns", type=int, default=6, help="Number of dialogue turns (default: 6)")
    parser.add_argument("--output", type=str, default=None, help="Output MP4 path")
    parser.add_argument("--thumbnail", type=str, default=None, help="Output thumbnail PNG path")
    parser.add_argument("--preview", type=float, default=None, help="Preview mode: seconds to render")

    args = parser.parse_args()
    run_pipeline(
        image_path=args.image,
        topic=args.topic,
        num_turns=args.turns,
        output_video_path=args.output,
        output_thumbnail_path=args.thumbnail,
        preview_seconds=args.preview
    )

if __name__ == "__main__":
    main()
