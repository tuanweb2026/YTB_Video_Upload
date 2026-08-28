#!/usr/bin/env python3
"""
Fixed Audio & Full On-Screen Captions Video Generator for @1995lido (Thảo Dương TV)
- Audio: Rich, clear, audible 432Hz meditation relaxation music (loudnorm + volume boosted).
- Visuals: Full on-screen text overlays displaying complete Time Boxing guide.
- Auto-upload live to YouTube via API.
"""

import os
import sys
import json
import ssl
import subprocess
from content_generator import get_slot_content
from youtube_api_auto_uploader import upload_video_via_api

ssl._create_default_https_context = ssl._create_unverified_context

SCRATCH_DIR = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management"
BRAIN_DIR = "/Users/abc/.gemini/antigravity/brain/f1b616c4-34df-4bce-8ba5-f93a710452fb"
FFMPEG = "/Users/abc/bin/ffmpeg"

img1 = f"{BRAIN_DIR}/youtube_shorts_thumbnail_1787412760992.jpg"
img2 = f"{BRAIN_DIR}/shorts_scene2_phone_1787412813911.jpg"
img3 = f"{BRAIN_DIR}/shorts_scene3_headphones_1787412829319.jpg"

output_mp4 = f"{SCRATCH_DIR}/output_queue/shorts_timeboxing_audible_meditation.mp4"
meditation_audio_wav = f"{SCRATCH_DIR}/loud_meditation_music.wav"

def generate_audible_meditation_music(duration=30.0):
    print("1. Generating Rich, Loud Audible 432Hz Meditation Music...")
    filter_expr = (
        "aevalsrc=sin(2*PI*432*t)*0.35 + sin(2*PI*528*t)*0.25 + sin(2*PI*216*t)*0.2 + sin(2*PI*648*t)*0.1:s=44100,"
        "lowpass=f=1200,aecho=0.8:0.88:100|200:0.4|0.2,volume=2.5,loudnorm=I=-16:TP=-1.5:LRA=11"
    )
    subprocess.run([
        FFMPEG, "-y", "-f", "lavfi",
        "-i", filter_expr,
        "-t", str(duration), meditation_audio_wav
    ], check=True)

def render_fixed_video():
    duration = 30.0
    generate_audible_meditation_music(duration)
    
    d1 = 10.0
    d2 = 10.0
    d3 = 10.0
    
    print("2. Rendering 9:16 Video with Full Text Captions & Rich Audio...")
    
    font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
    if not os.path.exists(font_path):
        font_path = "/System/Library/Fonts/Helvetica.ttc"
        
    filter_complex = (
        f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        f"drawtext=fontfile='{font_path}':text='KY THUAT TIME BOXING':fontcolor=yellow:fontsize=52:x=(w-text_w)/2:y=180:box=1:boxcolor=black@0.6:boxborderw=15,"
        f"drawtext=fontfile='{font_path}':text='Quan Ly 1 Ngay Khong Xao Nhang':fontcolor=white:fontsize=38:x=(w-text_w)/2:y=270:box=1:boxcolor=black@0.5:boxborderw=10,"
        f"drawtext=fontfile='{font_path}':text='1. Tat moi thong bao trong 15 phut dau sang':fontcolor=yellow:fontsize=36:x=(w-text_w)/2:y=1600:box=1:boxcolor=black@0.6:boxborderw=12[v0];"
        
        f"[1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        f"drawtext=fontfile='{font_path}':text='2 BUOC NANG CAO HIEU SUAT':fontcolor=yellow:fontsize=52:x=(w-text_w)/2:y=180:box=1:boxcolor=black@0.6:boxborderw=15,"
        f"drawtext=fontfile='{font_path}':text='2. Uong 1 ngum nuoc am nap nang luong':fontcolor=white:fontsize=38:x=(w-text_w)/2:y=270:box=1:boxcolor=black@0.5:boxborderw=10,"
        f"drawtext=fontfile='{font_path}':text='3. Viet ra dung 3 cong viec quan trong nhat':fontcolor=yellow:fontsize=36:x=(w-text_w)/2:y=1600:box=1:boxcolor=black@0.6:boxborderw=12[v1];"
        
        f"[2:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        f"drawtext=fontfile='{font_path}':text='TRANG THAI TAP TRUNG DEEP WORK':fontcolor=yellow:fontsize=50:x=(w-text_w)/2:y=180:box=1:boxcolor=black@0.6:boxborderw=15,"
        f"drawtext=fontfile='{font_path}':text='Chia khung gio 25 - 50 phut tap trung 100%':fontcolor=white:fontsize=38:x=(w-text_w)/2:y=270:box=1:boxcolor=black@0.5:boxborderw=10,"
        f"drawtext=fontfile='{font_path}':text='DANG KY KENH @1995lido NGAY!':fontcolor=white:fontsize=42:x=(w-text_w)/2:y=1650:box=1:boxcolor=red@0.8:boxborderw=15[v2];"
        
        f"[v0][v1][v2]concat=n=3:v=1:a=0[outv]"
    )
    
    cmd = [
        FFMPEG, "-y",
        "-loop", "1", "-t", str(d1), "-i", img1,
        "-loop", "1", "-t", str(d2), "-i", img2,
        "-loop", "1", "-t", str(d3), "-i", img3,
        "-i", meditation_audio_wav,
        "-filter_complex", filter_complex,
        "-map", "[outv]", "-map", "3:a",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
        "-c:a", "aac", "-b:a", "192k", "-shortest",
        output_mp4
    ]
    
    subprocess.run(cmd, check=True)
    print(f"✅ Fixed Video Created Successfully at: {output_mp4}")
    
    # 3. Auto-Upload Live to YouTube via API
    title = "Kỹ Thuật Time Boxing | Hướng Dẫn Chi Tiết & Nhạc Thiền 432Hz #Shorts #ThaoDuongTV"
    description = (
        "Khám phá kỹ thuật Time Boxing giúp quản lý thời gian và tập trung sâu 100% cùng Thảo Dương TV (@1995lido).\n\n"
        "🎧 Nhạc thiền 432Hz to rõ thư giãn & Hiển thị chữ tiếng Việt chi tiết.\n"
        "🌱 Đăng ký kênh: https://www.youtube.com/@1995lido?sub_confirmation=1\n\n"
        "#Shorts #ThaoDuongTV #TimeBoxing #NhacThien #DeepWork"
    )
    tags = ["Thảo Dương TV", "1995lido", "TimeBoxing", "NhạcThiền", "ChữTiếngViệt", "Shorts"]
    
    print("🚀 AUTO-UPLOADING FIXED SHORTS TO YOUTUBE...")
    video_id = upload_video_via_api(output_mp4, title, description, tags)
    return video_id

if __name__ == "__main__":
    render_fixed_video()
