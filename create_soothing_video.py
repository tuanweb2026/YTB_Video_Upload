import os
import subprocess

SCRATCH_DIR = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management"
BRAIN_DIR = "/Users/abc/.gemini/antigravity/brain/f1b616c4-34df-4bce-8ba5-f93a710452fb"
FFMPEG = "/Users/abc/bin/ffmpeg"

img1 = f"{BRAIN_DIR}/youtube_shorts_thumbnail_1787412760992.jpg"
img2 = f"{BRAIN_DIR}/shorts_scene2_phone_1787412813911.jpg"
img3 = f"{BRAIN_DIR}/shorts_scene3_headphones_1787412829319.jpg"

soothing_text = (
    "Chào bạn... Nếu sáng nay bạn cảm thấy lòng hơi mệt mỏi, hãy cho phép mình chậm lại một chút nhé. "
    "Dành 15 phút đầu tiên thật yên bình, không thông báo, không vội vã. "
    "Nếm một ngụm nước ấm, viết ra 3 điều bạn muốn nâng niu hôm nay. "
    "Và hãy để những giai điệu êm ái vỗ về tâm trí bạn. "
    "Thảo Dương TV luôn ở đây đồng hành cùng bạn. Nhấn đăng ký kênh để làm dịu tâm hồn mỗi ngày nhé."
)

aiff_file = f"{SCRATCH_DIR}/soothing_voice.aiff"
voice_wav = f"{SCRATCH_DIR}/soothing_voice.wav"
bg_music_wav = f"{SCRATCH_DIR}/bg_chill_music.wav"
mixed_audio = f"{SCRATCH_DIR}/final_soothing_audio.wav"
output_mp4 = f"{SCRATCH_DIR}/shorts_01_soothing_final.mp4"

# 1. Render gentle slow TTS using Linh voice with rate=125 (chậm rãi, ấm áp, truyền cảm)
print("1. Generating soothing voiceover (-r 125)...")
subprocess.run(["say", "-v", "Linh", "-r", "125", "-o", aiff_file, soothing_text], check=True)
subprocess.run([FFMPEG, "-y", "-i", aiff_file, voice_wav], check=True)

# Get audio duration
res = subprocess.run([FFMPEG, "-i", voice_wav], stderr=subprocess.PIPE, text=True)
duration = 33.0
for line in res.stderr.split('\n'):
    if "Duration" in line:
        parts = line.split("Duration:")[1].split(",")[0].strip().split(":")
        duration = float(parts[0])*3600 + float(parts[1])*60 + float(parts[2])
        break

print(f"Voice duration: {duration:.2f} seconds")

# 2. Generate smooth ambient chord soundscape
print("2. Synthesizing ambient chill music...")
subprocess.run([
    FFMPEG, "-y", "-f", "lavfi",
    "-i", "aevalsrc=sin(2*PI*261.63*t)*0.12+sin(2*PI*329.63*t)*0.08+sin(2*PI*392.00*t)*0.08:s=22050",
    "-af", "lowpass=f=600,aecho=0.8:0.88:60|120:0.4|0.2,volume=0.3",
    "-t", str(duration), bg_music_wav
], check=True)

# 3. Mix Voiceover + Ambient Chill Music
print("3. Mixing voiceover with ambient music...")
subprocess.run([
    FFMPEG, "-y", "-i", voice_wav, "-i", bg_music_wav,
    "-filter_complex", "[0:a]volume=1.3[a0];[1:a]volume=0.25[a1];[a0][a1]amix=inputs=2:duration=first[aout]",
    "-map", "[aout]", mixed_audio
], check=True)

# 4. Render 9:16 vertical video
d1 = duration * 0.33
d2 = duration * 0.33
d3 = duration * 0.34

cmd = [
    FFMPEG, "-y",
    "-loop", "1", "-t", str(d1), "-i", img1,
    "-loop", "1", "-t", str(d2), "-i", img2,
    "-loop", "1", "-t", str(d3), "-i", img3,
    "-i", mixed_audio,
    "-filter_complex", "[0:v][1:v][2:v]concat=n=3:v=1:a=0[outv]",
    "-map", "[outv]", "-map", "3:a",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
    "-c:a", "aac", "-b:a", "192k", "-shortest",
    output_mp4
]

print("4. Rendering final soothing MP4 video...")
subprocess.run(cmd, check=True)
print(f"✅ Soothing video rendered successfully at: {output_mp4}")
