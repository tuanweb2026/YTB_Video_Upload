#!/usr/bin/env python3
"""
Expands the Nikaya kịch bản database to 90 posts (Day 1 to 90)
by pulling the high-quality pre-generated posts from nikaya_230_authentic_posts.json
and overwriting nikaya_30_authentic_posts.json.
"""

import os
import json

SCRATCH_DIR = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management"
SOURCE_JSON = os.path.join(SCRATCH_DIR, "nikaya_230_authentic_posts.json")
TARGET_JSON = os.path.join(SCRATCH_DIR, "nikaya_30_authentic_posts.json")

def expand_posts():
    if not os.path.exists(SOURCE_JSON):
        print(f"❌ Source file not found: {SOURCE_JSON}")
        return
        
    with open(SOURCE_JSON, "r", encoding="utf-8") as f:
        all_posts = json.load(f)
        
    print(f"Loaded {len(all_posts)} posts from source database.")
    
    # Slice the first 90 posts
    selected_90 = all_posts[:90]
    
    # Ensure correct day sequence
    for idx, post in enumerate(selected_90):
        post["day"] = idx + 1
        
    with open(TARGET_JSON, "w", encoding="utf-8") as f:
        json.dump(selected_90, f, ensure_ascii=False, indent=2)
        
    print(f"✅ Successfully wrote {len(selected_90)} posts (Day 1 to 90) to {TARGET_JSON}!")

if __name__ == "__main__":
    expand_posts()
