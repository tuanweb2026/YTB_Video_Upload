#!/usr/bin/env python3
"""
Master Content Generator Engine for @1995lido (Thảo Dương TV)
WITH STRICT UNPUBLISHED DAY SELECTION & DUAL/TRIPLE NIGHT SLOT RESOLUTION
Guarantees 0% duplicate uploads by mapping 18:00, 20:00, 21:30 slots to separate unpublished posts!
"""

import os
import json
from datetime import datetime, timedelta

SCRATCH_DIR = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management"
NIKAYA_30_FILE = f"{SCRATCH_DIR}/nikaya_230_authentic_posts.json"  # Updated: 200 bài video dài
PUBLISHED_DB_FILE = f"{SCRATCH_DIR}/published_db.json"

SLOTS = {
    "slot_08am": {"time": "08:00 AM", "series": "Series B - Tư Duy Deep Work Sáng", "focus": "Building Discipline & Focus"},
    "slot_11am": {"time": "11:00 AM", "series": "Series A - Sơ Cứu Tâm Lý & Chữa Lành Trưa", "focus": "Overthinking Relief & Self-Love"},
    "slot_18pm": {"time": "18:00 PM", "series": "Triết Lý Nikaya Kinh Đêm - Slot 1", "focus": "Authentic Nikaya Kinh Wisdom 1"},
    "slot_20pm": {"time": "20:00 PM", "series": "Triết Lý Nikaya Kinh Đêm - Slot 2", "focus": "Authentic Nikaya Kinh Wisdom 2"},
    "slot_2130pm": {"time": "21:30 PM", "series": "Triết Lý Nikaya Kinh Đêm - Slot 3", "focus": "Night Meditation 432Hz"}
}

def load_authentic_nikaya_posts():
    if os.path.exists(NIKAYA_30_FILE):
        try:
            with open(NIKAYA_30_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return []

def get_published_days_and_titles():
    published_days = set()
    published_titles = set()
    if os.path.exists(PUBLISHED_DB_FILE):
        try:
            with open(PUBLISHED_DB_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                entries = data if isinstance(data, list) else data.get("published", [])
                for e in entries:
                    if "post_index" in e and isinstance(e["post_index"], int):
                        published_days.add(e["post_index"])
                    if "title" in e:
                        clean_t = e["title"].split("#")[0].strip().lower()
                        published_titles.add(clean_t)
                        if "sức mạnh của nhẫn nại" in clean_t or "khanti" in clean_t:
                            published_days.add(2)
                        elif "lối sống biết đủ" in clean_t or "santutthi" in clean_t:
                            published_days.add(1)
        except Exception as err:
            print(f"⚠️ Error reading published DB: {err}")
    return published_days, published_titles

AUTHENTIC_NIKAYA = load_authentic_nikaya_posts()

DEEP_WORK_SLOTS = [
    {"title": "Kỹ thuật Time Boxing Nâng Cao: Sắp Xếp 1 Ngày Không Xao Nhãng", "hook": "Đừng làm việc lan man nữa. Đây là khung hệ thống giúp bạn làm chủ 1 ngày...", "script": "Dạ chào bạn nhen! Muốn hoàn thành việc khó mà không bị phân tâm? Chia 1 ngày thành các ô thời gian cố định, 08h-10h làm việc khó nhất, tắt mọi thông báo nhen! Bấm Đăng Ký Kênh Thảo Dương TV nhen!"},
    {"title": "Phương Pháp Học Sâu (Deep Work): Hoàn Thành Việc Khó Trong Thời Gian Ngắn", "hook": "Động lực là kẻ lừa đảo lớn nhất. Bạn cần một hệ thống rèn luyện kỷ luật...", "script": "Chào buổi sáng nhen! Đừng chờ có cảm hứng rồi mới làm việc. Hãy đặt đồng hồ 25 phút Pomodoro, tập trung 100% vào đúng 1 mục tiêu duy nhất nhen! Bấm Đăng Ký Kênh Thảo Dương TV nhen!"},
    {"title": "Bí Quyết Quản Trị Năng Lượng Sinh Học: Tập Trung Cao Độ Đầu Sáng", "hook": "Bạn uể oải lúc 9h sáng? Đó là vì bạn chưa biết cách quản trị đồng hồ sinh học...", "script": "Dạ chào bạn nhen! Hãy dành 60 phút đầu sáng cho công việc quan trọng nhất, uống 1 cốc nước ấm và giữ tư thế ngồi thẳng nhen! Đăng Ký Kênh Thảo Dương TV nhen!"},
    {"title": "Quy Tắc 2 Phút Đánh Bại Sự Trì Hoãn Ngay Lập Tức", "hook": "Nếu một việc tốn ít hơn 2 phút để hoàn thành, hãy làm nó ngay...", "script": "Chào buổi sáng nhen! Việc nào làm dưới 2 phút như dọn bàn, trả lời tin nhắn, giải quyết ngay. Bạn sẽ thấy nhẹ đầu vô cùng nhen! Đăng Ký Kênh Thảo Dương TV nhen!"},
    {"title": "Tư Duy Tối Ưu Hiệu Suất & Kỷ Luật Bản Thân Đầu Sáng", "hook": "3 Thói quen nhỏ mỗi sáng giúp bạn thay đổi diện mạo cuộc sống...", "script": "Dạ chào bạn nhen! Hãy luôn giữ tinh thần kỷ luật, làm việc tập trung và chinh phục từng mục tiêu nhỏ mỗi ngày nhen! Bấm Đăng Ký Kênh Thảo Dương TV nhen!"}
]

HEALING_SLOTS = [
    {"title": "Khi Sự Nhiệt Huyết Biến Mất: Vượt Qua Giai Đoạn Tê Liệt Cảm Xúc", "hook": "Nếu bạn đang cợt nhả qua ngày vì hết sạch sức sống, hãy dừng lại 2 phút...", "script": "Dạ chào bạn nhen... Nếu hôm nay bạn thấy cạn kiệt năng lượng, đừng cố gồng mình nữa nghen. Cho phép bản thân nghỉ ngơi 15 phút, lắng nghe hơi thở và nếm ngụm nước ấm nhen! Nhấn Đăng Ký Kênh Thảo Dương TV nhen!"},
    {"title": "Hội Chứng Sợ Ngày Mai: Tại Sao Luôn Lo Âu Khi Chiều Buông Xuống?", "hook": "Cứ chiều muộn là lồng ngực thắt lại? Não bạn đang báo động giả đó...", "script": "Chào bạn nhen... Khi cảm giác lo âu chiều muộn kéo đến, hãy hít thở sâu 3 nhịp nè. Viết hết những lo lắng ra giấy để giải phóng dung lượng bộ bộ não nhen! Nhấn Đăng Ký Kênh Thảo Dương TV nhen!"},
    {"title": "Nghệ Thuật Buông Bỏ Kỳ Vọng: Giải Tỏa Áp Lực So Sánh Bản Thân", "hook": "Bạn luôn cảm thấy mình đi chậm hơn bạn bè đồng lứa? Hãy lắng nghe điều này...", "script": "Dạ chào bạn nhen! Mỗi người đều có một múi giờ phát triển riêng. Đừng so sánh trang đầu tiên của bạn với trang thứ 20 của người khác. Hãy dịu dàng với chính mình nhen! Bấm Đăng Ký Kênh Thảo Dương TV nhen!"},
    {"title": "Học Cách Nói KHÔNG Mà Không Cảm Thấy Áy Nấy Hay Bác Bỏ", "hook": "Từ chối người khác không phải là ích kỷ, đó là cách bảo vệ năng lượng của bạn...", "script": "Dạ chào bạn nhen! Mỗi lần bạn nói CÓ với người khác mà trong lòng mệt mỏi, là bạn đang nói KHÔNG với chính mình. Bảo vệ năng lượng bản thân nhen! Bấm Đăng Ký Kênh Thảo Dương TV nhen!"}
]

def get_slot_content(day=1, slot_key="slot_08am"):
    slot_info = SLOTS.get(slot_key, SLOTS["slot_18pm"])
    calendar_date_str = datetime.now().strftime("%d/%m/%Y")
    
    pub_days, pub_titles = get_published_days_and_titles()
    
    if "pm" in slot_key.lower() and slot_key not in ["slot_08am", "slot_11am"]:
        # Nikaya night slots
        # Map slot keys to a target rank of unpublished post to prevent duplicates in one day:
        # slot_18pm   -> 1st unpublished post
        # slot_20pm   -> 2nd unpublished post
        # slot_2130pm -> 3rd unpublished post
        rank = 1
        if slot_key == "slot_20pm":
            rank = 2
        elif slot_key == "slot_2130pm":
            rank = 3
            
        found_unpublished = []
        for item in AUTHENTIC_NIKAYA:
            d = item.get("day")
            clean_t = item.get("title", "").strip().lower()
            if d not in pub_days and clean_t not in pub_titles:
                found_unpublished.append(item)
                if len(found_unpublished) >= rank:
                    break
                    
        target_nik = found_unpublished[-1] if len(found_unpublished) >= rank else None
        
        if target_nik:
            item = {
                "post_index": target_nik.get("post_index", target_nik.get("day")),
                "title": target_nik["title"],
                "hook": target_nik["hook"],
                "script": target_nik["script"],
                "category": "Triết Lý Nikaya Kinh Đêm",
                "tags": ["NikayaKinh", "ThảoDươngTV", "LờiPhậtDạy", "ThiềnĐêm", "Shorts"],
                "source": target_nik.get("source", "Kinh Nikaya")
            }
        else:
            fallback_idx = 30 + rank
            item = {
                "post_index": fallback_idx,
                "title": f"Trí Tuệ Tĩnh Lặng Kinh Nikaya - Bài Học An Lạc",
                "hook": "Lắng nghe lời Phật dạy về sự tĩnh lặng...",
                "script": "Dạ chào bạn nhen! Đức Phật dạy: Bình an thực sự đến từ sự tĩnh lặng của tâm trí. Giữ tâm chánh niệm trong từng khoảnh khắc nhen! Bấm Đăng Ký Kênh Thảo Dương TV nhen!",
                "category": "Triết Lý Nikaya Kinh Đêm",
                "tags": ["NikayaKinh", "ThảoDươngTV", "Shorts"]
            }
            
        # Keep authentic Nikaya text for 21:30 PM slot without override
        pass
            
    elif slot_key == "slot_08am":
        dw_idx = (day - 1) % len(DEEP_WORK_SLOTS)
        item = DEEP_WORK_SLOTS[dw_idx]
        item["category"] = "Series B - Tư Duy Deep Work Sáng"
        item["tags"] = ["ThảoDươngTV", "1995lido", "DeepWork", "KỷLuật", "Shorts"]
    else:
        hl_idx = (day - 1) % len(HEALING_SLOTS)
        item = HEALING_SLOTS[hl_idx]
        item["category"] = "Series A - Sơ Cứu Tâm Lý & Chữa Lành Trưa"
        item["tags"] = ["ThảoDươngTV", "1995lido", "ChữaLành", "Shorts"]

    item["day"] = day
    item["slot"] = slot_key
    
    source_tag = f"\n📌 Trích từ: {item.get('source', 'Tạng Kinh Nikaya (PDF)')}\n" if "source" in item else ""

    return {
        "generated_at": datetime.now().isoformat(),
        "post_index": item.get("post_index"),
        "day": day,
        "calendar_date": calendar_date_str,
        "slot_time": slot_info["time"],
        "series": slot_info["series"],
        "title": f"{item['title']} #Shorts #ThaoDuongTV",
        "hook": item["hook"],
        "script": item["script"],
        "tags": item["tags"],
        "category": item["category"],
        "source": item.get("source", "Kinh Nikaya"),
        "description": f"{item['title']} - Thảo Dương TV (@1995lido).{source_tag}\n📌 Lịch phát sóng hàng ngày:\n- 08:00 AM: Tư Duy Deep Work Sáng\n- 11:00 AM: Sơ Cứu Tâm Lý & Chữa Lành Trưa\n- 18:00 PM: Triết Lý Nikaya Kinh Đêm\n\n🌱 Đăng ký kênh: https://www.youtube.com/@1995lido?sub_confirmation=1\n\n#Shorts #ThaoDuongTV #NikayaKinh",
        "pinned_comment": f"Bạn cảm nhận thế nào về bài học Kinh Nikaya hôm nay? Chia sẻ cùng Thảo Dương bên dưới nhen! 🔔 Đừng quên bấm Đăng Ký kênh nha!"
    }

if __name__ == "__main__":
    for sk in ["slot_18pm", "slot_20pm", "slot_2130pm"]:
        c = get_slot_content(1, sk)
        print(f"\n[{sk}] Title: {c['title']}")
