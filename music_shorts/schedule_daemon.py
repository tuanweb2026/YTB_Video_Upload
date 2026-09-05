#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
15-Minute Interval Auto-Pilot Music Shorts Poster
Uploads 1 Short video every 15 minutes to @1995lido (Thảo Dương TV) until all 31 are posted.
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime
from pathlib import Path

BASE_DIR = Path("/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management")
SHORTS_DIR = Path("/Users/abc/.gemini/antigravity/scratch/music_shorts")
CONFIG_FILE = SHORTS_DIR / "all_31_configs.json"
PROGRESS_FILE = SHORTS_DIR / "schedule_15min_progress.json"
DAEMON_LOG = SHORTS_DIR / "schedule_daemon.log"

sys.path.insert(0, str(BASE_DIR))
import yt_upload

FFMPEG = "/Users/abc/bin/ffmpeg"
YT_DLP = "/Users/abc/Library/Python/3.9/bin/yt-dlp"
INTERVAL_SECONDS = 15 * 60  # 15 phút = 900 giây

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    try:
        with open(DAEMON_LOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass

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

def process_one_video(item, tokens):
    vid_id = item["id"]
    title = item["title"]
    long_url = item["long_url"]
    start = item["start"]
    end = item["end"]
    genre = item["genre"]

    temp_full = SHORTS_DIR / f"temp_{vid_id}.mp4"
    out_short = SHORTS_DIR / f"short_{vid_id}.mp4"

    try:
        log(f"📥 1/3. Đang tải video nguồn ({vid_id})...")
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
            log(f"⚠️ Thử tải lần {attempt} thất bại, thử lại sau 3s...")
            time.sleep(3)

        if not dl_success:
            log(f"❌ Không tải được video {vid_id}, bỏ qua.")
            return None

        log(f"✂️ 2/3. Đang cắt đoạn cao trào {start} -> {end} và chuyển tỉ lệ dọc 9:16...")
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
        log(f"✅ Đã tạo video Shorts ({size_mb:.1f} MB)")

        log(f"📤 3/3. Đang upload lên kênh Thảo Dương TV (Public)...")
        desc = make_description(long_url, genre)
        tags = ["Shorts", "ThaoDuongTV", "Music", genre]

        # Lấy token mới nhất
        current_tokens = yt_upload.get_tokens() or tokens

        uploaded_id, err = yt_upload.upload_one(
            filepath=str(out_short),
            title=title,
            description=desc,
            tags=tags,
            privacy="public",
            tokens=current_tokens
        )

        if uploaded_id:
            yt_url = f"https://www.youtube.com/watch?v={uploaded_id}"
            log(f"🎉 THÀNH CÔNG! Link: {yt_url}")
            return {
                "uploaded_id": uploaded_id,
                "url": yt_url,
                "title": title,
                "status": "success",
                "timestamp": time.time(),
                "time_str": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        else:
            log(f"❌ Lỗi upload: {err}")
            return None

    except Exception as e:
        log(f"❌ Ngoại lệ: {e}")
        return None
    finally:
        if temp_full.exists():
            temp_full.unlink()
        if out_short.exists():
            out_short.unlink()
        log("🧹 Đã dọn dẹp file tạm.")

def main():
    log("🚀 KHỞI ĐỘNG TIẾN TRÌNH ĐĂNG SHORTS CÁCH NHAU 15 PHÚT MỖI BÀI")
    
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        configs = json.load(f)

    progress = load_progress()
    tokens = yt_upload.get_tokens()

    for idx, item in enumerate(configs, 1):
        vid_id = item["id"]
        title = item["title"]

        # Kiểm tra nếu bài này đã được đăng trong tiến trình 15 phút này chưa
        if vid_id in progress and progress[vid_id].get("status") == "success":
            log(f"[{idx}/{len(configs)}] ĐÃ ĐĂNG TRƯỚC ĐÓ: {title} -> {progress[vid_id]['url']}")
            continue

        log(f"\n{'='*70}\n[{idx}/{len(configs)}] TIẾN HÀNH ĐĂNG BÀI: {title}\n{'='*70}")
        result = process_one_video(item, tokens)

        if result:
            progress[vid_id] = result
            save_progress(progress)
            
            # Kiểm tra xem còn video nào chưa đăng không
            remaining = [v for v in configs if v["id"] not in progress or progress[v["id"]].get("status") != "success"]
            if not remaining:
                log("🎉 ĐÃ ĐĂNG HOÀN TẤT TOÀN BỘ 31 VIDEO SHORTS! KẾT THÚC.")
                break

            log(f"⏳ Đang nghỉ 15 phút ({INTERVAL_SECONDS} giây) trước khi đăng bài tiếp theo...")
            time.sleep(INTERVAL_SECONDS)
        else:
            log("⚠️ Đăng bài thất bại, sẽ thử lại sau 30 giây...")
            time.sleep(30)

if __name__ == "__main__":
    main()
