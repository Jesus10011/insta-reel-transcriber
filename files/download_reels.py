import os
import json
import yt_dlp

def download_reels():
    # Read URLs
    with open("reel_urls.txt", "r") as file:
        urls = [line.strip() for line in file if line.strip()]

    # Download each reel
    for i, url in enumerate(urls, start=1):
        slug = url.rstrip("/").split("/")[-1]
        reel_folder = os.path.join("reels", slug)
        metadata_path = os.path.join(reel_folder, "metadata.json")

        if not os.path.exists(metadata_path):
            print(f"⚠️ Missing metadata.json for reel {slug}, skipping.")
            continue

        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)

        output_path = os.path.join(reel_folder, metadata["video_path"])

        ydl_opts = {
            'outtmpl': output_path,
            'format': 'mp4/bestvideo+bestaudio',
            'merge_output_format': 'mp4',
            'quiet': False,
            'noplaylist': True,
            'ignoreerrors': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"[{i}/{len(urls)}] Downloading: {url} → {output_path}")
            try:
                ydl.download([url])
            except Exception as e:
                print(f"⚠️ Failed to download {url}: {e}")

    print("✅ All downloads completed.")
