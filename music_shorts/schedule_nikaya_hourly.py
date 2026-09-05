#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scheduler: Upload 8 Nikaya Shorts, 1 video per hour (60 minutes interval).
Calculates the exact scheduled target time for each episode based on starting hour,
so even if process restarts, it sleeps only until the exact target time.
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime
sys.path.append("/Users/abc/Library/Python/3.9/lib/python/site-packages")
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path("/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management")
SHORTS_DIR = Path("/Users/abc/.gemini/antigravity/scratch/music_shorts")
DATA_FILE = SHORTS_DIR / "nikaya_shorts_data.json"
SCHEDULE_PROGRESS = SHORTS_DIR / "nikaya_schedule_progress.json"

sys.path.insert(0, str(BASE_DIR))
import yt_upload

FFMPEG = "/Users/abc/bin/ffmpeg"
EDGE_TTS = "/Users/abc/Library/Python/3.9/bin/edge-tts"

# Start base timestamp: Tập 1 bắt đầu lúc 12:53:40
BASE_START_TIMESTAMP = 1788587620  # ~12:53:40 Ngày 05/09/2026
INTERVAL_SECONDS = 3600            # 1 hour per video

def create_title_card(base_img_path, title_lines, series_tag, output_path):
    img = Image.open(base_img_path).convert("RGBA")
    img = img.resize((1080, 1920), Image.Resampling.LANCZOS)
    W, H = img.size

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    card_top = int(H * 0.18)
    card_bottom = int(H * 0.42)
    card_left = int(W * 0.08)
    card_right = int(W * 0.92)

    draw.rounded_rectangle([card_left, card_top, card_right, card_bottom], radius=24, fill=(15, 23, 42, 215), outline=(255, 215, 0, 200), width=3)

    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", index=1, size=48)
        font_brand = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", index=1, size=24)
        font_sub = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", index=0, size=26)
    except Exception:
        font_title = ImageFont.load_default()
        font_brand = font_title
        font_sub = font_title

    draw.rounded_rectangle([card_left + 24, card_top + 24, card_left + 320, card_top + 64], radius=12, fill=(217, 119, 6, 230))
    draw.text((card_left + 36, card_top + 28), f"🌸 {series_tag}", fill=(255, 255, 255), font=font_brand)

    lines = title_lines.split("\n")
    y_text = card_top + 90
    for line in lines:
        draw.text((card_left + 28, y_text), line, fill=(255, 255, 255), font=font_title)
        y_text += 58

    draw.line([(card_left + 24, card_bottom - 60), (card_right - 24, card_bottom - 60)], fill=(255, 215, 0, 120), width=1)
    draw.text((card_left + 28, card_bottom - 46), "🔔 Bấm Đăng Ký kênh Thảo Dương TV & Nghe Video Dài", fill=(254, 240, 138), font=font_sub)

    final_img = Image.alpha_composite(img, overlay).convert("RGB")
    final_img.save(output_path, "JPEG", quality=95)

def get_audio_duration(audio_file):
    cmd = [
        FFMPEG, "-i", str(audio_file),
        "-hide_banner"
    ]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    for line in res.stderr.splitlines():
        if "Duration" in line:
            time_str = line.split("Duration:")[1].split(",")[0].strip()
            parts = time_str.split(":")
            return float(parts[0])*3600 + float(parts[1])*60 + float(parts[2])
    return 45.0

def build_single_short(item):
    item_id = item["id"]
    tts_mp3 = SHORTS_DIR / f"{item_id}_tts.mp3"
    card_jpg = SHORTS_DIR / f"{item_id}_card.jpg"
    out_mp4 = SHORTS_DIR / f"{item_id}_final.mp4"

    # 1. TTS
    print(f"🎙️ [1/4] Thu âm giọng đọc Nam Bộ (vi-VN-HoaiMyNeural)...")
    cmd_tts = [
        EDGE_TTS,
        "--voice", "vi-VN-HoaiMyNeural",
        "--text", item["script"],
        "--write-media", str(tts_mp3)
    ]
    for attempt in range(5):
        try:
            subprocess.run(cmd_tts, check=True)
            if tts_mp3.exists() and tts_mp3.stat().st_size > 1000:
                break
        except Exception as e_tts:
            print(f"⚠️ Thử lại TTS ({attempt+1}/5): {e_tts}")
            time.sleep(3)
    
    duration = get_audio_duration(tts_mp3)

    # 2. Card
    print(f"🎨 [2/4] Vẽ Card hình ảnh 1080x1920...")
    create_title_card(item["bg"], item["display_title"], item["series"], str(card_jpg))

    # 3. Render
    print(f"🎬 [3/4] Render video 9:16 (thời lượng {duration+1.5:.1f}s)...")
    cmd_render = [
        FFMPEG, "-y",
        "-loop", "1", "-i", str(card_jpg),
        "-i", str(tts_mp3),
        "-i", item["music"],
        "-filter_complex",
        f"[2:a]volume=0.18[bg];[1:a][bg]amix=inputs=2:duration=first:dropout_transition=2[aout]",
        "-map", "0:v",
        "-map", "[aout]",
        "-c:v", "libx264", "-tune", "stillimage", "-preset", "fast", "-crf", "22",
        "-c:a", "aac", "-b:a", "192k",
        "-t", str(duration + 1.5),
        "-pix_fmt", "yuv420p",
        str(out_mp4)
    ]
    subprocess.run(cmd_render, check=True)

    # Cleanup intermediate files
    if tts_mp3.exists(): tts_mp3.unlink()
    if card_jpg.exists(): card_jpg.unlink()

    return out_mp4

def run_schedule():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        items = json.load(f)

    prog = {}
    if SCHEDULE_PROGRESS.exists():
        try:
            with open(SCHEDULE_PROGRESS, "r", encoding="utf-8") as f:
                prog = json.load(f)
        except Exception:
            pass

    tokens = yt_upload.get_tokens()
    total_episodes = len(items)

    print(f"🚀 TIẾN TRÌNH LỊCH TRÌNH ĐĂNG 8 TẬP SHORTS - 1 TIẾNG / 1 TẬP")
    print(f"⏰ Thời gian hệ thống: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}")

    for idx, item in enumerate(items, 1):
        item_id = item["id"]
        title = item["title"]

        # Target timestamp for this episode (12:54, 13:54, 14:54...)
        target_timestamp = BASE_START_TIMESTAMP + (idx - 1) * INTERVAL_SECONDS
        target_time_str = datetime.fromtimestamp(target_timestamp).strftime('%H:%M:%S')

        if item_id in prog and prog[item_id].get("status") == "success":
            print(f"✅ [TẬP {idx}/{total_episodes}] ĐÃ ĐĂNG THÀNH CÔNG: {title}")
            print(f"   🔗 Link: {prog[item_id]['url']} (đăng lúc: {prog[item_id].get('time_str')})")
            continue

        # Check if time has arrived
        now = time.time()
        if now < target_timestamp:
            wait_sec = target_timestamp - now
            print(f"\n⏳ TẬP {idx}/{total_episodes} sẽ đăng vào lúc: {target_time_str} (còn {wait_sec/60:.1f} phút nữa).")
            print(f"💤 Đang đợi đúng mốc giờ {target_time_str}...")
            sys.stdout.flush()
            time.sleep(wait_sec)

        print(f"\n{'#'*70}")
        print(f"⏰ [{datetime.now().strftime('%H:%M:%S')}] ĐẾN GIỜ ĐĂNG TẬP {idx}/{total_episodes}: {title}")
        print(f"{'#'*70}")

        out_mp4 = None
        try:
            out_mp4 = build_single_short(item)
            size_mb = out_mp4.stat().st_size / 1024 / 1024
            print(f"📦 File hoàn tất ({size_mb:.1f} MB), bắt đầu upload...")

            current_tokens = yt_upload.get_tokens() or tokens
            uploaded_id, err = yt_upload.upload_one(
                filepath=str(out_mp4),
                title=title,
                description=item["description"],
                tags=item["tags"],
                privacy="public",
                tokens=current_tokens
            )

            if uploaded_id:
                yt_url = f"https://www.youtube.com/watch?v={uploaded_id}"
                now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"\n🎉 [TẬP {idx}/{total_episodes}] ĐĂNG THÀNH CÔNG: {yt_url} lúc {now_str}")
                prog[item_id] = {
                    "uploaded_id": uploaded_id,
                    "url": yt_url,
                    "title": title,
                    "status": "success",
                    "timestamp": time.time(),
                    "time_str": now_str
                }
                with open(SCHEDULE_PROGRESS, "w", encoding="utf-8") as f:
                    json.dump(prog, f, ensure_ascii=False, indent=2)
            else:
                print(f"❌ Upload thất bại: {err}")

        except Exception as e:
            print(f"❌ Lỗi khi xử lý tập {idx}: {e}")
        finally:
            if out_mp4 and out_mp4.exists():
                out_mp4.unlink()
                print("🧹 Đã dọn dẹp video thành phẩm.")

    print("\n🎊 TOÀN BỘ 8 TẬP ĐÃ ĐƯỢC ĐĂNG TẢI HOÀN TẤT THEO ĐÚNG LỊCH TRÌNH!")

if __name__ == "__main__":
    run_schedule()
