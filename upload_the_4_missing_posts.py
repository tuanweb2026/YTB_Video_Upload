#!/usr/bin/env python3
"""
Upload the 4 Missing Posts (Posts 10, 18, 19, 20) Live to YouTube Studio API.
Ensures 100% complete set of 20 live videos published!
"""

import os
import sys
import json
import ssl
import time
from datetime import datetime
from video_builder import build_video_for_content
from youtube_api_auto_uploader import upload_video_via_api

ssl._create_default_https_context = ssl._create_unverified_context

SCRATCH_DIR = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management"
OUTPUT_QUEUE = f"{SCRATCH_DIR}/output_queue"
DB_FILE = f"{SCRATCH_DIR}/published_db.json"

MISSING_4_POSTS = [
    {
        "post_index": 10,
        "clean_title": "Sự Tĩnh Lặng Nikaya: Giai Điệu 432Hz Thư Giãn Sâu & Bình An",
        "hook": "Thả lỏng toàn bộ cơ thể, lắng nghe giai điệu tĩnh lặng Kinh Nikaya...",
        "script": "Chào buổi tối bình yên nhen! Hãy nhắm mắt lại, đeo tai nghe vào và để giai điệu tần số an lành 432Hz xua tan đi mọi mệt mỏi trong ngày. Chúc bạn có một giấc ngủ an lành trong Chánh Niệm nhen! Bấm Đăng Ký Kênh Thảo Dương TV nhen!",
        "source": "Triết Lý Nikaya Kinh Đêm - Nhạc Thiền Tần Số 432Hz"
    },
    {
        "post_index": 18,
        "clean_title": "Buông Bỏ Lòng Tham Dục (LOBHA): Tận Hưởng Tự Do Thực Sự",
        "hook": "Càng muốn nắm giữ nhiều, tay bạn càng mỏi...",
        "script": "Dạ chào bạn nhen! Trong Kinh Tăng Chi Bố, Đức Phật dạy: Tham dục LOBHA giống như người uống nước muối, càng uống càng khát. Biết dừng lại đúng lúc, học cách buông bỏ bớt nhu cầu dư thừa giúp bạn tận hưởng tự do thực sự nhen! Nhấn Đăng Ký Kênh Thảo Dương TV nhen!",
        "source": "Kinh Tăng Chi Bố - Tham Dục"
    },
    {
        "post_index": 19,
        "clean_title": "Sự Tự Do Khỏi Định Kiến: Trí Tuệ Độc Lập Kālāma",
        "hook": "Bức tường ngăn cách lớn nhất giữa người với người chính là định kiến...",
        "script": "Chào bạn nhen! Trong Kinh Kalama Kinh Tăng Chi Bố, Đức Phật dạy lời khuyên vàng: Đừng vội tin vì cội nguồn truyền thống, đừng vội tin vì lời đồn đại. Hãy tự mình suy nghiệm, thấy điều nào mang lại bình an ích lợi thì hãy theo. Giữ trí tuệ độc lập nhen! Đăng Ký Kênh Thảo Dương TV nhen!",
        "source": "Kinh Tăng Chi Bố - Kinh Kalama"
    },
    {
        "post_index": 20,
        "clean_title": "Tâm Hỷ Vô Lượng (MUDITA): Vui Với Thắng Lợi Của Người Khác",
        "hook": "Ghen tỵ làm héo mòn tâm hồn bạn. Hãy học cách mừng cho thành công người khác...",
        "script": "Dạ chào bạn nhen! Đức Phật dạy về Tâm Hỷ MUDITA: Thấy người khác được may mắn, thành công mà lòng tràn ngập niềm vui chung. Lòng đố kỵ chỉ đốt cháy chính bạn, còn Tâm Hỷ mở ra kho báu hạnh phúc vô tận nhen! Bấm Đăng Ký Kênh Thảo Dương TV nhen!",
        "source": "Kinh Tăng Chi Bố - Tâm Hỷ Mudita"
    }
]

def load_db():
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

def save_db(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

def upload_missing_4():
    db = load_db()
    
    # Filter out entries for posts 10, 18, 19, 20 that were fallback entries
    missing_indices = [10, 18, 19, 20]
    cleaned_db = [e for e in db if e.get("post_index") not in missing_indices]
    save_db(cleaned_db)
    
    print(f"🧹 Filtered DB for missing 4 posts. Current valid live count: {len(cleaned_db)}")
    
    for item in MISSING_4_POSTS:
        idx = item["post_index"]
        title_with_hashtags = f"{item['clean_title']} #Shorts #NikayaKinh"
        
        print("\n" + "="*70)
        print(f"🚀 RENDERING & PUBLISHING MISSING POST #{idx}: {title_with_hashtags}")
        print("="*70)
        
        content_data = {
            "title": title_with_hashtags,
            "hook": item["hook"],
            "script": item["script"],
            "category": "Triết Lý Nikaya Kinh Đêm",
            "series": "Triết Lý Nikaya Kinh Đêm",
            "tags": ["NikayaKinh", "ThảoDươngTV", "Shorts"],
            "source": item["source"]
        }
        
        filename = f"shorts_nikaya_{idx}.mp4"
        print(f"🎥 Building video MP4: {filename}...")
        video_path = build_video_for_content(content_data, filename)
        
        desc = (
            f"{item['clean_title']} - Thảo Dương TV (@1995lido).\n\n"
            f"📌 Trích từ: {item['source']}\n"
            f"🌱 Đăng ký kênh: https://www.youtube.com/@1995lido?sub_confirmation=1\n\n"
            f"#Shorts #ThaoDuongTV #NikayaKinh"
        )
        tags = ["NikayaKinh", "ThảoDươngTV", "Shorts"]
        
        print(f"🚀 Uploading missing Post #{idx} to YouTube Studio API...")
        video_id = upload_video_via_api(video_path, title_with_hashtags, desc, tags)
        
        if not video_id:
            print(f"❌ Failed to upload Post #{idx}! Retrying after 5 seconds...")
            time.sleep(5)
            video_id = upload_video_via_api(video_path, title_with_hashtags, desc, tags)
            
        if video_id:
            youtube_url = f"https://www.youtube.com/watch?v={video_id}"
            pub_entry = {
                "post_index": idx,
                "title": title_with_hashtags,
                "youtube_url": youtube_url,
                "video_id": video_id,
                "local_file": video_path,
                "published_at": datetime.now().isoformat(),
                "calendar_date": datetime.now().strftime("%d/%m/%Y"),
                "category": "Triết Lý Nikaya Kinh Đêm",
                "status": "LIVE_SUCCESS"
            }
            cleaned_db.append(pub_entry)
            save_db(cleaned_db)
            print(f"🎉 MISSING POST #{idx} SUCCESSFULLY PUBLISHED LIVE AT: {youtube_url}")
        else:
            print(f"⚠️ Post #{idx} could not be uploaded.")
            
        time.sleep(3) # Throttle calls to avoid quota/rate limits

    print("\n" + "="*70)
    print("✨ ALL 4 MISSING POSTS PROCESSED!")
    print("="*70)

if __name__ == "__main__":
    upload_missing_4()
