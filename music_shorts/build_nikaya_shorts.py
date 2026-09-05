#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Builder & Publisher for 8 Buddhist Sutra Shorts
- Edge Neural TTS (vi-VN-HoaiMyNeural - Giọng Nam Bộ ngọt ngào)
- Pillow Dynamic Title Overlay Card
- Background Music (nhac_thien_432hz, nhac_chill_zen)
- FFmpeg 1080x1920 Vertical format
- YouTube Direct Resumable Upload
"""

import os
import sys
import json
import time
import subprocess
sys.path.append("/Users/abc/Library/Python/3.9/lib/python/site-packages")
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path("/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management")
SHORTS_DIR = Path("/Users/abc/.gemini/antigravity/scratch/music_shorts")
DATA_FILE = SHORTS_DIR / "nikaya_shorts_data.json"
PROGRESS_FILE = SHORTS_DIR / "nikaya_upload_progress.json"

sys.path.insert(0, str(BASE_DIR))
import yt_upload

FFMPEG = "/Users/abc/bin/ffmpeg"
EDGE_TTS = "/Users/abc/Library/Python/3.9/bin/edge-tts"

def create_title_card(base_img_path, title_lines, series_tag, output_path):
    img = Image.open(base_img_path).convert("RGBA")
    # Resize to exact 1080x1920
    img = img.resize((1080, 1920), Image.Resampling.LANCZOS)
    W, H = img.size

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Semi-transparent dark container
    card_top = int(H * 0.18)
    card_bottom = int(H * 0.42)
    card_left = int(W * 0.08)
    card_right = int(W * 0.92)

    draw.rounded_rectangle([card_left, card_top, card_right, card_bottom], radius=24, fill=(15, 23, 42, 215), outline=(255, 215, 0, 200), width=3)

    # Fonts
    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", index=1, size=48)
        font_brand = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", index=1, size=24)
        font_sub = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", index=0, size=26)
    except Exception:
        font_title = ImageFont.load_default()
        font_brand = font_title
        font_sub = font_title

    # Brand badge
    draw.rounded_rectangle([card_left + 24, card_top + 24, card_left + 320, card_top + 64], radius=12, fill=(217, 119, 6, 230))
    draw.text((card_left + 40, card_top + 30), f"🌸 {series_tag}", fill=(255, 255, 255), font=font_brand)

    # Title lines
    y_offset = card_top + 85
    for line in title_lines.split("\n"):
        draw.text((card_left + 28, y_offset), line.strip(), fill=(254, 240, 138), font=font_title)
        y_offset += 62

    # Footer note on card
    draw.text((card_left + 28, card_bottom - 45), "🎧 LỜI PHẬT DẠY NIKAYA · THẢO DƯƠNG TV", fill=(203, 213, 225), font=font_sub)

    final_img = Image.alpha_composite(img, overlay).convert("RGB")
    final_img.save(output_path, "JPEG", quality=95)

def get_audio_duration(file_path):
    res = subprocess.run([FFMPEG, "-i", str(file_path)], stderr=subprocess.PIPE, text=True)
    for line in res.stderr.split("\n"):
        if "Duration" in line:
            parts = line.split("Duration:")[1].split(",")[0].strip().split(":")
            return float(parts[0])*3600 + float(parts[1])*60 + float(parts[2])
    return 45.0

def build_and_upload():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        items = json.load(f)

    prog = {}
    if PROGRESS_FILE.exists():
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                prog = json.load(f)
        except Exception:
            pass

    tokens = yt_upload.get_tokens()

    for idx, item in enumerate(items, 1):
        item_id = item["id"]
        title = item["title"]

        if item_id in prog and prog[item_id].get("status") == "success":
            print(f"[{idx}/{len(items)}] ĐÃ CÓ: {title} -> {prog[item_id]['url']}")
            continue

        print(f"\n{'='*70}\n[{idx}/{len(items)}] ĐANG TẠO & ĐĂNG BÀI: {title}\n{'='*70}")

        tts_mp3 = SHORTS_DIR / f"{item_id}_tts.mp3"
        card_jpg = SHORTS_DIR / f"{item_id}_card.jpg"
        out_mp4 = SHORTS_DIR / f"{item_id}_final.mp4"

        try:
            # 1. Generate Voice TTS
            print("🎙️ 1/4. Thu âm giọng đọc miền Nam (vi-VN-HoaiMyNeural)...")
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
                    print(f"⚠️ Thử thu âm lại lần {attempt+1}/5 sau 3 giây... ({e_tts})")
                    time.sleep(3)
            duration = get_audio_duration(tts_mp3)
            print(f"✅ Thu âm hoàn tất (Thời lượng: {duration:.1f}s)")

            # 2. Generate Graphic Card
            print("🎨 2/4. Tạo card hình ảnh 1080x1920...")
            create_title_card(item["bg"], item["display_title"], item["series"], str(card_jpg))

            # 3. Mix Video + Audio + Background Music
            print("🎬 3/4. Render video hoàn chỉnh chuẩn 9:16...")
            bg_music = item["music"]
            # Video length = voice duration + 1.5s
            total_len = duration + 1.5

            cmd_render = [
                FFMPEG, "-y",
                "-loop", "1", "-i", str(card_jpg),
                "-i", str(tts_mp3),
                "-i", bg_music,
                "-filter_complex",
                f"[2:a]volume=0.18[bg];[1:a][bg]amix=inputs=2:duration=first:dropout_transition=2[aout]",
                "-map", "0:v",
                "-map", "[aout]",
                "-c:v", "libx264", "-tune", "stillimage", "-preset", "fast", "-crf", "22",
                "-c:a", "aac", "-b:a", "192k",
                "-t", str(total_len),
                "-pix_fmt", "yuv420p",
                str(out_mp4)
            ]
            subprocess.run(cmd_render, check=True)
            size_mb = out_mp4.stat().st_size / 1024 / 1024
            print(f"✅ Render thành công video Shorts ({size_mb:.1f} MB)")

            # 4. Upload to YouTube
            print("📤 4/4. Đăng tải trực tiếp lên kênh YouTube Thảo Dương TV (Public)...")
            current_tokens = yt_upload.get_tokens() or tokens
            uploaded_id, err = yt_upload.upload_one(
                filepath=str(out_mp4),
                title=item["title"],
                description=item["description"],
                tags=item["tags"],
                privacy="public",
                tokens=current_tokens
            )

            if uploaded_id:
                yt_url = f"https://www.youtube.com/watch?v={uploaded_id}"
                print(f"🎉 XUẤT BẢN THÀNH CÔNG! Link: {yt_url}")
                prog[item_id] = {
                    "uploaded_id": uploaded_id,
                    "url": yt_url,
                    "title": item["title"],
                    "status": "success",
                    "timestamp": time.time()
                }
                with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
                    json.dump(prog, f, ensure_ascii=False, indent=2)
            else:
                print(f"❌ Upload lỗi: {err}")

        except Exception as e:
            print(f"❌ Ngoại lệ trong quá trình xử lý: {e}")
        finally:
            if tts_mp3.exists():
                tts_mp3.unlink()
            if card_jpg.exists():
                card_jpg.unlink()
            if out_mp4.exists():
                out_mp4.unlink()
            print("🧹 Đã dọn dẹp file tạm.")

        time.sleep(3)

if __name__ == "__main__":
    build_and_upload()
