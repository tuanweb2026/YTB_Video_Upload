#!/usr/bin/env python3
"""
1-Click Immediate Publisher for @1995lido (Thảo Dương TV)
"""

import os
import subprocess
from content_generator import get_slot_content

SCRATCH_DIR = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management"
VIDEO_PATH = f"{SCRATCH_DIR}/output_queue/shorts_day_1.mp4"

def publish_instant():
    content = get_slot_content(1, "slot_08am")
    
    # 1. Copy Title & Description to macOS Clipboard
    clipboard_text = f"TIÊU ĐỀ:\n{content['title']}\n\nMÔ TẢ:\n{content['description']}\n\nTAGS:\n{', '.join(content['tags'])}\n\nBÌNH LUẬN GHIM:\n{content['pinned_comment']}"
    
    process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    process.communicate(clipboard_text.encode('utf-8'))
    
    print("=" * 60)
    print("🚀 ĐANG MỞ TRANG ĐĂNG BÀI YOUTUBE STUDIO TRỰC TIẾP...")
    print("=" * 60)
    print(f"🎬 Video: {VIDEO_PATH}")
    print(f"📌 Tiêu đề: {content['title']}")
    print(f"📋 Đã sao chép sẵn Tiêu đề + Mô tả vào Khay Nhớ Tạm (Clipboard)!")
    print("-" * 60)
    
    # 2. Open Finder directly at video location
    subprocess.run(["open", "-R", VIDEO_PATH])
    
    # 3. Open YouTube Studio Upload in default Browser
    subprocess.run(["open", "https://studio.youtube.com"])
    
    print("✅ Đã mở YouTube Studio và mở thư mục chứa Video trên máy của bạn!")
    print("👉 Bạn chỉ cần Kéo Thả video vào YouTube Studio và nhấn Dán (Cmd+V) là xong!")
    print("=" * 60)

if __name__ == "__main__":
    publish_instant()
