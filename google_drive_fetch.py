"""
Google Drive Integration & Weighted Asset Selection Module for Learn English Champs
Fetches podcast background images from GOOGLE_DRIVE_FOLDER_ID using Google Service Account.
Supports:
- Priority for new unpublished images
- Infinite circulation mode (Weighted Least-Recently-Used selection)
- Local directory fallback
"""
import os
import io
import json
import glob
import random
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

GOOGLE_DRIVE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID", "1tgPpDbynmPS72m29fvhFSS7ZNPqvmwlb")
GOOGLE_SERVICE_ACCOUNT_KEY = os.getenv("GOOGLE_SERVICE_ACCOUNT_KEY")
LOCAL_IMAGE_DIR = os.getenv("LOCAL_IMAGE_DIR", "input")
PUBLISHED_LOG = "published_videos.json"

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def get_drive_service():
    """Build and return an authorized Google Drive v3 service instance."""
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError:
        print("[DRIVE] google-api-python-client or google-auth not installed.")
        return None

    if not GOOGLE_SERVICE_ACCOUNT_KEY:
        print("[DRIVE] GOOGLE_SERVICE_ACCOUNT_KEY not found in environment.")
        return None

    try:
        key_str = GOOGLE_SERVICE_ACCOUNT_KEY.strip()
        if key_str.startswith('{'):
            info = json.loads(key_str)
            credentials = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
            return build('drive', 'v3', credentials=credentials)
        elif os.path.exists(GOOGLE_SERVICE_ACCOUNT_KEY):
            credentials = service_account.Credentials.from_service_account_file(GOOGLE_SERVICE_ACCOUNT_KEY, scopes=SCOPES)
            return build('drive', 'v3', credentials=credentials)
        else:
            return None
    except Exception as e:
        print(f"[DRIVE ERROR] Failed to initialize Google Drive service: {e}")
        return None

def list_drive_images(folder_id: str):
    """Lists image files inside the specified Google Drive folder."""
    if not folder_id:
        return []
    service = get_drive_service()
    if not service:
        return []
    try:
        query = f"'{folder_id}' in parents and trashed = false"
        results = service.files().list(
            q=query,
            fields="files(id, name, mimeType, size)",
            pageSize=100
        ).execute()
        files = results.get('files', [])
        valid_extensions = ('.png', '.jpg', '.jpeg', '.webp')
        filtered = []
        for f in files:
            name = f.get('name', '').lower()
            if name.endswith(valid_extensions):
                # Filter out accidental screenshot uploads
                if not name.startswith('screenshot') and not name.startswith('image.png'):
                    filtered.append(f)
        # If no filtered images, return all valid extensions
        if not filtered:
            filtered = [f for f in files if f.get('name', '').lower().endswith(valid_extensions)]
        return filtered
    except Exception as e:
        print(f"[DRIVE ERROR] Error listing files in folder {folder_id}: {e}")
        return []

def download_file(file_id: str, dest_path: str) -> bool:
    """Downloads a file from Google Drive."""
    try:
        from googleapiclient.http import MediaIoBaseDownload
    except ImportError:
        return False
    service = get_drive_service()
    if not service:
        return False
    try:
        request = service.files().get_media(fileId=file_id)
        os.makedirs(os.path.dirname(os.path.abspath(dest_path)), exist_ok=True)
        with io.FileIO(dest_path, 'wb') as fh:
            downloader = MediaIoBaseDownload(fh, request, chunksize=10 * 1024 * 1024)
            done = False
            while not done:
                status, done = downloader.next_chunk()
        return True
    except Exception as e:
        print(f"[DRIVE ERROR] Error downloading {file_id}: {e}")
        return False

def get_image_usage_counts():
    """Counts how many times each image has been used from published_videos.json."""
    if os.path.exists(PUBLISHED_LOG):
        try:
            with open(PUBLISHED_LOG, 'r', encoding='utf-8') as f:
                data = json.load(f)
                counts = {}
                for item in data:
                    iname = (item.get("image_name") or item.get("image_file") or "").strip().lower()
                    if iname:
                        counts[iname] = counts.get(iname, 0) + 1
                return counts
        except Exception:
            return {}
    return {}

def select_and_download_image(allow_recirculation: bool = True) -> str:
    """
    Selects an image using Weighted Least-Recently-Used selection:
    1. Checks Google Drive folder.
    2. Selects an unpublished image if available.
    3. If all images have been used, selects the least frequently used image (weighted inverse).
    4. Falls back to local input images if Google Drive is unavailable.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    img_dir = os.path.join(script_dir, LOCAL_IMAGE_DIR)
    os.makedirs(img_dir, exist_ok=True)

    drive_files = list_drive_images(GOOGLE_DRIVE_FOLDER_ID)
    local_imgs = sorted(
        glob.glob(os.path.join(img_dir, "*.png")) +
        glob.glob(os.path.join(img_dir, "*.jpg")) +
        glob.glob(os.path.join(img_dir, "*.jpeg")) +
        glob.glob(os.path.join(img_dir, "*.webp"))
    )

    usage_counts = get_image_usage_counts()
    selected_image_path = None

    if drive_files:
        print(f"[DRIVE] Found {len(drive_files)} images in Google Drive folder.")
        unpublished_drive = [f for f in drive_files if f['name'].strip().lower() not in usage_counts]

        if unpublished_drive:
            # Pick a new, unpublished image
            chosen = unpublished_drive[0]
            print(f"[IMAGE SELECT] Selected NEW unpublished image from Drive: {chosen['name']}")
        elif allow_recirculation:
            # Weighted Least-Recently-Used
            weights = [max(1, 1000 // (3 ** min(usage_counts.get(f['name'].strip().lower(), 0), 6))) for f in drive_files]
            chosen = random.choices(drive_files, weights=weights, k=1)[0]
            used_times = usage_counts.get(chosen['name'].strip().lower(), 0)
            print(f"[IMAGE SELECT] Circulation mode: Selected {chosen['name']} (used {used_times} times before).")
        else:
            chosen = None

        if chosen:
            dest_path = os.path.join(img_dir, chosen['name'])
            if not os.path.exists(dest_path):
                print(f"[DRIVE] Downloading image from Google Drive: {chosen['name']}...")
                success = download_file(chosen['id'], dest_path)
                if success:
                    selected_image_path = dest_path
            else:
                selected_image_path = dest_path

    # Fallback to local images if Drive was unreachable
    if not selected_image_path and local_imgs:
        unpublished_local = [f for f in local_imgs if os.path.basename(f).strip().lower() not in usage_counts]
        if unpublished_local:
            selected_image_path = unpublished_local[0]
        else:
            weights = [max(1, 1000 // (3 ** min(usage_counts.get(os.path.basename(f).strip().lower(), 0), 6))) for f in local_imgs]
            selected_image_path = random.choices(local_imgs, weights=weights, k=1)[0]
        print(f"[IMAGE SELECT] Using local image: {os.path.basename(selected_image_path)}")

    if not selected_image_path:
        raise FileNotFoundError("No image could be selected from Google Drive or local input folder.")

    return selected_image_path

if __name__ == "__main__":
    img_path = select_and_download_image()
    print("Selected Image Path:", img_path)
