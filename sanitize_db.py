#!/usr/bin/env python3
"""
Sanitize published_db.json so every entry has explicit post_index (1 to 20)
and clean duplicate entries.
"""

import os
import json

SCRATCH_DIR = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management"
PUBLISHED_DB_FILE = f"{SCRATCH_DIR}/published_db.json"

def sanitize_published_db():
    if not os.path.exists(PUBLISHED_DB_FILE):
        return
        
    with open(PUBLISHED_DB_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    entries = data if isinstance(data, list) else data.get("published", [])
    
    seen_titles = set()
    cleaned_entries = []
    
    # Mapping for first 10 posts based on title
    mapping = {
        "lối sống biết đủ": 1,
        "nhẫn nại": 2,
        "chánh niệm hơi thở": 3,
        "luật nhân quả": 4,
        "tâm từ vô lượng": 5,
        "định luật vô thường": 6,
        "8 ngọn gió đời": 7,
        "chánh ngữ": 8,
        "tự mình là hải đăng": 9,
        "sự tĩnh lặng": 10
    }
    
    for e in entries:
        title = e.get("title", "")
        clean_t = title.split("#")[0].strip().lower()
        
        # Determine post_index if missing
        if "post_index" not in e or not isinstance(e["post_index"], int):
            found_idx = None
            for key, idx in mapping.items():
                if key in clean_t:
                    found_idx = idx
                    break
            if found_idx:
                e["post_index"] = found_idx
            else:
                continue
                
        idx = e["post_index"]
        
        # Deduplicate
        if idx in seen_titles or clean_t in seen_titles:
            print(f"🧹 Removing duplicate entry in published_db: Post #{idx} - {title}")
            continue
            
        seen_titles.add(idx)
        seen_titles.add(clean_t)
        cleaned_entries.append(e)
        
    cleaned_entries.sort(key=lambda x: x.get("post_index", 0))
    
    with open(PUBLISHED_DB_FILE, "w", encoding="utf-8") as f:
        json.dump(cleaned_entries, f, ensure_ascii=False, indent=2)
        
    print(f"✅ Sanitized published_db.json: Total {len(cleaned_entries)} clean unique posts (Posts 1 to {len(cleaned_entries)}).")

if __name__ == "__main__":
    sanitize_published_db()
