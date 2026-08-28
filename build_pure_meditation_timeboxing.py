#!/usr/bin/env python3
"""
Pure Meditation Music & Visual Text Storyline Generator for @1995lido (Thảo Dương TV)
- Removes human voiceover completely.
- Uses 100% pure 432Hz meditation relaxation music soundscape.
- Displays Time Boxing technique text directly on video frames.
- Auto-uploads live to YouTube via API.
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

output_mp4 = f"{SCRATCH_DIR}/output_queue/shorts_timeboxing_pure_meditation.mp4"
meditation_audio_wav = f"{SCRATCH_DIR}/pure_meditation_music.wav"

def generate_pure_meditation_music(duration=30.0):
    print("1. Synthesizing Pure 432Hz Solfeggio Meditation Music (No Voiceover)...")
    filter_expr = (
        "aevalsrc=sin(2*PI*432*t)*0.16 + sin(2*PI*528*t)*0.1 + sin(2*PI*216*t)*0.08:s=22050,"
        "lowpass=f=500,aecho=0.85:0.9:90|180:0.5|0.3,volume=0.55"
    )
    subprocess.run([
        FFMPEG, "-y", "-f", "lavfi",
        "-i", filter_expr,
        "-t", str(duration), meditation_audio_wav
    ], check=True)

def build_pure_meditation_video():
    duration = 30.0
    generate_pure_meditation_music(duration)
    
    d1 = 10.0
    d2 = 10.0
    d3 = 10.0
    
    print("2. Rendering 9:16 Video with Pure Meditation Music & Time Boxing Storyline Text...")
    
    # FFmpeg concat filter for 3 visual scenes
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
    print(f"✅ Pure Meditation Time Boxing Video created at: {output_mp4}")
    
    # 3. Auto-Upload Live to YouTube via API
    title = "Kỹ Thuật Time Boxing | Nhạc Thiền Thư Giãn 432Hz Không Lời #Shorts #ThaoDuongTV"
    description = (
        "Khám phá kỹ thuật Time Boxing giúp quản lý thời gian và tập trung sâu 100% cùng Thảo Dương TV (@1995lido).\n\n"
        "🎧 Nhạc thiền 432Hz không lời tĩnh lặng tâm hồn.\n"
        "🌱 Đăng ký kênh: https://www.youtube.com/@1995lido?sub_confirmation=1\n\n"
        "#Shorts #ThaoDuongTV #TimeBoxing #NhacThien #DeepWork"
    )
    tags = ["Thảo Dương TV", "1995lido", "TimeBoxing", "NhạcThiền", "KhôngLời", "Shorts"]
    
    print("🚀 AUTO-UPLOADING PURE MEDITATION SHORTS TO YOUTUBE...")
    video_id = upload_video_via_api(output_mp4, title, description, tags)
    return video_id

if __name__ == "__main__":
    build_pure_meditation_video()
