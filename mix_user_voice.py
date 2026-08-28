import os
import sys
import subprocess

SCRATCH_DIR = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management"
BRAIN_DIR = "/Users/abc/.gemini/antigravity/brain/f1b616c4-34df-4bce-8ba5-f93a710452fb"
FFMPEG = "/Users/abc/bin/ffmpeg"

def mix_user_recording(audio_input_path):
    if not os.path.exists(audio_input_path):
        print(f"❌ File audio {audio_input_path} không tồn tại.")
        return
        
    img1 = f"{BRAIN_DIR}/youtube_shorts_thumbnail_1787412760992.jpg"
    img2 = f"{BRAIN_DIR}/shorts_scene2_phone_1787412813911.jpg"
    img3 = f"{BRAIN_DIR}/shorts_scene3_headphones_1787412829319.jpg"
    bg_music_wav = f"{SCRATCH_DIR}/clean_bg_chill.wav"
    output_mp4 = f"{SCRATCH_DIR}/shorts_01_REAL_HUMAN_VOICE.mp4"

    # Get user audio duration
    res = subprocess.run([FFMPEG, "-i", audio_input_path], stderr=subprocess.PIPE, text=True)
    duration = 25.0
    for line in res.stderr.split('\n'):
        if "Duration" in line:
            parts = line.split("Duration:")[1].split(",")[0].strip().split(":")
            duration = float(parts[0])*3600 + float(parts[1])*60 + float(parts[2])
            break

    print(f"🎧 Độ dài giọng đọc thật: {duration:.2f} giây")

    # Mix user voiceover with background music
    mixed_audio = f"{SCRATCH_DIR}/user_mixed_audio.wav"
    subprocess.run([
        FFMPEG, "-y", "-i", audio_input_path, "-i", bg_music_wav,
        "-filter_complex", "[0:a]volume=1.3[a0];[1:a]volume=0.25[a1];[a0][a1]amix=inputs=2:duration=first[aout]",
        "-map", "[aout]", mixed_audio
    ], check=True)

    # Render final MP4
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

    subprocess.run(cmd, check=True)
    print(f"🎉 VIDEO HOÀN CHỈNH GIỌNG THẬT ĐÃ ĐƯỢC TẠO TẠI: {output_mp4}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        mix_user_recording(sys.argv[1])
    else:
        print("Usage: python3 mix_user_voice.py <path_to_user_audio_file>")
