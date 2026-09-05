#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Robust Batch Pipeline: Download -> Cut 9:16 -> Upload to YouTube (Thao Duong TV) -> Clean up temp files
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path

BASE_DIR = Path("/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management")
SHORTS_DIR = Path("/Users/abc/.gemini/antigravity/scratch/music_shorts")
CONFIG_FILE = SHORTS_DIR / "all_31_configs.json"
PROGRESS_FILE = SHORTS_DIR / "upload_progress.json"

sys.path.insert(0, str(BASE_DIR))
import yt_upload

FFMPEG = "/Users/abc/bin/ffmpeg"
YT_DLP = "/Users/abc/Library/Python/3.9/bin/yt-dlp"

def load_progress():
    if PROGRESS_FILE.exists():
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_progress(prog):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(prog, f, ensure_ascii=False, indent=2)

def make_description(long_url, genre):
    clean_genre = genre.replace(" ", "")
    return f"""🎵 Nếu bạn nghe hay thì hãy nghe video dài đầy đủ tại link: {long_url}
👉 Đăng ký kênh Thảo Dương TV để thưởng thức thêm nhiều ca khúc & bản phối tuyệt vời: https://www.youtube.com/@1995lido

Cảm ơn các bạn đã lắng nghe và ủng hộ kênh! Chúc bạn có những phút giây thư giãn tuyệt vời. ✨🎶
#ThaoDuongTV #Shorts #Music #AmNhacMoiNgay #{clean_genre}"""

def main():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        configs = json.load(f)

    progress = load_progress()
    print(f"Total videos in queue: {len(configs)}")
    tokens = yt_upload.get_tokens()

    success_count = len([k for k, v in progress.items() if v.get("status") == "success"])

    for i, item in enumerate(configs, 1):
        vid_id = item["id"]
        title = item["title"]
        long_url = item["long_url"]
        start = item["start"]
        end = item["end"]
        genre = item["genre"]

        if vid_id in progress and progress[vid_id].get("status") == "success":
            print(f"[{i}/{len(configs)}] SKIPPED (Already uploaded): {title} -> {progress[vid_id]['url']}")
            continue

        print(f"\n{'='*70}\n[{i}/{len(configs)}] BẮT ĐẦU: {title}\n{'='*70}", flush=True)

        temp_full = SHORTS_DIR / f"temp_{vid_id}.mp4"
        out_short = SHORTS_DIR / f"short_{vid_id}.mp4"

        try:
            # 1. Download with retries
            print(f"📥 1/3. Đang tải video nguồn ({vid_id})...", flush=True)
            dl_success = False
            for attempt in range(1, 4):
                dl_cmd = [
                    YT_DLP,
                    "--extractor-args", "youtube:player_client=android",
                    "-f", "18/best",
                    "-o", str(temp_full),
                    f"https://www.youtube.com/watch?v={vid_id}"
                ]
                res = subprocess.run(dl_cmd)
                if res.returncode == 0 and temp_full.exists() and temp_full.stat().st_size > 100000:
                    dl_success = True
                    break
                print(f"⚠️ Tải lần {attempt} không thành công, thử lại sau 3s...", flush=True)
                time.sleep(3)

            if not dl_success:
                print(f"❌ Không tải được video {vid_id}, bỏ qua.", flush=True)
                continue

            # 2. Cut & Convert to 9:16 (1080x1920)
            print(f"✂️ 2/3. Đang cắt đoạn cao trào {start} -> {end} và chuyển tỉ lệ dọc 9:16...", flush=True)
            ff_cmd = [
                FFMPEG, "-y",
                "-ss", start,
                "-to", end,
                "-i", str(temp_full),
                "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
                "-c:v", "libx264", "-preset", "fast", "-crf", "22",
                "-c:a", "aac", "-b:a", "192k",
                str(out_short)
            ]
            subprocess.run(ff_cmd, check=True)
            size_mb = out_short.stat().st_size / 1024 / 1024
            print(f"✅ Đã tạo video Shorts ({size_mb:.1f} MB)", flush=True)

            # 3. Upload to YouTube
            print(f"📤 3/3. Đang upload lên kênh Thảo Dương TV (Public)...", flush=True)
            desc = make_description(long_url, genre)
            tags = ["Shorts", "ThaoDuongTV", "Music", genre]

            uploaded_id, err = yt_upload.upload_one(
                filepath=str(out_short),
                title=title,
                description=desc,
                tags=tags,
                privacy="public",
                tokens=tokens
            )

            if uploaded_id:
                yt_url = f"https://www.youtube.com/watch?v={uploaded_id}"
                print(f"🎉 THÀNH CÔNG! Link: {yt_url}", flush=True)
                progress[vid_id] = {
                    "uploaded_id": uploaded_id,
                    "url": yt_url,
                    "title": title,
                    "status": "success",
                    "timestamp": time.time()
                }
                save_progress(progress)
                success_count += 1
            else:
                print(f"❌ Lỗi upload: {err}", flush=True)
                if "quotaExceeded" in str(err) or "rateLimit" in str(err):
                    print("⚠️ Đã chạm giới hạn quota API trong ngày của YouTube. Tạm dừng batch.", flush=True)
                    break

        except Exception as e:
            print(f"❌ Exception: {e}", flush=True)
        finally:
            if temp_full.exists():
                temp_full.unlink()
            if out_short.exists():
                out_short.unlink()
            print("🧹 Đã dọn dẹp file tạm.", flush=True)

        time.sleep(3)

    print(f"\n==========================================")
    print(f"HOÀN TẤT BATCH! Tổng số video đã tải lên: {success_count}/{len(configs)}")
    print(f"==========================================")

if __name__ == "__main__":
    main()
