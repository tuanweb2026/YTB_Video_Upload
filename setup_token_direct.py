#!/usr/bin/env python3
"""
Direct YouTube Auto Upload Executor
Uses saved token.json to perform live video uploads directly to @1995lido.
"""

import os
import sys
import json
from content_generator import get_slot_content
from youtube_api_auto_uploader import upload_video_via_api

SCRATCH_DIR = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management"
VIDEO_PATH = f"{SCRATCH_DIR}/output_queue/shorts_day_1.mp4"

def execute_live_upload():
    content = get_slot_content(1, "slot_08am")
    print(f"🎬 Initiating Live Upload for: {content['title']}")
    video_id = upload_video_via_api(VIDEO_PATH, content["title"], content["description"], content["tags"])
    if video_id:
        print(f"🎉 SUCCESS! Video is live at: https://www.youtube.com/watch?v={video_id}")
        return video_id
    return None

if __name__ == "__main__":
    execute_live_upload()
