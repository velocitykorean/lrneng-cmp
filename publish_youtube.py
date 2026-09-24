"""
YouTube Upload, Thumbnail & Playlist Publishing Module for Learn English Champs
Uploads educational English podcast episodes, attaches high-CTR thumbnails,
and automatically adds the video to the channel's "Learn English" playlist.
"""
import os
import sys
import json
import time
from datetime import datetime
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

load_dotenv()

PUBLISHED_LOG = "published_videos.json"

def get_authenticated_youtube_service():
    """Authenticate with YouTube Data API v3 using OAuth refresh token."""
    client_id = (os.getenv('YT_CLIENT_ID') or os.getenv('YOUTUBE_CLIENT_ID', '')).strip()
    client_secret = (os.getenv('YT_CLIENT_SECRET') or os.getenv('YOUTUBE_CLIENT_SECRET', '')).strip()
    refresh_token = (os.getenv('YT_REFRESH_TOKEN') or os.getenv('YOUTUBE_REFRESH_TOKEN', '')).strip()

    if not all([client_id, client_secret, refresh_token]):
        raise ValueError("Missing YouTube credentials! Ensure YT_CLIENT_ID, YT_CLIENT_SECRET, and YT_REFRESH_TOKEN are set.")

    creds = Credentials(
        None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=["https://www.googleapis.com/auth/youtube"]
    )

    try:
        creds.refresh(Request())
    except Exception as e:
        print(f"[YOUTUBE ERROR] Failed to refresh token: {e}")
        raise

    return build('youtube', 'v3', credentials=creds)

def get_or_create_playlist(youtube, playlist_title: str = "Learn English - Full Podcast Lessons") -> str:
    """Finds an existing playlist by title or creates a new public playlist."""
    try:
        req = youtube.playlists().list(part="snippet", mine=True, maxResults=50)
        resp = req.execute()
        for item in resp.get("items", []):
            title = item["snippet"]["title"]
            if playlist_title.lower() in title.lower() or "learn english" in title.lower():
                print(f"[YOUTUBE] Found existing playlist: '{title}' (ID: {item['id']})")
                return item["id"]

        # Create playlist if not found
        print(f"[YOUTUBE] Creating new playlist: '{playlist_title}'...")
        body = {
            "snippet": {
                "title": playlist_title,
                "description": "Daily English learning podcast lessons by Learn English Champs. Master conversational English, overcome fear of speaking, and build fluency."
            },
            "status": {
                "privacyStatus": "public"
            }
        }
        res = youtube.playlists().insert(part="snippet,status", body=body).execute()
        playlist_id = res.get("id")
        print(f"[YOUTUBE] Playlist created successfully! ID: {playlist_id}")
        return playlist_id
    except Exception as e:
        print(f"[YOUTUBE WARNING] Failed to get/create playlist: {e}")
        return None

def add_video_to_playlist(youtube, video_id: str, playlist_id: str):
    """Adds a video to the specified YouTube playlist."""
    if not playlist_id:
        return False
    try:
        print(f"[YOUTUBE] Adding Video {video_id} to Playlist {playlist_id}...")
        body = {
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }
        youtube.playlistItems().insert(part="snippet", body=body).execute()
        print("[YOUTUBE] Video successfully added to playlist!")
        return True
    except Exception as e:
        print(f"[YOUTUBE WARNING] Failed to add video to playlist: {e}")
        return False

def upload_to_youtube(video_path: str, title: str, description: str, tags: list = None, category_id: str = "27", privacy_status: str = "public") -> str:
    """
    Uploads a video to YouTube.
    Category 27 = Education.
    """
    if tags is None:
        tags = [
            "learn english", "english podcast", "learn english champs", "english conversation",
            "overcome fear of speaking english", "speak english fluently", "daily english practice",
            "english vocabulary", "english listening practice", "english lessons"
        ]

    youtube = get_authenticated_youtube_service()

    body = {
        "snippet": {
            "title": title[:100],
            "description": description,
            "tags": tags[:30],
            "categoryId": category_id
        },
        "status": {
            "privacyStatus": privacy_status,
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(
        str(video_path),
        chunksize=10 * 1024 * 1024,
        resumable=True,
        mimetype="video/mp4"
    )

    print(f"[YOUTUBE] Uploading Video: {title}")
    request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            pct = int(status.progress() * 100)
            print(f"  --> Upload progress: {pct}%")

    video_id = response.get("id")
    print(f"[YOUTUBE] Upload Complete! Video ID: {video_id}")
    print(f"[YOUTUBE] Video URL: https://youtu.be/{video_id}")
    return video_id

def set_video_thumbnail(video_id: str, thumbnail_path: str) -> bool:
    """Attaches custom thumbnail image to YouTube video."""
    if not os.path.exists(thumbnail_path):
        print(f"[YOUTUBE] Thumbnail file not found: {thumbnail_path}")
        return False

    youtube = get_authenticated_youtube_service()
    print(f"[YOUTUBE] Setting custom thumbnail for Video ID: {video_id}...")
    try:
        media = MediaFileUpload(str(thumbnail_path), mimetype="image/png")
        youtube.thumbnails().set(videoId=video_id, media_body=media).execute()
        print("[YOUTUBE] Thumbnail successfully set!")
        return True
    except Exception as e:
        print(f"[YOUTUBE] Failed to set thumbnail: {e}")
        return False

def log_published_video(video_id: str, title: str, image_name: str, duration_sec: float, topic: str, playlist_id: str = None):
    """Logs the published video to published_videos.json for history and weighted selection."""
    log_data = []
    if os.path.exists(PUBLISHED_LOG):
        try:
            with open(PUBLISHED_LOG, "r", encoding="utf-8") as f:
                log_data = json.load(f)
        except Exception:
            log_data = []

    log_data.append({
        "video_id": video_id,
        "title": title,
        "image_name": os.path.basename(image_name),
        "duration_seconds": round(duration_sec, 2),
        "topic": topic,
        "playlist_id": playlist_id,
        "timestamp": datetime.now().isoformat(),
        "url": f"https://youtu.be/{video_id}"
    })

    with open(PUBLISHED_LOG, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=2, ensure_ascii=False)
    print(f"[LOG] Appended publication log to {PUBLISHED_LOG}")
