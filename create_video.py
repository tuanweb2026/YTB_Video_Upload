import os
import subprocess

SCRATCH_DIR = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management"
BRAIN_DIR = "/Users/abc/.gemini/antigravity/brain/f1b616c4-34df-4bce-8ba5-f93a710452fb"
FFMPEG = "/Users/abc/bin/ffmpeg"

img1 = f"{BRAIN_DIR}/youtube_shorts_thumbnail_1787412760992.jpg"
img2 = f"{BRAIN_DIR}/shorts_scene2_phone_1787412813911.jpg"
img3 = f"{BRAIN_DIR}/shorts_scene3_headphones_1787412829319.jpg"

voice_text = "Nếu bạn cảm thấy mệt mỏi mỗi sáng, thử ngay 3 bước này. Bước 1: Không chạm điện thoại 15 phút đầu. Bước 2: Uống nước ấm và viết 3 việc quan trọng. Bước 3: Nghe 5 phút nhạc nhẹ để đưa não vào trạng thái tập trung. Nhớ nhấn Đăng ký kênh Thảo Dương TV nhé!"

aiff_file = f"{SCRATCH_DIR}/voice.aiff"
wav_file = f"{SCRATCH_DIR}/voice.wav"
output_mp4 = f"{SCRATCH_DIR}/shorts_01_final.mp4"

# 1. Generate Voiceover using Mac TTS (Linh)
subprocess.run(["say", "-v", "Linh", "-o", aiff_file, voice_text], check=True)
subprocess.run([FFMPEG, "-y", "-i", aiff_file, wav_file], check=True)

# Get audio duration
res = subprocess.run([FFMPEG, "-i", wav_file], stderr=subprocess.PIPE, text=True)
duration = 20.0
for line in res.stderr.split('\n'):
    if "Duration" in line:
        parts = line.split("Duration:")[1].split(",")[0].strip().split(":")
        duration = float(parts[0])*3600 + float(parts[1])*60 + float(parts[2])
        break

d1 = duration * 0.3
d2 = duration * 0.35
d3 = duration * 0.35

# 2. Build FFmpeg command to stitch images with audio
filter_complex = (
    f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,loop=loop=-1:size=1:start=0,setpts=N/TB[v0];"
    f"[1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,loop=loop=-1:size=1:start=0,setpts=N/TB[v1];"
    f"[2:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,loop=loop=-1:size=1:start=0,setpts=N/TB[v2];"
    f"[v0][v1][v2]concat=n=3:v=1:a=0[vcat];"
    f"[vcat]trim=duration={duration}[v]"
)

# Simplified ffmpeg command for generating 1080x1920 video with voiceover
cmd = [
    FFMPEG, "-y",
    "-loop", "1", "-t", str(d1), "-i", img1,
    "-loop", "1", "-t", str(d2), "-i", img2,
    "-loop", "1", "-t", str(d3), "-i", img3,
    "-i", wav_file,
    "-filter_complex", "[0:v][1:v][2:v]concat=n=3:v=1:a=0[outv]",
    "-map", "[outv]", "-map", "3:a",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
    "-c:a", "aac", "-b:a", "192k", "-shortest",
    output_mp4
]

print("Executing FFmpeg video render...")
subprocess.run(cmd, check=True)
print(f"✅ Video created successfully at: {output_mp4}")
