#!/usr/bin/env python3
"""
Pre-Render Upcoming Videos Generator for @1995lido (Thảo Dương TV)
Pre-renders MP4 video files for upcoming day (Day 4: 25/08/2026 - THỨ BA)
into output_queue/ for user review in local dashboard.
"""

import os
import sys
import json
import ssl
from content_generator import get_slot_content
from video_builder import build_video_for_content

ssl._create_default_https_context = ssl._create_unverified_context

SCRATCH_DIR = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management"
OUTPUT_QUEUE = f"{SCRATCH_DIR}/output_queue"

def pre_render_upcoming(day=4):
    os.makedirs(OUTPUT_QUEUE, exist_ok=True)
    slots = ["slot_08am", "slot_11am", "slot_18pm"]
    
    rendered_files = []
    print(f"🎬 Pre-rendering upcoming videos for Day {day} (25/08/2026)...")
    
    for slot_key in slots:
        content = get_slot_content(day=day, slot_key=slot_key)
        filename = f"shorts_day_{day}_{slot_key}.mp4"
        print(f"-> Rendering Day {day} [{content['slot_time']}] - {content['title']}...")
        video_path = build_video_for_content(content, filename)
        rendered_files.append({
            "day": day,
            "slot_key": slot_key,
            "slot_time": content["slot_time"],
            "series": content["series"],
            "title": content["title"],
            "script": content["script"],
            "video_path": video_path,
            "filename": filename
        })
        
    print("✅ PRE-RENDERING FOR UPCOMING DAY COMPLETED SUCCESSFULLY!")
    return rendered_files

if __name__ == "__main__":
    pre_render_upcoming(day=4)
