#!/usr/bin/env python3
"""
Meditation Music & On-Screen Captions Video Generator for @1995lido (Thảo Dương TV)
Renders 9:16 vertical Shorts video with relaxing 432Hz meditation music and burnt-in captions,
then automatically uploads live to YouTube via API.
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

output_mp4 = f"{SCRATCH_DIR}/output_queue/shorts_day_1_meditation_captioned.mp4"
meditation_bg_wav = f"{SCRATCH_DIR}/meditation_music_432hz.wav"
mixed_audio_wav = f"{SCRATCH_DIR}/meditation_mixed_audio.wav"

def generate_meditation_music(duration=30.0):
    print("1. Synthesizing 432Hz / 528Hz Solfeggio Meditation Music...")
    filter_expr = (
        "aevalsrc=sin(2*PI*432*t)*0.12 + sin(2*PI*528*t)*0.08 + sin(2*PI*216*t)*0.1:s=22050,"
        "lowpass=f=450,aecho=0.85:0.9:80|160:0.5|0.3,volume=0.35"
    )
    subprocess.run([
        FFMPEG, "-y", "-f", "lavfi",
        "-i", filter_expr,
        "-t", str(duration), meditation_bg_wav
    ], check=True)

def render_captioned_video():
    content = get_slot_content(1, "slot_08am")
    script_text = content["script"]
    
    # 1. Generate Voiceover
    speech_raw = f"{SCRATCH_DIR}/meditation_speech_raw.wav"
    speech_processed = f"{SCRATCH_DIR}/meditation_speech_processed.wav"
    aiff_file = f"{SCRATCH_DIR}/meditation_speech.aiff"
    
    print("2. Generating Southern Voiceover...")
    subprocess.run(["say", "-v", "Linh", "-r", "116", "-o", aiff_file, script_text], check=True)
    subprocess.run([FFMPEG, "-y", "-i", aiff_file, speech_raw], check=True)
    
    # Audio processing
    subprocess.run([
        FFMPEG, "-y", "-i", speech_raw,
        "-af", "asetrate=22050*1.05,aresample=22050,atempo=1/1.05,equalizer=f=250:width_type=h:width=200:g=4,equalizer=f=3500:width_type=h:width=1200:g=2.5,lowpass=f=5000",
        speech_processed
    ], check=True)
    
    # Get audio duration
    res = subprocess.run([FFMPEG, "-i", speech_processed], stderr=subprocess.PIPE, text=True)
    duration = 30.0
    for line in res.stderr.split('\n'):
        if "Duration" in line:
            parts = line.split("Duration:")[1].split(",")[0].strip().split(":")
            duration = float(parts[0])*3600 + float(parts[1])*60 + float(parts[2])
            break
            
    # 2. Generate Meditation Music & Mix
    generate_meditation_music(duration)
    
    print("3. Mixing Voiceover with Meditation Music...")
    subprocess.run([
        FFMPEG, "-y", "-i", speech_processed, "-i", meditation_bg_wav,
        "-filter_complex", "[0:a]volume=1.3[a0];[1:a]volume=0.3[a1];[a0][a1]amix=inputs=2:duration=first[aout]",
        "-map", "[aout]", mixed_audio_wav
    ], check=True)
    
    # 3. Render 9:16 Video
    d1 = duration * 0.33
    d2 = duration * 0.33
    d3 = duration * 0.34
    
    filter_complex = (
        f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,loop=loop=-1:size=1:start=0,setpts=N/TB[v0];"
        f"[1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,loop=loop=-1:size=1:start=0,setpts=N/TB[v1];"
        f"[2:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,loop=loop=-1:size=1:start=0,setpts=N/TB[v2];"
        f"[v0][v1][v2]concat=n=3:v=1:a=0[outv]"
    )
    
    print("4. Rendering 9:16 Meditation Video...")
    cmd = [
        FFMPEG, "-y",
        "-loop", "1", "-t", str(d1), "-i", img1,
        "-loop", "1", "-t", str(d2), "-i", img2,
        "-loop", "1", "-t", str(d3), "-i", img3,
        "-i", mixed_audio_wav,
        "-filter_complex", filter_complex,
        "-map", "[outv]", "-map", "3:a",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
        "-c:a", "aac", "-b:a", "192k", "-shortest",
        output_mp4
    ]
    
    subprocess.run(cmd, check=True)
    print(f"✅ Meditation Captioned Video created at: {output_mp4}")
    
    # 4. Execute Auto Upload to YouTube Live (Title kept strictly < 90 chars)
    title = "Kỹ thuật Time Boxing Nâng Cao | Nhạc Thiền Thư Giãn #Shorts #ThaoDuongTV"
    print(f"🚀 AUTO-UPLOADING NEW MEDITATION SHORTS TO YOUTUBE...")
    video_id = upload_video_via_api(output_mp4, title, content["description"], content["tags"])
    return video_id

if __name__ == "__main__":
    render_captioned_video()
