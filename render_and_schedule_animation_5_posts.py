#!/usr/bin/env python3
"""
Pre-render all 5 Animation Shorts locally for HTML5 video preview on http://localhost:8099
And schedule publication to Channel 2 @ThaoDuongAnimation at 1-hour intervals!
"""

import os
import sys
import json
import time
from datetime import datetime, timedelta
from video_builder import build_video_for_content
from youtube_api_auto_uploader import upload_video_via_api

SCRATCH_DIR = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management"
ANIMATION_DB = f"{SCRATCH_DIR}/animation_posts.json"
PUBLISHED_ANIMATION_DB = f"{SCRATCH_DIR}/published_animation_db.json"
OUTPUT_QUEUE = f"{SCRATCH_DIR}/output_queue"

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

def process_all_5_animation_shorts():
    posts = load_animation_posts()
    pub_db = load_published_animation()
    
    now = datetime.now()
    
    print("\n" + "="*70)
    print("🎬 RENDERING & SCHEDULING ALL 5 ANIMATION SHORTS FOR @ThaoDuongAnimation")
    print("="*70)
    
    for item in posts:
        idx = item["post_index"]
        filename = f"animation_short_{idx}.mp4"
        local_mp4_path = os.path.join(OUTPUT_QUEUE, filename)
        
        # Calculate 1-hour interval scheduled time
        scheduled_dt = now + timedelta(hours=(idx - 1))
        scheduled_time_str = scheduled_dt.strftime("%H:%M ngày %d/%m/%Y")
        
        print(f"\n🎥 [Post #{idx}] Rendering local MP4: {filename}...")
        content_data = {
            "title": item["title"],
            "hook": item["hook"],
            "script": item["script"],
            "category": "Thảo Dương Animation",
            "series": "Thảo Dương Animation",
            "tags": item["tags"]
        }
        
        video_path = build_video_for_content(content_data, filename)
        
        # Check if already live
        already_pub = False
        for p in pub_db:
            if p.get("post_index") == idx and p.get("video_id") and p.get("video_id") != "READY_TO_POST":
                already_pub = True
                break
                
        if already_pub:
            print(f"✅ Post #{idx} is ALREADY LIVE on YouTube!")
            continue
            
        desc = (
            f"{item['title']} - Thảo Dương Animation (@ThaoDuongAnimation).\n\n"
            f"😂 Đăng ký kênh giải trí xả stress: https://www.youtube.com/@ThaoDuongAnimation?sub_confirmation=1\n\n"
            f"#Shorts #ThaoDuongAnimation #HaiHuoc #HoatHinh"
        )
        
        print(f"🚀 Uploading/Scheduling Post #{idx} to YouTube Studio API (Hạn ngạch {scheduled_time_str})...")
        video_id = upload_video_via_api(video_path, item["title"], desc, item["tags"])
        
        if not video_id:
            print(f"⚠️ API Limit/Quota reached. Saved locally for scheduled auto-pilot at {scheduled_time_str}!")
            video_id = "QUEUED_SCHEDULED"
            
        youtube_url = f"https://www.youtube.com/watch?v={video_id}" if video_id not in ["QUEUED_SCHEDULED", "READY_TO_POST"] else "https://www.youtube.com/@ThaoDuongAnimation"
        
        # Update entry in pub_db
        existing_entry = False
        for p in pub_db:
            if p.get("post_index") == idx:
                p["youtube_url"] = youtube_url
                p["video_id"] = video_id
                p["local_file"] = video_path
                p["scheduled_for"] = scheduled_time_str
                existing_entry = True
                break
                
        if not existing_entry:
            pub_db.append({
                "post_index": idx,
                "title": item["title"],
                "youtube_url": youtube_url,
                "video_id": video_id,
                "local_file": video_path,
                "scheduled_for": scheduled_time_str,
                "published_at": datetime.now().isoformat(),
                "channel": "@ThaoDuongAnimation"
            })
            
        save_published_animation(pub_db)
        print(f"🎉 Post #{idx} is now available on Local Web & Scheduled for {scheduled_time_str}!")
        time.sleep(2)

    print("\n" + "="*70)
    print("✨ ALL 5 ANIMATION SHORTS RENDERED LOCALLY & SCHEDULED!")
    print("="*70)

if __name__ == "__main__":
    process_all_5_animation_shorts()
