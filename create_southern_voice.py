import os
import subprocess

SCRATCH_DIR = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management"
BRAIN_DIR = "/Users/abc/.gemini/antigravity/brain/f1b616c4-34df-4bce-8ba5-f93a710452fb"
FFMPEG = "/Users/abc/bin/ffmpeg"

img1 = f"{BRAIN_DIR}/youtube_shorts_thumbnail_1787412760992.jpg"
img2 = f"{BRAIN_DIR}/shorts_scene2_phone_1787412813911.jpg"
img3 = f"{BRAIN_DIR}/shorts_scene3_headphones_1787412829319.jpg"

# Southern Vietnamese gentle motivational script (Từ ngữ Miền Nam dịu dàng, ngọt ngào, gần gũi)
southern_script = (
    "Dạ chào bạn nhen... Sáng nay lòng bạn có đang thấy hơi mệt mỏi hông? "
    "Cho phép mình chậm lại một chút nghen. "
    "Dành 15 phút đầu tiên thật là yên bình... "
    "Uống một ngụm nước ấm nè, rồi viết ra 3 điều bạn muốn nâng niu hôm nay. "
    "Thảo Dương TV luôn ở đây để vỗ về tâm hồn bạn. "
    "Nhớ nhấn đăng ký kênh để đồng hành cùng mình mỗi ngày nhen!"
)

aiff_file = f"{SCRATCH_DIR}/southern_voice.aiff"
voice_raw_wav = f"{SCRATCH_DIR}/southern_voice_raw.wav"
voice_sweet_wav = f"{SCRATCH_DIR}/southern_voice_sweet.wav"
bg_music_wav = f"{SCRATCH_DIR}/clean_bg_chill.wav"
final_audio = f"{SCRATCH_DIR}/southern_final_audio.wav"
output_mp4 = f"{SCRATCH_DIR}/shorts_01_southern_voiced_final.mp4"

# 1. Render base speech with slow rate=118
print("1. Generating Southern base voiceover...")
subprocess.run(["say", "-v", "Linh", "-r", "118", "-o", aiff_file, southern_script], check=True)
subprocess.run([FFMPEG, "-y", "-i", aiff_file, voice_raw_wav], check=True)

# 2. Apply pitch & formant modulation to sound sweet, soft, cute & young (pitch up 8%, smooth equalizer)
print("2. Pitch shifting & sweetening voice tone...")
subprocess.run([
    FFMPEG, "-y", "-i", voice_raw_wav,
    "-af", "asetrate=22050*1.08,aresample=22050,atempo=1/1.08,equalizer=f=3000:width_type=h:width=1000:g=3,lowpass=f=4500",
    voice_sweet_wav
], check=True)

# Get audio duration
res = subprocess.run([FFMPEG, "-i", voice_sweet_wav], stderr=subprocess.PIPE, text=True)
duration = 30.0
for line in res.stderr.split('\n'):
    if "Duration" in line:
        parts = line.split("Duration:")[1].split(",")[0].strip().split(":")
        duration = float(parts[0])*3600 + float(parts[1])*60 + float(parts[2])
        break

print(f"Southern voice duration: {duration:.2f}s")

# 3. Mix Sweet Southern Voice with Chill Ambient Music
print("3. Mixing voiceover and ambient music...")
subprocess.run([
    FFMPEG, "-y", "-i", voice_sweet_wav, "-i", bg_music_wav,
    "-filter_complex", "[0:a]volume=1.35[a0];[1:a]volume=0.25[a1];[a0][a1]amix=inputs=2:duration=first[aout]",
    "-map", "[aout]", final_audio
], check=True)

# 4. Render 9:16 vertical MP4 video
d1 = duration * 0.33
d2 = duration * 0.33
d3 = duration * 0.34

cmd = [
    FFMPEG, "-y",
    "-loop", "1", "-t", str(d1), "-i", img1,
    "-loop", "1", "-t", str(d2), "-i", img2,
    "-loop", "1", "-t", str(d3), "-i", img3,
    "-i", final_audio,
    "-filter_complex", "[0:v][1:v][2:v]concat=n=3:v=1:a=0[outv]",
    "-map", "[outv]", "-map", "3:a",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
    "-c:a", "aac", "-b:a", "192k", "-shortest",
    output_mp4
]

print("4. Rendering final Southern Voiced Shorts Video...")
subprocess.run(cmd, check=True)
print(f"✅ Final Southern Voiced Video rendered at: {output_mp4}")
