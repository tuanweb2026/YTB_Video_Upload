#!/usr/bin/env python3
"""
Master Auto-Pilot Runner & Recovery (Backfiller) Script for Thảo Dương TV (@1995lido)
Designed to:
1. Check published_db.json and upload any missed slots for today (recovery/backfill).
2. Generate, render, and upload the current scheduled slot.
3. Proactively pre-render all 5 slot videos for the NEXT day for local web preview.
"""

import os
import sys
import json
import time
from datetime import datetime, timedelta
from content_generator import get_slot_content
from video_builder import build_video_for_content
from youtube_api_auto_uploader import upload_video_via_api

SCRATCH_DIR = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management"
DB_FILE = f"{SCRATCH_DIR}/published_db.json"
OUTPUT_QUEUE = f"{SCRATCH_DIR}/output_queue"

SLOT_TIMES = {
    "slot_08am": {"hour": 8, "minute": 0},
    "slot_11am": {"hour": 11, "minute": 0},
    "slot_18pm": {"hour": 18, "minute": 0},
    "slot_20pm": {"hour": 20, "minute": 0},
    "slot_2130pm": {"hour": 21, "minute": 30}
}

def load_published_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return []

def save_published_db(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

def get_day_number(date_obj):
    # Day 1 is 22/08/2026
    start_date = datetime(2026, 8, 22)
    delta = date_obj - start_date
    return delta.days + 1

def backfill_missed_slots():
    print("🔄 Checking for missed slots today to backfill/recover...")
    now = datetime.now()
    today_str = now.strftime("%d/%m/%Y")
    day_num = get_day_number(datetime(now.year, now.month, now.day))
    
    db = load_published_db()
    
    # Collect slots published today
    published_slots_today = set()
    for entry in db:
        if entry.get("calendar_date") == today_str and entry.get("status") == "LIVE_SUCCESS":
            # Map title or category back to slot if stored, or we can just infer by slot key
            slot = entry.get("slot")
            if slot:
                published_slots_today.add(slot)
                
    for slot_key, time_info in SLOT_TIMES.items():
        slot_time = now.replace(hour=time_info["hour"], minute=time_info["minute"], second=0, microsecond=0)
        
        # If the slot time has passed today and it has not been published, backfill it!
        if now > slot_time and slot_key not in published_slots_today:
            print(f"⚠️ MISSED SLOT DETECTED: {slot_key} (Scheduled: {time_info['hour']}:{time_info['minute']:02d}). Recovering now...")
            success = run_upload_for_slot(day_num, slot_key)
            if success:
                published_slots_today.add(slot_key)
            time.sleep(5)

def run_upload_for_slot(day, slot_key):
    today_str = datetime.now().strftime("%d/%m/%Y")
    
    # Check if already published to prevent double posting
    db = load_published_db()
    for entry in db:
        if entry.get("calendar_date") == today_str and entry.get("slot") == slot_key and entry.get("status") == "LIVE_SUCCESS":
            print(f"✅ Slot {slot_key} already published for today.")
            return True
            
    print(f"🚀 Processing Slot {slot_key} for Day {day}...")
    content = get_slot_content(day=day, slot_key=slot_key)
    
    filename = f"shorts_day_{day}_{slot_key}.mp4"
    video_path = os.path.join(OUTPUT_QUEUE, filename)
    
    # Render if not exists
    if not os.path.exists(video_path):
        video_path = build_video_for_content(content, filename)
        
    print(f"📡 Uploading to YouTube: {content['title']}...")
    video_id = upload_video_via_api(
        video_path,
        content["title"],
        content["description"],
        content["tags"]
    )
    
    if video_id:
        youtube_url = f"https://www.youtube.com/watch?v={video_id}"
        new_entry = {
            "post_index": content.get("post_index"),
            "day": day,
            "slot": slot_key,
            "title": content["title"],
            "youtube_url": youtube_url,
            "video_id": video_id,
            "local_file": video_path,
            "published_at": datetime.now().isoformat(),
            "calendar_date": today_str,
            "category": content["category"],
            "status": "LIVE_SUCCESS"
        }
        db.append(new_entry)
        save_published_db(db)
        print(f"🎉 Slot {slot_key} successfully published: {youtube_url}")
        return True
    else:
        print(f"❌ Failed to upload Slot {slot_key} to YouTube.")
        return False

def pre_render_next_day_previews():
    next_day_dt = datetime.now() + timedelta(days=1)
    next_day_str = next_day_dt.strftime("%d/%m/%Y")
    day_num = get_day_number(datetime(next_day_dt.year, next_day_dt.month, next_day_dt.day))
    
    print(f"\n🔮 Proactively rendering previews for NEXT DAY: {next_day_str} (Day {day_num})...")
    
    for slot_key in SLOT_TIMES.keys():
        filename = f"shorts_day_{day_num}_{slot_key}.mp4"
        out_path = os.path.join(OUTPUT_QUEUE, filename)
        
        if os.path.exists(out_path):
            continue
            
        print(f"🎥 Pre-rendering: {filename}...")
        content = get_slot_content(day=day_num, slot_key=slot_key)
        build_video_for_content(content, filename)
        print(f"✅ Preview ready: {filename}")

if __name__ == "__main__":
    # Get slot_key from command line arguments if provided
    target_slot = sys.argv[1] if len(sys.argv) > 1 else None
    
    # 1. Run backfill recovery first
    backfill_missed_slots()
    
    # 2. Upload current slot if specified
    if target_slot in SLOT_TIMES:
        now = datetime.now()
        day_num = get_day_number(datetime(now.year, now.month, now.day))
        run_upload_for_slot(day_num, target_slot)
        
    # 3. Always pre-render previews for the next day
    pre_render_next_day_previews()
