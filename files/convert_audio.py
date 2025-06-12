import os
import json
import subprocess
import whisper

def transcribe_audio():
    reels_dir = "reels"
    model = whisper.load_model("medium")

    for slug in os.listdir(reels_dir):
        reel_path = os.path.join(reels_dir, slug)
        metadata_path = os.path.join(reel_path, "metadata.json")

        if not os.path.isfile(metadata_path):
            print(f"Skipping {slug}: metadata.json not found")
            continue

        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)

        video_path = os.path.join(reel_path, metadata["video_path"])
        audio_path = os.path.join(reel_path, metadata["audio_path"])
        transcript_path = os.path.join(reel_path, metadata["audio_transcription_path"])

        if os.path.exists(transcript_path):
            print(f"Transcript already exists for {slug}, skipping.")
            continue

        print(f"\n🎧 Extracting audio from {video_path}...")
        try:
            subprocess.run([
                "ffmpeg", "-i", video_path, "-vn", "-acodec", "pcm_s16le",
                "-ar", "44100", "-ac", "2", audio_path
            ], check=True)
        except subprocess.CalledProcessError:
            print(f"❌ Failed to extract audio for {slug}")
            continue

        print(f"🧠 Transcribing audio for {slug}...")
        try:
            result = model.transcribe(audio_path)
            with open(transcript_path, "w", encoding="utf-8") as f:
                f.write(result["text"])
        except Exception as e:
            print(f"❌ Transcription failed for {slug}: {e}")

        # Clean up audio file
        if os.path.exists(audio_path):
            os.remove(audio_path)

    print("\n✅ Audio transcription complete.")

if __name__ == "__main__":
    transcribe_audio()
