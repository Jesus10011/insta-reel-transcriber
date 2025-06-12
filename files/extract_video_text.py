import os
import json
import cv2
import pytesseract

def extract_video_text():
    reels_dir = "reels"

    for slug in os.listdir(reels_dir):
        reel_path = os.path.join(reels_dir, slug)
        metadata_path = os.path.join(reel_path, "metadata.json")

        if not os.path.isfile(metadata_path):
            print(f"Skipping {slug}: metadata.json not found")
            continue

        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)

        video_path = os.path.join(reel_path, metadata["video_path"])
        output_text_path = os.path.join(reel_path, metadata["video_transcription_path"])

        if os.path.exists(output_text_path):
            print(f"📄 Text already extracted for {slug}, skipping.")
            continue

        print(f"\n🖼️  Processing video frames for {slug}...")

        cap = cv2.VideoCapture(video_path)
        success, frame_count, text_blocks = True, 0, []

        while success:
            cap.set(cv2.CAP_PROP_POS_MSEC, frame_count * 1000)  # 1 frame per second
            success, frame = cap.read()
            if not success:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(gray)
            cleaned_text = text.strip()

            if cleaned_text:
                text_blocks.append(cleaned_text)

            frame_count += 1

        cap.release()

        if text_blocks:
            with open(output_text_path, "w", encoding="utf-8") as f:
                f.write("\n\n".join(text_blocks))
            print(f"✅ OCR complete for {slug}, text saved.")
        else:
            print(f"⚠️  No readable text found in video for {slug}")


if __name__ == "__main__":
    extract_video_text()
