#!/usr/bin/env python3
"""
Dedicated Auto-Pilot Video Builder & Publisher for Channel 2: @ThaoDuongAnimation
Creates funny, vibrant, highly engaging vertical Shorts for Animation & Comedy!
"""

import os
import sys
import json
import time
from datetime import datetime
from video_builder import build_video_for_content
from youtube_api_auto_uploader import upload_video_via_api

SCRATCH_DIR = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management"
ANIMATION_DB = f"{SCRATCH_DIR}/animation_posts.json"
PUBLISHED_ANIMATION_DB = f"{SCRATCH_DIR}/published_animation_db.json"

def load_animation_posts():
    if os.path.exists(ANIMATION_DB):
        with open(ANIMATION_DB, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def load_published_animation():
    if os.path.exists(PUBLISHED_ANIMATION_DB):
        try:
            with open(PUBLISHED_ANIMATION_DB, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return []

def save_published_animation(db):
    with open(PUBLISHED_ANIMATION_DB, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

def build_and_publish_animation(post_index=1):
    posts = load_animation_posts()
    target_post = None
    for p in posts:
        if p.get("post_index") == post_index:
            target_post = p
            break
            
    if not target_post:
        print(f"⚠️ Post #{post_index} not found in Animation DB!")
        return False
        
    print("\n" + "="*70)
    print(f"🎬 BUILDING & PUBLISHING ANIMATION SHORT #{post_index} FOR @ThaoDuongAnimation")
    print("="*70)
    
    content_data = {
        "title": target_post["title"],
        "hook": target_post["hook"],
        "script": target_post["script"],
        "category": "Thảo Dương Animation",
        "series": "Thảo Dương Animation",
        "tags": target_post["tags"]
    }
    
    filename = f"animation_short_{post_index}.mp4"
    video_path = build_video_for_content(content_data, filename)
    
    desc = (
        f"{target_post['title']} - Thảo Dương Animation (@ThaoDuongAnimation).\n\n"
        f"😂 Đăng ký kênh giải trí xả stress: https://www.youtube.com/@ThaoDuongAnimation?sub_confirmation=1\n\n"
        f"#Shorts #ThaoDuongAnimation #HaiHuoc #HoatHinh"
    )
    
    print(f"🚀 Uploading Animation Short #{post_index} to YouTube Studio API...")
    video_id = upload_video_via_api(video_path, target_post["title"], desc, target_post["tags"])
    
    youtube_url = f"https://www.youtube.com/watch?v={video_id}" if video_id else f"https://www.youtube.com/@ThaoDuongAnimation"
    
    pub_db = load_published_animation()
    pub_entry = {
        "post_index": post_index,
        "title": target_post["title"],
        "youtube_url": youtube_url,
        "video_id": video_id or "READY_TO_POST",
        "local_file": video_path,
        "published_at": datetime.now().isoformat(),
        "channel": "@ThaoDuongAnimation"
    }
    pub_db.append(pub_entry)
    save_published_animation(pub_db)
    print(f"🎉 ANIMATION SHORT #{post_index} PROCESSED AT: {youtube_url}")
    return youtube_url

if __name__ == "__main__":
    build_and_publish_animation(1)
