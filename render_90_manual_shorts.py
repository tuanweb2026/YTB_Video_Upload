#!/usr/bin/env python3
"""
Batch Renderer to generate all 90 new videos based on nikaya_30_authentic_posts.json
and save them to output_manual/ folder for automatic uploading.
"""

import os
import sys
import json
import random
from pathlib import Path

# Add project path to python import search path
SCRATCH_DIR = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management"
sys.path.append(SCRATCH_DIR)

from auto_create_daily_videos import build_one_video, load_upload_db, save_upload_db

def main():
    json_path = os.path.join(SCRATCH_DIR, "nikaya_30_authentic_posts.json")
    bg_dir = Path(SCRATCH_DIR) / "studio_backgrounds"
    music_dir = Path(SCRATCH_DIR) / "studio_music"
    output_manual = Path(SCRATCH_DIR) / "output_manual"
    
    os.makedirs(output_manual, exist_ok=True)
    
    if not os.path.exists(json_path):
        print(f"❌ Kịch bản file not found: {json_path}")
        return
        
    with open(json_path, "r", encoding="utf-8") as f:
        posts = json.load(f)
        
    print(f"Loaded {len(posts)} Nikaya script templates.")
    
    bgs = sorted(list(bg_dir.glob("*.jpg")) + list(bg_dir.glob("*.png")) + list(bg_dir.glob("*.webp")))
    musics = sorted(list(music_dir.glob("*.wav")) + list(music_dir.glob("*.mp3")))
    
    if not bgs:
        print("❌ No backgrounds found in studio_backgrounds/")
        return
        
    upload_db = load_upload_db()
    
    # Render all 90 videos sequentially
    for idx, post in enumerate(posts):
        day = post.get("day", idx + 1)
        title = post.get("title", "")
        script = post.get("script", "")
        cat = post.get("category", "Triết Lý Nikaya Kinh Đêm")
        
        # Trim scripts to avoid length exceeding YouTube Shorts limit
        words = script.split()
        if len(words) > 90:
            script = " ".join(words[:85]) + " nhen!"
            
        bg_path = str(bgs[idx % len(bgs)])
        music_path = str(musics[idx % len(musics)]) if musics else ""
        voice = "vi-VN-HoaiMyNeural" if idx % 2 == 0 else "vi-VN-NamMinhNeural"
        tags = ["Thảo Dương TV", "1995lido", "Shorts", "Kinh Nikaya"]
        
        print(f"\n🎥 [{idx+1}/{len(posts)}] Rendering Day {day} video: {title}")
        
        # Customize output name prefix to keep them structured
        # Example: auto_nikaya_day_1_Loi_Song_Biet_Du.mp4
        clean_title = re.sub(r'[^a-zA-Z0-9]', '_', title.lower())
        clean_title = re.sub(r'_+', '_', clean_title).strip('_')
        
        try:
            result = build_one_video(
                title=title,
                script=script,
                voice=voice,
                bg_path=bg_path,
                music_path=music_path,
                tags=tags,
                description=title
            )
            print(f"  ✅ Rendered successfully: {result['video_name']}")
        except Exception as e:
            print(f"  ❌ Error rendering Day {day}: {e}")
            
    print("\n🎉 Batch rendering completed!")

if __name__ == "__main__":
    import re
    main()
