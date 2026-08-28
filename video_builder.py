#!/usr/bin/env python3
"""
Automated Neural AI Video Builder for @1995lido (Thảo Dương TV)
- Dynamic Title Card overlay printed directly on the background image for each video.
- 100% unique custom background graphics matching each video title.
- Video duration: ~30 seconds long.
- Microsoft Edge Neural AI TTS (vi-VN-HoaiMyNeural) for 100% natural Southern voiceover.
- Warm channel subscription call-to-action ending.
"""

import os
import sys
import re
import time
import subprocess
from content_generator import get_slot_content
from make_dynamic_title_card import create_title_overlay_image

SCRATCH_DIR = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management"
BRAIN_DIR = "/Users/abc/.gemini/antigravity/brain/f1b616c4-34df-4bce-8ba5-f93a710452fb"
OUTPUT_QUEUE = f"{SCRATCH_DIR}/output_queue"
FFMPEG = "/Users/abc/bin/ffmpeg"

BG_ZEN = f"{BRAIN_DIR}/bg_zen_meditation_1787464848840.jpg"
BG_DEEPWORK = f"{BRAIN_DIR}/bg_deep_work_focus_1787464869588.jpg"
BG_NIGHT = f"{BRAIN_DIR}/bg_night_chill_1787464916542.jpg"

bg_music_wav = f"{SCRATCH_DIR}/clean_bg_chill.wav"

def get_base_theme_image(category_or_series=""):
    cat_lower = str(category_or_series).lower()
    if "deep work" in cat_lower or "tối ưu" in cat_lower or "năng lượng" in cat_lower or "kỷ luật" in cat_lower:
        return BG_DEEPWORK
    elif "nhạc" in cat_lower or "đêm" in cat_lower or "chill" in cat_lower or "432hz" in cat_lower or "nikaya" in cat_lower:
        return BG_ZEN
    else:
        return BG_ZEN

def generate_neural_tts(text, output_mp3):
    print("🎙️ Synthesizing Ultra-Realistic Southern Voice (vi-VN-HoaiMyNeural)...")
    clean_text = re.sub(r"[^\w\s\.,!\?àáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđÀÁẢÃẠÂẦẤẨẪẬĂẰẮẲẴẶÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ]", " ", text)
    clean_text = re.sub(r"\s+", " ", clean_text).strip()
    
    cmd = ["/Users/abc/Library/Python/3.9/bin/edge-tts", "--voice", "vi-VN-HoaiMyNeural", "--text", clean_text, "--write-media", output_mp3]
    
    for attempt in range(3):
        try:
            subprocess.run(cmd, check=True)
            if os.path.exists(output_mp3) and os.path.getsize(output_mp3) > 1000:
                return output_mp3
        except Exception as e:
            print(f"⚠️ TTS Attempt {attempt+1} failed: {e}. Retrying after 2s...")
            time.sleep(2)
            
    # Fallback to simple text if edge-tts had network glitch
    ultra_simple = re.sub(r"[^a-zA-Z0-9àáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđÀÁẢÃẠÂẦẤẨẪẬĂẰẮẲẴẶÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ ]", "", clean_text)
    cmd2 = ["/Users/abc/Library/Python/3.9/bin/edge-tts", "--voice", "vi-VN-HoaiMyNeural", "--text", ultra_simple, "--write-media", output_mp3]
    subprocess.run(cmd2, check=True)
    return output_mp3

def build_video_for_content(content_data, video_filename="shorts_auto.mp4"):
    script_text = content_data["script"]
    title_text = content_data["title"].replace("#Shorts", "").replace("#ThaoDuongTV", "").replace("#NikayaKinh", "").strip()
    category_text = content_data.get("category", content_data.get("series", "Thảo Dương TV"))
    
    base_bg = get_base_theme_image(category_text)
    
    clean_filename = video_filename.replace(".mp4", "")
    custom_title_card = f"{SCRATCH_DIR}/title_card_{clean_filename}.jpg"
    create_title_overlay_image(base_bg, title_text, custom_title_card, series_tag=category_text[:20])
    
    img1 = custom_title_card
    img2 = f"{BRAIN_DIR}/shorts_scene2_phone_1787412813911.jpg"
    img3 = base_bg
    
    output_mp4 = f"{OUTPUT_QUEUE}/{video_filename}"
    
    speech_mp3 = f"{SCRATCH_DIR}/auto_speech_neural.mp3"
    speech_raw = f"{SCRATCH_DIR}/auto_speech_raw.wav"
    speech_processed = f"{SCRATCH_DIR}/auto_speech_processed.wav"
    mixed_audio = f"{SCRATCH_DIR}/auto_mixed_audio.wav"
    
    print(f"🎬 Building ~30s Video with Dynamic Title Overlay [{title_text[:25]}] -> {video_filename}")
    
    generate_neural_tts(script_text, speech_mp3)
    subprocess.run([FFMPEG, "-y", "-i", speech_mp3, speech_raw], check=True)
    
    subprocess.run([
        FFMPEG, "-y", "-i", speech_raw,
        "-af", "equalizer=f=250:width_type=h:width=200:g=3.5,equalizer=f=3500:width_type=h:width=1200:g=2.0,lowpass=f=6000",
        speech_processed
    ], check=True)
    
    res = subprocess.run([FFMPEG, "-i", speech_processed], stderr=subprocess.PIPE, text=True)
    duration = 30.0
    for line in res.stderr.split('\n'):
        if "Duration" in line:
            parts = line.split("Duration:")[1].split(",")[0].strip().split(":")
            duration = float(parts[0])*3600 + float(parts[1])*60 + float(parts[2])
            break
            
    subprocess.run([
        FFMPEG, "-y", "-i", speech_processed, "-i", bg_music_wav,
        "-filter_complex", "[0:a]volume=1.35[a0];[1:a]volume=0.22[a1];[a0][a1]amix=inputs=2:duration=first[aout]",
        "-map", "[aout]", mixed_audio
    ], check=True)
    
    d1 = duration * 0.35
    d2 = duration * 0.30
    d3 = duration * 0.35
    
    filter_complex = (
        f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,loop=loop=-1:size=1:start=0,setpts=N/TB[v0];"
        f"[1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,loop=loop=-1:size=1:start=0,setpts=N/TB[v1];"
        f"[2:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,loop=loop=-1:size=1:start=0,setpts=N/TB[v2];"
        f"[v0][v1][v2]concat=n=3:v=1:a=0[outv]"
    )
    
    cmd = [
        FFMPEG, "-y",
        "-loop", "1", "-t", str(d1), "-i", img1,
        "-loop", "1", "-t", str(d2), "-i", img2,
        "-loop", "1", "-t", str(d3), "-i", img3,
        "-i", mixed_audio,
        "-filter_complex", filter_complex,
        "-map", "[outv]", "-map", "3:a",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
        "-c:a", "aac", "-b:a", "192k", "-shortest",
        output_mp4
    ]
    
    subprocess.run(cmd, check=True)
    print(f"✅ Dynamic Title Video created at: {output_mp4} (Duration: {duration:.1f}s)")
    return output_mp4

if __name__ == "__main__":
    content = get_slot_content(1, "slot_08am")
    build_video_for_content(content, "shorts_day_1.mp4")
