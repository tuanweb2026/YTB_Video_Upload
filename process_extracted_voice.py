import os
import subprocess

SCRATCH_DIR = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management"
BRAIN_DIR = "/Users/abc/.gemini/antigravity/brain/f1b616c4-34df-4bce-8ba5-f93a710452fb"
FFMPEG = "/Users/abc/bin/ffmpeg"

input_audio = f"{SCRATCH_DIR}/extracted_voice.mp3"
trimmed_audio = f"{SCRATCH_DIR}/extracted_trimmed.wav"
bg_music_wav = f"{SCRATCH_DIR}/clean_bg_chill.wav"
mixed_audio = f"{SCRATCH_DIR}/extracted_mixed_audio.wav"
output_mp4 = f"{SCRATCH_DIR}/shorts_01_extracted_voice_final.mp4"

img1 = f"{BRAIN_DIR}/youtube_shorts_thumbnail_1787412760992.jpg"
img2 = f"{BRAIN_DIR}/shorts_scene2_phone_1787412813911.jpg"
img3 = f"{BRAIN_DIR}/shorts_scene3_headphones_1787412829319.jpg"

# 1. Inspect total audio duration
res = subprocess.run([FFMPEG, "-i", input_audio], stderr=subprocess.PIPE, text=True)
print(res.stderr[:500])

# 2. Extract first 30 seconds of high quality voiceover from downloaded MP3
target_duration = 30.0
print(f"1. Extracting {target_duration}s of voiceover from {input_audio}...")
subprocess.run([
    FFMPEG, "-y", "-ss", "00:00:05", "-t", str(target_duration),
    "-i", input_audio, "-af", "highpass=f=100,lowpass=f=7000,volume=1.4",
    trimmed_audio
], check=True)

# 3. Mix extracted voice with soft chill background music
print("2. Mixing extracted voiceover with ambient chill music...")
subprocess.run([
    FFMPEG, "-y", "-i", trimmed_audio, "-i", bg_music_wav,
    "-filter_complex", "[0:a]volume=1.4[a0];[1:a]volume=0.2[a1];[a0][a1]amix=inputs=2:duration=first[aout]",
    "-map", "[aout]", mixed_audio
], check=True)

# 4. Render 9:16 Vertical Video
d1 = target_duration * 0.33
d2 = target_duration * 0.33
d3 = target_duration * 0.34

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

print("3. Rendering final Shorts Video with extracted voice...")
subprocess.run(cmd, check=True)
print(f"🎉 FINAL EXTRACTED VOICE SHORTS VIDEO SAVED AT: {output_mp4}")
