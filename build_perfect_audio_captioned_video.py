#!/usr/bin/env python3
"""
Perfect Audio & Clean 9:16 Video Generator for @1995lido (Thảo Dương TV)
- Audio: Rich, loud, crystal-clear 432Hz Solfeggio meditation relaxation music.
- Visuals: Clean 9:16 vertical video scenes.
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

output_mp4 = f"{SCRATCH_DIR}/output_queue/shorts_perfect_audio_meditation.mp4"
meditation_audio_wav = f"{SCRATCH_DIR}/perfect_meditation_music.wav"

def generate_loud_meditation_music(duration=30.0):
    print("1. Generating Rich, Crystal-Clear 432Hz Meditation Music (Boosted Volume)...")
    filter_expr = (
        "aevalsrc=sin(2*PI*432*t)*0.35 + sin(2*PI*528*t)*0.25 + sin(2*PI*216*t)*0.2:s=44100,"
        "lowpass=f=1200,aecho=0.8:0.88:100|200:0.4|0.2,volume=3.0,loudnorm=I=-14:TP=-1.5:LRA=11"
    )
    subprocess.run([
        FFMPEG, "-y", "-f", "lavfi",
        "-i", filter_expr,
        "-t", str(duration), meditation_audio_wav
    ], check=True)

def render_perfect_video():
    duration = 30.0
    generate_loud_meditation_music(duration)
    
    d1 = 10.0
    d2 = 10.0
    d3 = 10.0
    
    print("2. Rendering 9:16 Video with Rich Audio & Clean Visual Storyline...")
    
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
        "-i", meditation_audio_wav,
        "-filter_complex", filter_complex,
        "-map", "[outv]", "-map", "3:a",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
        "-c:a", "aac", "-b:a", "192k", "-shortest",
        output_mp4
    ]
    
    subprocess.run(cmd, check=True)
    print(f"✅ Perfect Audio Video Created at: {output_mp4}")
    
    # 3. Auto-Upload Live to YouTube via API
    title = "Kỹ Thuật Time Boxing | Hướng Dẫn & Nhạc Thiền 432Hz To Rõ #Shorts #ThaoDuongTV"
    description = (
        "Khám phá kỹ thuật Time Boxing giúp quản lý thời gian và tập trung sâu 100% cùng Thảo Dương TV (@1995lido).\n\n"
        "🎧 Nhạc thiền 432Hz to rõ thư giãn tâm hồn.\n"
        "🌱 Đăng ký kênh: https://www.youtube.com/@1995lido?sub_confirmation=1\n\n"
        "#Shorts #ThaoDuongTV #TimeBoxing #NhacThien #DeepWork"
    )
    tags = ["Thảo Dương TV", "1995lido", "TimeBoxing", "NhạcThiền", "AmThanhToRo", "Shorts"]
    
    print("🚀 AUTO-UPLOADING PERFECT AUDIO SHORTS TO YOUTUBE...")
    video_id = upload_video_via_api(output_mp4, title, description, tags)
    return video_id

if __name__ == "__main__":
    render_perfect_video()
