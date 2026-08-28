import os
import subprocess

SCRATCH_DIR = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management"
BRAIN_DIR = "/Users/abc/.gemini/antigravity/brain/f1b616c4-34df-4bce-8ba5-f93a710452fb"
FFMPEG = "/Users/abc/bin/ffmpeg"

img1 = f"{BRAIN_DIR}/youtube_shorts_thumbnail_1787412760992.jpg"
img2 = f"{BRAIN_DIR}/shorts_scene2_phone_1787412813911.jpg"
img3 = f"{BRAIN_DIR}/shorts_scene3_headphones_1787412829319.jpg"

duration = 30.0
bg_music_wav = f"{SCRATCH_DIR}/clean_bg_chill.wav"
output_mp4 = f"{SCRATCH_DIR}/shorts_01_clean_master.mp4"

# Generate high quality ambient chill track
print("Synthesizing clean ambient chill background music...")
subprocess.run([
    FFMPEG, "-y", "-f", "lavfi",
    "-i", "aevalsrc=sin(2*PI*261.63*t)*0.15+sin(2*PI*329.63*t)*0.1+sin(2*PI*392.00*t)*0.1:s=22050",
    "-af", "lowpass=f=700,aecho=0.8:0.88:60|120:0.4|0.2,volume=0.35",
    "-t", str(duration), bg_music_wav
], check=True)

d1 = 10.0
d2 = 10.0
d3 = 10.0

cmd = [
    FFMPEG, "-y",
    "-loop", "1", "-t", str(d1), "-i", img1,
    "-loop", "1", "-t", str(d2), "-i", img2,
    "-loop", "1", "-t", str(d3), "-i", img3,
    "-i", bg_music_wav,
    "-filter_complex", "[0:v][1:v][2:v]concat=n=3:v=1:a=0[outv]",
    "-map", "[outv]", "-map", "3:a",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
    "-c:a", "aac", "-b:a", "192k", "-shortest",
    output_mp4
]

print("Rendering clean master MP4 video (Ready for Southern Voiceover)...")
subprocess.run(cmd, check=True)
print(f"✅ Clean master video saved at: {output_mp4}")
