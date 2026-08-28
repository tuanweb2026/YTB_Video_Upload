#!/usr/bin/env python3
"""
Pre-render all 5 upcoming videos for Day 3 (24/08/2026) locally for preview on the web dashboard.
"""

import os
import sys
import time
from datetime import datetime
from content_generator import get_slot_content
from video_builder import build_video_for_content

SCRATCH_DIR = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management"
OUTPUT_QUEUE = f"{SCRATCH_DIR}/output_queue"

def render_all_slots_for_day_3():
    day = 3
    slots = ["slot_08am", "slot_11am", "slot_18pm", "slot_20pm", "slot_2130pm"]
    
    print("\n" + "="*70)
    print(f"🎬 PRE-RENDERING ALL 5 VIDEOS FOR DAY 3 (24/08/2026) FOR LOCAL PREVIEW")
    print("="*70)
    
    for slot in slots:
        print(f"\n⚡ Processing slot: {slot}...")
        content = get_slot_content(day=day, slot_key=slot)
        
        filename = f"shorts_day_{day}_{slot}.mp4"
        out_path = os.path.join(OUTPUT_QUEUE, filename)
        
        # Check if already rendered
        if os.path.exists(out_path):
            print(f"✅ Already rendered: {filename}")
            continue
            
        print(f"🎥 Rendering video: {filename}...")
        build_video_for_content(content, filename)
        print(f"🎉 Successfully rendered: {filename}")

if __name__ == "__main__":
    render_all_slots_for_day_3()
