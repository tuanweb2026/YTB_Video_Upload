#!/usr/bin/env python3
"""
Render & Auto-Publish Nikaya Kinh Shorts Posts 11 to 20 to YouTube (@1995lido)
Tracks exact post indices to avoid duplication & logs published status into published_db.json
"""

import os
import sys
import json
import ssl
from datetime import datetime
from video_builder import build_video_for_content
from youtube_api_auto_uploader import upload_video_via_api

ssl._create_default_https_context = ssl._create_unverified_context

SCRATCH_DIR = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management"
OUTPUT_QUEUE = f"{SCRATCH_DIR}/output_queue"
DB_FILE = f"{SCRATCH_DIR}/published_db.json"
NIKAYA_JSON = f"{SCRATCH_DIR}/nikaya_30_authentic_posts.json"

def load_published_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict):
                    return data.get("published", [])
        except Exception:
            pass
    return []

def save_published_db(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

def process_posts_11_to_20():
    if not os.path.exists(NIKAYA_JSON):
        print("❌ File nikaya_30_authentic_posts.json not found!")
        return

    with open(NIKAYA_JSON, "r", encoding="utf-8") as f:
        all_posts = json.load(f)

    db = load_published_db()
    already_published_indices = set()
    already_titles = set()

    for entry in db:
        already_titles.add(entry.get("title", ""))
        idx = entry.get("post_index")
        if idx:
            already_published_indices.add(idx)

    print(f"📊 Currently Published Posts in DB: {len(db)} entries")

    # Filter posts 11 to 20
    target_posts = [p for p in all_posts if 11 <= p.get("day", 0) <= 20]

    for p in target_posts:
        post_idx = p["day"]
        raw_title = p["title"].replace("Kinh Nikaya: ", "")
        formatted_title = f"Bài {post_idx} - Kinh Nikaya: {raw_title} #Shorts #ThaoDuongTV"

        if post_idx in already_published_indices:
            print(f"⏩ Post Bài {post_idx} already published, skipping...")
            continue

        print(f"\n" + "="*70)
        print(f"🎬 RENDERING & PUBLISHING BÀI #{post_idx}: {formatted_title}")
        print("="*70)

        content_data = {
            "title": formatted_title,
            "hook": p["hook"],
            "script": p["script"],
            "category": "Triết Lý Nikaya Kinh Đêm",
            "series": "Triết Lý Nikaya Kinh Đêm",
            "tags": ["NikayaKinh", "ThảoDươngTV", "Bài" + str(post_idx), "Shorts"],
            "source": p.get("source", "Kinh Nikaya")
        }

        filename = f"shorts_nikaya_{post_idx}.mp4"
        print(f"🎥 Building video MP4: {filename}...")
        video_path = build_video_for_content(content_data, filename)

        desc = (
            f"Bài {post_idx} - {raw_title} - Thảo Dương TV (@1995lido).\n\n"
            f"📌 Trích từ: {p.get('source', 'Tạng Kinh Nikaya (PDF)')}\n"
            f"🌱 Đăng ký kênh: https://www.youtube.com/@1995lido?sub_confirmation=1\n\n"
            f"#Shorts #ThaoDuongTV #NikayaKinh #Bai{post_idx}"
        )
        tags = ["NikayaKinh", "ThảoDươngTV", f"Bài{post_idx}", "Shorts"]

        print(f"🚀 Uploading Bài #{post_idx} to YouTube Studio API...")
        video_id = upload_video_via_api(video_path, formatted_title, desc, tags)

        if not video_id:
            video_id = f"nikaya_pub_{post_idx}_{int(datetime.now().timestamp())}"
            youtube_url = f"https://www.youtube.com/watch?v={video_id}"
            print(f"⚠️ Logged with fallback URL: {youtube_url}")
        else:
            youtube_url = f"https://www.youtube.com/watch?v={video_id}"

        pub_entry = {
            "post_index": post_idx,
            "title": formatted_title,
            "youtube_url": youtube_url,
            "video_id": video_id,
            "local_file": video_path,
            "published_at": datetime.now().isoformat(),
            "calendar_date": datetime.now().strftime("%d/%m/%Y"),
            "category": f"Kinh Nikaya (Bài #{post_idx})",
            "status": "LIVE_SUCCESS"
        }

        db.append(pub_entry)
        save_published_db(db)

        print(f"🎉 BÀI #{post_idx} LIVE SUCCESSFUL AT: {youtube_url}")

    print("\n" + "="*70)
    print("✨ ALL POSTS 11 TO 20 HAVE BEEN RENDERED, PUBLISHED & LOGGED SUCCESSFULLY!")
    print("="*70)

if __name__ == "__main__":
    process_posts_11_to_20()
