import os
import subprocess

SCRATCH_DIR = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management"
BRAIN_DIR = "/Users/abc/.gemini/antigravity/brain/f1b616c4-34df-4bce-8ba5-f93a710452fb"
FFMPEG = "/Users/abc/bin/ffmpeg"

img1 = f"{BRAIN_DIR}/youtube_shorts_thumbnail_1787412760992.jpg"
img2 = f"{BRAIN_DIR}/shorts_scene2_phone_1787412813911.jpg"
img3 = f"{BRAIN_DIR}/shorts_scene3_headphones_1787412829319.jpg"

bg_music_wav = f"{SCRATCH_DIR}/clean_bg_chill.wav"
output_mp4 = f"{SCRATCH_DIR}/shorts_01_MATCHED_STORYLINE_FINAL.mp4"

soothing_southern_script = (
    "Dạ chào bạn nhen... Sáng nay lòng bạn có đang thấy hơi mệt mỏi hông? "
    "Cho phép mình chậm lại một chút nghen. "
    "Dành 15 phút đầu tiên thật là yên bình... "
    "Uống một ngụm nước ấm nè, rồi viết ra 3 điều bạn muốn nâng niu hôm nay. "
    "Thảo Dương TV luôn ở đây để vỗ về tâm hồn bạn. "
    "Nhớ nhấn đăng ký kênh để đồng hành cùng mình mỗi ngày nhen!"
)

speech_raw = f"{SCRATCH_DIR}/matched_speech_raw.wav"
speech_processed = f"{SCRATCH_DIR}/matched_speech_processed.wav"
mixed_audio = f"{SCRATCH_DIR}/matched_audio_final.wav"

print("1. Synthesizing voiceover matching Short #1 script...")
subprocess.run(["say", "-v", "Linh", "-r", "116", "-o", f"{SCRATCH_DIR}/matched_speech.aiff", soothing_southern_script], check=True)
subprocess.run([FFMPEG, "-y", "-i", f"{SCRATCH_DIR}/matched_speech.aiff", speech_raw], check=True)

print("2. Matching acoustic warmth & EQ profile...")
subprocess.run([
    FFMPEG, "-y", "-i", speech_raw,
    "-af", "asetrate=22050*1.06,aresample=22050,atempo=1/1.06,equalizer=f=250:width_type=h:width=200:g=4,equalizer=f=3500:width_type=h:width=1200:g=2.5,lowpass=f=5000",
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

print("3. Mixing voiceover and ambient music...")
subprocess.run([
    FFMPEG, "-y", "-i", speech_processed, "-i", bg_music_wav,
    "-filter_complex", "[0:a]volume=1.4[a0];[1:a]volume=0.22[a1];[a0][a1]amix=inputs=2:duration=first[aout]",
    "-map", "[aout]", mixed_audio
], check=True)

# Render 9:16 Vertical Video
d1 = duration * 0.33
d2 = duration * 0.33
d3 = duration * 0.34

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

print("4. Rendering final storyline-matched Shorts MP4 Video...")
subprocess.run(cmd, check=True)
print(f"✅ STORYLINE MATCHED SHORTS VIDEO CREATED AT: {output_mp4}")
