"""
Master Automation Pipeline for Learn English Champs
Executes the full automated workflow:
1. Selects & downloads character scene image from Google Drive via Weighted Least-Recently-Used selection.
2. Generates comprehensive multi-chapter English learning podcast story.
3. Synthesizes Microsoft Neural voices (Emma & Alex) with millisecond word timestamps.
4. Creates high-CTR YouTube thumbnail in the center gap space.
5. Renders 1080p 30fps MP4 video with single-line active-word-highlighted subtitles and audio visualizer.
6. Uploads video to YouTube, sets thumbnail, adds to 'Learn English' playlist, and logs to published_videos.json.
"""
import os
import sys
import argparse
import asyncio
from datetime import datetime

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Ensure UTF-8 stdout encoding on Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import config
from google_drive_fetch import select_and_download_image
from story_generator import generate_full_podcast_story, generate_youtube_metadata
from tts_engine import generate_podcast_audio
from thumbnail_generator import generate_thumbnail
from video_composer import render_podcast_video
from publish_youtube import upload_to_youtube, set_video_thumbnail, get_or_create_playlist, add_video_to_playlist, log_published_video, get_authenticated_youtube_service

def run_auto_pipeline(target_minutes: float = 30.0, topic: str = None, dry_run: bool = False, preview_seconds: float = None):
    print("=" * 70)
    print("    [PODCAST] LEARN ENGLISH CHAMPS - AUTOMATED PIPELINE")
    print("=" * 70)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ep_num = 1
    if os.path.exists("published_videos.json"):
        try:
            import json
            with open("published_videos.json", "r", encoding="utf-8") as f:
                history = json.load(f)
                ep_num = len(history) + 1
        except Exception:
            ep_num = 1

    # ----------------------------------------------------
    # Step 1: Select & Download Image from Google Drive
    # ----------------------------------------------------
    print(f"\n[Step 1/6] Selecting Podcast Scene Image (Google Drive / Weighted LRU)...")
    try:
        image_path = select_and_download_image(allow_recirculation=True)
    except Exception as e:
        print(f"[ERROR] Failed to select image from Google Drive: {e}")
        image_path = config.DEFAULT_IMAGE_PATH
        print(f"Falling back to default image: {image_path}")

    print(f"  Selected Image: {os.path.basename(image_path)}")

    # ----------------------------------------------------
    # Step 2: Generate English Learning Dialogue & Chapters
    # ----------------------------------------------------
    print(f"\n[Step 2/6] Generating Podcast Dialogue (Target: {target_minutes:.1f} minutes)...")
    story = generate_full_podcast_story(target_minutes=target_minutes, topic=topic)
    print(f"  Episode Topic: {story['topic']}")
    print(f"  Total Dialogue Turns: {len(story['dialogue'])}")
    print(f"  Chapters Planned: {len(story['chapters'])}")

    # ----------------------------------------------------
    # Step 3: Synthesize Speech & Word Timings
    # ----------------------------------------------------
    print(f"\n[Step 3/6] Synthesizing Microsoft Neural Voices & Word Timings...")
    master_audio_path, subtitle_chunks, total_duration = asyncio.run(
        generate_podcast_audio(story["dialogue"])
    )
    print(f"  Total Audio Duration: {total_duration:.2f}s ({total_duration/60.0:.1f} mins)")
    print(f"  Single-Line Subtitle Chunks: {len(subtitle_chunks)}")

    # Calculate chapter timestamps for YouTube description
    chapters_with_timestamps = []
    for ch in story["chapters"]:
        start_turn_idx = ch["start_turn"]
        ch_time = 0.0
        if start_turn_idx > 0 and start_turn_idx < len(story["dialogue"]):
            for chunk in subtitle_chunks:
                if chunk.get("turn_idx", -1) == start_turn_idx:
                    ch_time = chunk["start"]
                    break
        chapters_with_timestamps.append({
            "title": ch["title"],
            "start_time": ch_time
        })

    # ----------------------------------------------------
    # Step 4: Create High-CTR YouTube Thumbnail
    # ----------------------------------------------------
    print(f"\n[Step 4/6] Creating High-CTR YouTube Thumbnail...")
    thumbnail_path = os.path.join(config.OUTPUT_DIR, f"thumbnail_ep{ep_num}_{timestamp}.png")
    generate_thumbnail(
        image_path=image_path,
        title_1=story.get("thumbnail_title_1", "SPEAK ENGLISH"),
        title_2=story.get("thumbnail_title_2", "WITHOUT FEAR!"),
        hook=story.get("thumbnail_hook", "Overcome Shyness & Speak Fluently"),
        output_path=thumbnail_path,
        ep_number=ep_num
    )

    # ----------------------------------------------------
    # Step 5: Render 1080p Video (Single-line highlighted text + visualizer)
    # ----------------------------------------------------
    print(f"\n[Step 5/6] Rendering 1080p Video via FFmpeg Pipe...")
    video_path = os.path.join(config.OUTPUT_DIR, f"podcast_ep{ep_num}_{timestamp}.mp4")
    render_podcast_video(
        image_path=image_path,
        audio_path=master_audio_path,
        subtitle_chunks=subtitle_chunks,
        output_video_path=video_path,
        fps=config.VIDEO_FPS,
        preview_seconds=preview_seconds
    )

    # ----------------------------------------------------
    # Step 6: Publish to YouTube & Add to Playlist
    # ----------------------------------------------------
    print(f"\n[Step 6/6] Publishing to YouTube Channel 'Learn English Champs'...")
    yt_meta = generate_youtube_metadata(
        topic=story["topic"],
        duration_sec=total_duration,
        chapters_with_timestamps=chapters_with_timestamps
    )

    if dry_run:
        print("[DRY RUN] Skipping YouTube upload. Video & thumbnail generated successfully!")
        video_id = "DRY_RUN_ID"
        playlist_id = "DRY_RUN_PLAYLIST"
    else:
        try:
            yt = get_authenticated_youtube_service()
            video_id = upload_to_youtube(
                video_path=video_path,
                title=yt_meta["title"],
                description=yt_meta["description"],
                tags=yt_meta["tags"],
                category_id="27",
                privacy_status="public"
            )

            # Set thumbnail
            set_video_thumbnail(video_id, thumbnail_path)

            # Add to 'Learn English' Playlist
            playlist_id = get_or_create_playlist(yt, playlist_title="Learn English - Full Podcast Lessons")
            if playlist_id:
                add_video_to_playlist(yt, video_id, playlist_id)

            # Log to history
            log_published_video(
                video_id=video_id,
                title=yt_meta["title"],
                image_name=image_path,
                duration_sec=total_duration,
                topic=story["topic"],
                playlist_id=playlist_id
            )
            print(f"\n[SUCCESS] Successfully published Episode #{ep_num} to YouTube!")
            print(f"   URL: https://youtu.be/{video_id}")
        except Exception as e:
            print(f"[YOUTUBE ERROR] Failed to upload or update playlist: {e}")
            video_id = None
            playlist_id = None

    print("\n" + "=" * 70)
    print("                 PIPELINE RUN COMPLETE!")
    print("=" * 70)
    print(f"Video File:      {video_path}")
    print(f"Thumbnail File:  {thumbnail_path}")
    print(f"Master Audio:    {master_audio_path}")
    if video_id and video_id != "DRY_RUN_ID":
        print(f"YouTube URL:     https://youtu.be/{video_id}")
    print("=" * 70)

    return {
        "video_path": video_path,
        "thumbnail_path": thumbnail_path,
        "video_id": video_id,
        "duration": total_duration
    }

def main():
    parser = argparse.ArgumentParser(description="Learn English Champs Daily Auto-Pipeline")
    parser.add_argument("--duration", type=float, default=30.0, help="Target duration in minutes (default: 30.0)")
    parser.add_argument("--topic", type=str, default=None, help="Custom topic for English podcast")
    parser.add_argument("--dry-run", action="store_true", help="Generate video & thumbnail without uploading to YouTube")
    parser.add_argument("--preview", type=float, default=None, help="Preview mode: render only N seconds of video")

    args = parser.parse_args()
    run_auto_pipeline(
        target_minutes=args.duration,
        topic=args.topic,
        dry_run=args.dry_run,
        preview_seconds=args.preview
    )

if __name__ == "__main__":
    main()
