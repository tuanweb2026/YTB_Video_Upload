#!/usr/bin/env python3
"""
Batch Renderer to generate 200 more Nikaya Shorts videos from nikaya_300_authentic_pool.json
and save them directly to output_manual/ folder for automatic 30-min crontab uploading.
"""

import os
import sys
import json
import re
import random
from pathlib import Path

SCRATCH_DIR = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management"
sys.path.append(SCRATCH_DIR)

from auto_create_daily_videos import build_one_video, load_upload_db, save_upload_db

def main():
    json_path = os.path.join(SCRATCH_DIR, "nikaya_300_authentic_pool.json")
    bg_dir = Path(SCRATCH_DIR) / "studio_backgrounds"
    music_dir = Path(SCRATCH_DIR) / "studio_music"
    output_manual = Path(SCRATCH_DIR) / "output_manual"
    
    os.makedirs(output_manual, exist_ok=True)
    
    if not os.path.exists(json_path):
        print(f"❌ Database file not found: {json_path}")
        return
        
    with open(json_path, "r", encoding="utf-8") as f:
        posts = json.load(f)
        
    print(f"Loaded total database of {len(posts)} Nikaya posts.")
    
    bgs = sorted(list(bg_dir.glob("*.jpg")) + list(bg_dir.glob("*.png")) + list(bg_dir.glob("*.webp")))
    musics = sorted(list(music_dir.glob("*.wav")) + list(music_dir.glob("*.mp3")))
    
    if not bgs:
        print("❌ No backgrounds found in studio_backgrounds/")
        return

    # Check existing files in output_manual to avoid duplicates
    existing_files = [f.name for f in output_manual.glob("*.mp4") if f.stat().st_size > 1024]
    print(f"Currently {len(existing_files)} video files in output_manual/.")
    
    # Target rendering the next 200 items (starting from index 83 to 283)
    target_posts = posts[83:283]
    print(f"Queueing {len(target_posts)} new videos for rendering...")
    
    rendered_count = 0
    
    for idx, post in enumerate(target_posts):
        day = post.get("day", 84 + idx)
        title = post.get("title", "").strip()
        script = post.get("script", "").strip()
        cat = post.get("category", "Triết Lý Nikaya Kinh Đêm")
        
        # Clean title for comparison
        clean_name = re.sub(r'[^a-zA-Z0-9]', '_', title.lower())
        clean_name = re.sub(r'_+', '_', clean_name).strip('_')
        
        # Check if already rendered
        if any(clean_name[:25] in f.lower() for f in existing_files):
            print(f"⏭️ Skipping already rendered: {title[:40]}")
            continue
            
        # Ensure script is optimal length for Shorts
        words = script.split()
        if len(words) > 85:
            script = " ".join(words[:80]) + " nhen!"
            
        bg_path = str(bgs[idx % len(bgs)])
        music_path = str(musics[idx % len(musics)]) if musics else ""
        voice = "vi-VN-HoaiMyNeural" if idx % 2 == 0 else "vi-VN-NamMinhNeural"
        tags = ["Thảo Dương TV", "1995lido", "Shorts", "Kinh Nikaya", "Lời Phật Dạy"]
        
        print(f"\n🎥 [{rendered_count+1}/200] (Day {day}) Rendering: {title}")
        
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
            rendered_count += 1
            print(f"  ✅ Rendered OK: {result['video_name']}")
        except Exception as e:
            print(f"  ❌ Error rendering Day {day}: {e}")
            
    print(f"\n🎉 Successfully rendered {rendered_count} new Nikaya Shorts videos into output_manual/!")

if __name__ == "__main__":
    main()
