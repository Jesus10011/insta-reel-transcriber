import os
import json
from files.extract_saved_reels import extract_reel_urls
from files.download_reels import download_reels
from files.convert_audio import transcribe_audio
from files.extract_video_text import extract_video_text

def main():
    #extract_reel_urls()
    os.makedirs("reels", exist_ok=True)

    with open("reel_urls.txt", "r") as f:
        urls = [line.strip() for line in f if line.strip()]

    for i, url in enumerate(urls, start=1):
        slug = url.rstrip("/").split("/")[-1]
        reel_folder = os.path.join("reels", slug)
        os.makedirs(reel_folder, exist_ok=True)

        metadata = {
            "reel_id": f"reel_{i:03d}",
            "original_url": url,
            "video_path": f"{i}_.mp4",
            "audio_path": f"{i}_.wav",
            "audio_transcription_path": f"{i}_audio_transcription.txt",
            "video_transcription_path": f"{i}_video_transcription.txt"
        }

        with open(os.path.join(reel_folder, "metadata.json"), "w", encoding="utf-8") as meta_file:
            json.dump(metadata, meta_file, indent=2)

    print(f"Metadata generated for {len(urls)} reels.")

    #download_reels()
    #transcribe_audio()
    #extract_video_text()

if __name__ == "__main__":
    main()
