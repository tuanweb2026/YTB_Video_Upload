#!/usr/bin/env python3
"""
Custom Video Generator for @anhhailuavuive (Anh Hai Lúa Hài Hước)
Synthesizes multi-voice dialog (Sếp: Male, Nhân viên: Female) and builds a funny MP4 short video.
Places output directly in /Users/abc/Documents/Kenh_youtube/anh Hai lua - Hai Huoc/
"""

import os
import sys
import re
import time
import subprocess
from PIL import Image, ImageDraw, ImageFont

TARGET_DIR = "/Users/abc/Documents/Kenh_youtube/anh Hai lua - Hai Huoc"
SCRATCH_DIR = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management"
BRAIN_DIR = "/Users/abc/.gemini/antigravity/brain/f1b616c4-34df-4bce-8ba5-f93a710452fb"
OUTPUT_MP4 = os.path.join(TARGET_DIR, "anh_hai_lua_hai_huoc.mp4")
FFMPEG = "/Users/abc/bin/ffmpeg"

DIALOG = [
    {"speaker": "sep", "text": "Nãy giờ cô vẫn chưa về à?"},
    {"speaker": "nv", "text": "Dạ đúng rồi sếp. Em đang tìm chìa khóa mà không thấy đâu hết trơn á."},
    {"speaker": "sep", "text": "Mất chìa khóa hả? Tôi giúp cô mở khóa lấy hữu nghị hai trăm cành thôi."},
    {"speaker": "nv", "text": "Hai trăm cành? Gì đắt dữ vậy sếp?"},
    {"speaker": "sep", "text": "Ái chà, tuy tôi là sếp nhưng kỹ năng mở khóa tôi cũng phải bỏ tiền đi học đó nha. Bớt chút đi mà sếp. Ờ không bớt được đâu. Cô đi làm cho tôi lương cô đâu bớt lại cho tôi. Tôi mở không chạm vào xe luôn."},
    {"speaker": "nv", "text": "Tức là anh không cần sờ vào xe mà vẫn mở được hả?"},
    {"speaker": "sep", "text": "Đúng vậy, không sờ vào xe mà vẫn mở được. Muốn mở thì thanh toán tiền trước đã."},
    {"speaker": "nv", "text": "Đây, sếp cứ mở ra trước đi, không trả tiền sếp trừ lương em nè."},
    {"speaker": "sep", "text": "Không được, cơ hội như này không xuất hiện lần thứ hai. Cô bắt buộc phải chuyển khoản trước. Không mở được tôi đền cô bốn trăm cành."},
    {"speaker": "nv", "text": "Xong rồi đó sếp, sếp mở đi."},
    {"speaker": "sep", "text": "Chờ tí, mạng hơi bị trễ. À à nhận được tiền rồi. Ủa, sao cái chìa khóa xe này của cô bấm lại không mở được vậy?"},
    {"speaker": "nv", "text": "Ai bảo với sếp chìa khóa này là của cái xe này? Chìa khóa này là của xe khác mà!"},
    {"speaker": "sep", "text": "Hả?"},
    {"speaker": "nv", "text": "Không chạm vào xe cơ mà. Sếp mở tiếp đi. Mở không được chứ gì? Đền em bốn trăm cành!"},
    {"speaker": "sep", "text": "Ải thật, bị cô chơi một vố đau rồi!"}
]

def generate_voiceover_segments():
    print("🎙️ Synthesizing multi-voice dialog segment by segment...")
    segment_files = []
    
    for i, line in enumerate(DIALOG):
        voice = "vi-VN-NamMinhNeural" if line["speaker"] == "sep" else "vi-VN-HoaiMyNeural"
        segment_mp3 = f"{SCRATCH_DIR}/seg_{i}.mp3"
        segment_wav = f"{SCRATCH_DIR}/seg_{i}.wav"
        
        cmd = [sys.executable, "-m", "edge_tts", "--voice", voice, "--text", line["text"], "--write-media", segment_mp3]
        
        success = False
        for attempt in range(3):
            try:
                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if os.path.exists(segment_mp3) and os.path.getsize(segment_mp3) > 100:
                    success = True
                    break
            except Exception:
                time.sleep(1)
                
        if not success:
            # Fallback text
            simple_text = re.sub(r"[^a-zA-Z0-9àáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđÀÁẢÃẠÂẦẤẨẪẬĂẰẮẲẴẶÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ ]", "", line["text"])
            cmd_fallback = [sys.executable, "-m", "edge_tts", "--voice", voice, "--text", simple_text, "--write-media", segment_mp3]
            subprocess.run(cmd_fallback, check=True)
            
        # Convert to WAV
        subprocess.run([FFMPEG, "-y", "-i", segment_mp3, segment_wav], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        segment_files.append(segment_wav)
        
    return segment_files

def concatenate_audio_segments(segment_files):
    print("🎛️ Concatenating all dialog audio segments...")
    concat_list_file = f"{SCRATCH_DIR}/concat_list.txt"
    with open(concat_list_file, "w", encoding="utf-8") as f:
        for fpath in segment_files:
            f.write(f"file '{fpath}'\n")
            # Insert a 0.5s pause between sentences
            f.write(f"file '{SCRATCH_DIR}/pause_0.5s.wav'\n")
            
    # Create a 0.5s silence file
    subprocess.run([
        FFMPEG, "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", "0.5",
        f"{SCRATCH_DIR}/pause_0.5s.wav"
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    raw_voice_wav = f"{SCRATCH_DIR}/dialog_raw.wav"
    subprocess.run([
        FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", concat_list_file, "-c", "copy", raw_voice_wav
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    return raw_voice_wav

def create_humorous_title_card():
    print("🎨 Creating humorous Title Card overlay...")
    img = Image.new("RGB", (768, 1376), color="#1e293b")
    draw = ImageDraw.Draw(img)
    
    # Draw simple colorful background shapes
    draw.rectangle([50, 50, 718, 1326], outline="#facc15", width=6)
    draw.rectangle([60, 60, 708, 1316], outline="#ec4899", width=2)
    
    font_path = "/Library/Fonts/Arial Unicode.ttf"
    if not os.path.exists(font_path):
        font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
        
    try:
        font_large = ImageFont.truetype(font_path, 48)
        font_medium = ImageFont.truetype(font_path, 36)
    except Exception:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        
    draw.text((384, 200), "ANH HAI LÚA HÀI HƯỚC", fill="#facc15", font=font_large, anchor="mm")
    draw.text((384, 300), "Kịch Bản: Mở Khóa Xe", fill="#38bdf8", font=font_medium, anchor="mm")
    draw.text((384, 380), "Hữu Nghị 200k!", fill="#ffffff", font=font_large, font_style="bold" if hasattr(font_large, "font_style") else None, anchor="mm")
    
    card_path = f"{SCRATCH_DIR}/hailua_title_card.jpg"
    img.save(card_path)
    return card_path

def build_final_funny_video():
    os.makedirs(TARGET_DIR, exist_ok=True)
    
    seg_files = generate_voiceover_segments()
    dialog_wav = concatenate_audio_segments(seg_files)
    title_card = create_humorous_title_card()
    
    # Process voice to add slight warmth
    processed_voice = f"{SCRATCH_DIR}/dialog_processed.wav"
    subprocess.run([
        FFMPEG, "-y", "-i", dialog_wav,
        "-af", "equalizer=f=300:width_type=h:width=150:g=2.5,lowpass=f=8000",
        processed_voice
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Get audio duration
    res = subprocess.run([FFMPEG, "-i", processed_voice], stderr=subprocess.PIPE, text=True)
    duration = 30.0
    for line in res.stderr.split('\n'):
        if "Duration" in line:
            parts = line.split("Duration:")[1].split(",")[0].strip().split(":")
            duration = float(parts[0])*3600 + float(parts[1])*60 + float(parts[2])
            break
            
    print(f"🎬 Humorous video voiceover duration: {duration:.2f} seconds.")
    
    # Mix with funny backing music (we reuse chill backing loop but lower volume)
    bg_music_wav = f"{SCRATCH_DIR}/clean_bg_chill.wav"
    mixed_audio = f"{SCRATCH_DIR}/dialog_mixed.wav"
    
    if os.path.exists(bg_music_wav):
        subprocess.run([
            FFMPEG, "-y", "-i", processed_voice, "-stream_loop", "-1", "-i", bg_music_wav,
            "-filter_complex", "[0:a]volume=1.8[v];[1:a]volume=0.18[m];[v][m]amix=inputs=2:duration=first",
            "-t", str(duration), mixed_audio
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        mixed_audio = processed_voice
        
    # Render final MP4
    bg_zen_meditation = f"{BRAIN_DIR}/bg_zen_meditation_1787464848840.jpg"
    img2 = f"{BRAIN_DIR}/shorts_scene2_phone_1787412813911.jpg"
    
    print(f"🎥 Rendering final funny video to: {OUTPUT_MP4}...")
    
    subprocess.run([
        FFMPEG, "-y",
        "-loop", "1", "-t", "5.0", "-i", title_card,
        "-loop", "1", "-t", str(duration - 5.0), "-i", img2,
        "-i", mixed_audio,
        "-filter_complex", "[0:v]scale=768:1376,setdar=24/43[v0];[1:v]scale=768:1376,setdar=24/43[v1];[v0][v1]concat=n=2:v=1:a=0[v]",
        "-map", "[v]", "-map", "2:a",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest", OUTPUT_MP4
    ], check=True)
    
    print("🎉 Humorous short video successfully built!")

if __name__ == "__main__":
    build_final_funny_video()
