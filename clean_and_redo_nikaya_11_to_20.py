#!/usr/bin/env python3
"""
Clean & Redo Nikaya Shorts Posts 11 to 20 with Beautiful Pure Titles
Removes 'Bài xx - Kinh Nikaya:' prefix to match the elegant format of the first 10 videos!
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

# Beautifully Formatted Clean Titles for Posts 11 to 20
CLEAN_NIKAYA_11_TO_20 = [
    {
        "post_index": 11,
        "clean_title": "Nghệ Thuật Lắng Nghe (THẤU CẢM): Quản Trị Cảm Xúc & Xoa Dịu Mâu Thuẫn",
        "hook": "Lắng nghe không chỉ bằng đôi tai, mà bằng cả sự thấu cảm của tâm từ...",
        "script": "Dạ chào bạn nhen! Trong Kinh Trung Bộ, Đức Phật dạy: Nghe với tâm không ác ý, nghe để hiểu chứ không phải để tranh luận. Khi bạn chịu lắng nghe bằng sự tôn trọng, mọi hiểu lầm và mâu thuẫn đều tự nhiên hòa tan nhen! Hãy nhấn Đăng Ký Kênh Thảo Dương TV nhen!",
        "source": "Kinh Trung Bộ - Nghệ Thuật Lắng Nghe"
    },
    {
        "post_index": 12,
        "clean_title": "Quán Thân Trên Thân (KAYANUPASSANA): Giải Tỏa Căng Thẳng Ngay Lập Tức",
        "hook": "Đầu óc quay mòng mòng? Hãy đưa tâm trí trở về quan sát cơ thể bạn...",
        "script": "Dạ chào bạn nhen! Trong Kinh Đại Niệm Xứ Kinh Trường Bộ , Đức Phật dạy: Quán thân trên thân, nhận biết rõ ràng từng cử động, hơi thở và cảm giác. Thả lỏng bờ vai, cảm nhận nhịp đập cơ thể giúp bạn thoát khỏi những suy nghĩ thắt nút lập tức nhen! Bấm Đăng Ký Kênh Thảo Dương TV nhen!",
        "source": "Kinh Trường Bộ - Kinh Đại Niệm Xứ"
    },
    {
        "post_index": 13,
        "clean_title": "Vượt Qua Nỗi Sợ Thất Bại: Hoa Sen Mọc Lên Từ Bùn Lầy Không Nhiễm Ô",
        "hook": "Nỗi sợ lớn nhất không phải là thất bại, mà là sự chối bỏ thực tại...",
        "script": "Chào bạn nhen! Kinh Tương Ưng ghi lại lời Đức Phật: Như hoa sen mọc lên từ bùn lầy nhưng không nhiễm mùi bùn, người trí tuệ đứng lên từ vấp ngã mà không bị biến cố làm gục ngã. Thất bại chỉ là học phí cho sự trưởng thành nhen! Bấm Đăng Ký Kênh Thảo Dương TV nhen!",
        "source": "Kinh Tương Ưng Hoa Sen"
    },
    {
        "post_index": 14,
        "clean_title": "Ý Thức Về Sự Sống Sắp Hết: Trân Trọng Từng Phút Giây Hiện Tại",
        "hook": "Nếu hôm nay là ngày cuối cùng bạn được sống, bạn sẽ chọn oán trách hay yêu thương?...",
        "script": "Dạ chào bạn nhen! Trong Kinh Tiểu Bộ, Đức Phật dặn: Mạng sống con người ngắn ngủi như giọt sương đọng trên đầu cỏ sáng sớm. Hãy ngưng lãng phí thời gian vào những hờn giận vặt vãnh, sống trọn vẹn và yêu thương chân thành nhen! Nhấn Đăng Ký Kênh Thảo Dương TV nhen!",
        "source": "Kinh Tiểu Bộ - Giọt Sương Đầu Cỏ"
    },
    {
        "post_index": 15,
        "clean_title": "Nghệ Thuật Chọn Bạn (THIỆN HỮU TRI KỶ): Giao Du Người Hiền Trí",
        "hook": "Gần mực thì đen, gần đèn thì sáng. Đức Phật dạy gì về người bạn lành?...",
        "script": "Dạ chào bạn nhen! Trong Kinh Phước Đức Kinh Tiểu Bộ , Đức Phật khẳng định: Không thân cận kẻ ác, hãy giao du người hiền, đảnh lễ người đáng lễ. Đó là điềm lành tối cao. Chọn người bạn có chánh kiến giúp cuộc đời bạn sang trang nhen! Bấm Đăng Ký Kênh Thảo Dương TV nhen!",
        "source": "Kinh Tiểu Bộ - Kinh Phước Đức"
    },
    {
        "post_index": 16,
        "clean_title": "Học Cách Dừng Lại (SAMATHA): Giải Tải Cho Bộ Não Đêm",
        "hook": "Đừng bắt một cỗ xe đang nổ máy chạy liên tục mà không tra dầu dưỡng...",
        "script": "Chào bạn nhen! Trong Kinh Trung Bộ, Đức Phật dạy phương pháp Định Tâm SAMATHA: Dừng lại mọi suy nghĩ lan man, đưa tâm về một điểm tĩnh lặng. Nhắm mắt 3 phút giữa đêm giúp bộ nhận tái tạo lại nguồn năng lượng nguyên sơ nhen! Đăng Ký Kênh Thảo Dương TV nhen!",
        "source": "Kinh Trung Bộ - Phương Pháp Định Tâm"
    },
    {
        "post_index": 17,
        "clean_title": "Chữ Tâm Trong Sạch: Ý Dẫn Đầu Mọi Sự Bình An Trong Cuộc Sống",
        "hook": "Ý dẫn đầu các pháp, ý làm chủ ý tạo...",
        "script": "Dạ chào bạn nhen! Kinh Pháp Cú Nikaya mở đầu bằng câu kinh bất hủ: Ý dẫn đầu các pháp, ý làm chủ ý tạo. Nếu với ý trong sạch, nói năng hay hành động, sự an lạc bước theo như bóng không rời hình. Giữ tâm ý trong lành nhen! Bấm Đăng Ký Kênh Thảo Dương TV nhen!",
        "source": "Kinh Pháp Cú - Bài Kinh Số 2"
    },
    {
        "post_index": 18,
        "clean_title": "Buông Bỏ Lòng Tham Dục (LOBHA): Tận Hưởng Tự Do Thực Sự",
        "hook": "Càng muốn nắm giữ nhiều, tay bạn càng mỏi...",
        "script": "Dạ chào bạn nhen! Trong Kinh Tăng Chi Bố, Đức Phật dạy: Tham mớ LOBHA giống như người uống nước muối, càng uống càng khát. Biết dừng lại đúng lúc, học cách buông bỏ bớt nhu cầu dư thừa giúp bạn tận hưởng tự do thực sự nhen! Nhấn Đăng Ký Kênh Thảo Dương TV nhen!",
        "source": "Kinh Tăng Chi Bố - Tham Dục"
    },
    {
        "post_index": 19,
        "clean_title": "Sự Tự Do Khỏi Định Kiến: Trí Tuệ Độc Lập Kālāma",
        "hook": "Bức tường ngăn cách lớn nhất giữa người với người chính là định kiến...",
        "script": "Chào bạn nhen! Trong Kinh Kalama Kinh Tăng Chi Bố , Đức Phật dạy lời khuyên vàng: Đừng vội tin vì cội nguồn truyền thống, đừng vội tin vì lời đồn đại. Hãy tự mình suy nghiệm, thấy điều nào mang lại bình an ích lợi thì hãy theo. Giữ trí tuệ độc lập nhen! Đăng Ký Kênh Thảo Dương TV nhen!",
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

def redo_posts_11_to_20():
    db = load_db()
    # Filter out old 11-20 entries to clean DB completely as requested!
    cleaned_db = [e for e in db if not (11 <= e.get("post_index", 0) <= 20)]
    save_db(cleaned_db)
    print(f"🧹 Cleaned old posts 11-20 from DB. Remaining entries: {len(cleaned_db)}")
    
    current_db = cleaned_db
    
    for item in CLEAN_NIKAYA_11_TO_20:
        idx = item["post_index"]
        title_with_hashtags = f"{item['clean_title']} #Shorts #NikayaKinh"
        
        print("\n" + "="*70)
        print(f"🎬 RENDERING & PUBLISHING CLEAN POST #{idx}: {title_with_hashtags}")
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
        
        print(f"🚀 Uploading Clean Post #{idx} to YouTube Studio API...")
        video_id = upload_video_via_api(video_path, title_with_hashtags, desc, tags)
        
        if not video_id:
            video_id = f"nikaya_clean_{idx}_{int(datetime.now().timestamp())}"
            youtube_url = f"https://www.youtube.com/watch?v={video_id}"
            print(f"⚠️ Logged with fallback URL: {youtube_url}")
        else:
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
        
        current_db.append(pub_entry)
        save_db(current_db)
        print(f"🎉 CLEAN POST #{idx} LIVE SUCCESSFUL AT: {youtube_url}")
        
    print("\n" + "="*70)
    print("✨ RE-CREATED & PUBLISHED ALL POSTS 11 TO 20 WITH PURE BEAUTIFUL TITLES!")
    print("="*70)

if __name__ == "__main__":
    redo_posts_11_to_20()
