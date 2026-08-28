#!/usr/bin/env python3
"""
High-Fidelity Neural TTS Generator using Microsoft Edge Neural Voice (vi-VN-HoaiMyNeural)
- Voice: vi-VN-HoaiMyNeural (Soft, Natural, Ultra-Realistic Southern Vietnamese Voice)
- 100% Free, high quality, human-like cadence and prosody.
"""

import os
import sys
import json
import ssl
import subprocess
import urllib.request

ssl._create_default_https_context = ssl._create_unverified_context

SCRATCH_DIR = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management"
TEST_AUDIO_MP3 = f"{SCRATCH_DIR}/test_neural_voice.mp3"
TEST_AUDIO_WAV = f"{SCRATCH_DIR}/test_neural_voice.wav"
FFMPEG = "/Users/abc/bin/ffmpeg"

test_text = "Dạ chào bạn nhen! Muốn hoàn thành việc khó mà không bị phân tâm? Thử ngay kỹ thuật Time Boxing này nè. Thảo Dương TV luôn ở bên bạn!"

def generate_edge_neural_voice(text, output_mp3):
    print("🎙️ Synthesizing Ultra-Realistic Southern Voice via Edge Neural (vi-VN-HoaiMyNeural)...")
    # Check if edge-tts CLI or python module is available, or use direct websocket/script
    try:
        cmd = [sys.executable, "-m", "edge_tts", "--voice", "vi-VN-HoaiMyNeural", "--text", text, "--write-media", output_mp3]
        subprocess.run(cmd, check=True)
        print(f"✅ Neural Voice MP3 generated at: {output_mp3}")
        return True
    except Exception as e:
        print(f"edge-tts module not installed: {e}. Installing edge-tts...")
        subprocess.run([sys.executable, "-m", "pip", "install", "edge-tts"], check=False)
        try:
            cmd = [sys.executable, "-m", "edge_tts", "--voice", "vi-VN-HoaiMyNeural", "--text", text, "--write-media", output_mp3]
            subprocess.run(cmd, check=True)
            print(f"✅ Neural Voice MP3 generated at: {output_mp3}")
            return True
        except Exception as ex:
            print(f"edge-tts synthesis note: {ex}")
            return False

if __name__ == "__main__":
    generate_edge_neural_voice(test_text, TEST_AUDIO_MP3)
