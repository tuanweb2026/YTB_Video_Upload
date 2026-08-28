#!/usr/bin/env python3
"""
Deep Philosophical & Witty Animation Content Generator for Channel 2: @ThaoDuongAnimation
Inspired by Kurzgesagt, The School of Life, Pursuit of Wonder, and Psych2Go!
Blends witty daily life humor with deep psychological & philosophical wisdom!
"""

import json
import os

SCRATCH_DIR = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management"
ANIMATION_DB = f"{SCRATCH_DIR}/animation_posts.json"

PHILOSOPHICAL_ANIMATION_POSTS = [
    {
        "post_index": 1,
        "title": "Bẫy Tâm Lý 'Chờ Có Đủ Mới Sống': Bài Học Chiếc Ly Đầy #Shorts #ThaoDuongAnimation",
        "hook": "Ban ngày mải mê chạy theo tiền tài, tự nhủ: Sau này giàu rồi mình mới sống hạnh phúc...",
        "script": "Dạ chào bạn nhen! Người ta thường rơi vào bẫy tâm lý 'Khi Nào': Khi nào có nhà đẹp mới vui, khi nào giàu mới thong dong. Nhưng chiếc ly nếu cứ chờ rót đầy tràn mới chịu uống, thì nước ngọt bên trong đã sớm bốc hơi! Hạnh phúc không phải là điểm đến cuối con đường, mà là khả năng cảm nhận từng bước chân ngay lúc này nhen! Nhấn Đăng Ký Kênh Thảo Dương Animation nhen!",
        "category": "Triết Lý Cuộc Sống Chiều Sâu",
        "tags": ["ThaoDuongAnimation", "TrietLyCuocSong", "Psychology", "Shorts"]
    },
    {
        "post_index": 2,
        "title": "Nghệ Thuật 'Không Phản Ứng': Thắng Đánh Thức Tâm Trí Giữa Bát Phong #Shorts #ThaoDuongAnimation",
        "hook": "Khi ai đó ném lời xúc phạm vào bạn, bạn sẽ nhặt lên ôm vào lòng hay để nó rơi xuống đất?...",
        "script": "Chào bạn nhen! Triết gia Epictetus dạy rằng: Không ai có thể làm tổn thương bạn nếu bạn không cho phép. Lời chê bai của người khác giống như món quà vô chủ, nếu bạn không nhận thì nó vẫn thuộc về người ném! Học cách dừng lại 3 giây trước mọi cơn giận giúp bạn làm chủ hoàn toàn vận mệnh nhen! Bấm Đăng Ký Kênh Thảo Dương Animation nhen!",
        "category": "Triết Lý Stoicism & Tâm Lý",
        "tags": ["ThaoDuongAnimation", "Stoicism", "TrietLy", "Shorts"]
    },
    {
        "post_index": 3,
        "title": "Bí Mật Của Sự Buông Bỏ: Đừng Ôm Viên Than Đang Cháy #Shorts #ThaoDuongAnimation",
        "hook": "Oán giận người khác giống như tự mình uống chất độc rồi chờ người ta qua đời...",
        "script": "Dạ chào bạn nhen! Trong tâm lý học, việc ôm hận thù giống như nắm chặt một viên than hồng với ý định ném vào người khác. Người bị bỏng đầu tiên luôn là chính bạn! Buông bỏ không phải là tha thứ cho kẻ khác, mà là cởi trói cho chính tâm hồn mình được tự do nhen! Nhấn Đăng Ký Kênh Thảo Dương Animation nhen!",
        "category": "Chữa Lành & Trí Tuệ",
        "tags": ["ThaoDuongAnimation", "TamLyHoc", "ChuaLanh", "Shorts"]
    },
    {
        "post_index": 4,
        "title": "Ảo Tưởng Về Sự Rảnh Rỗi: Tại Sao Càng Rảnh Càng Mệt Mỏi? #Shorts #ThaoDuongAnimation",
        "hook": "Nằm lướt điện thoại cả ngày nhưng tối đến vẫn cảm thấy kiệt sức và trống rỗng...",
        "script": "Chào bạn nhen! Tâm lý học chỉ ra rằng: Sự nằm lười không giúp bộ não nghỉ ngơi, nó chỉ làm gia tăng cảm giác tội lỗi và trì trệ. Hoạt động có mục đích mới thực sự nạp lại năng lượng cho tâm trí. Hãy đứng dậy dọn dẹp căn phòng hoặc đi dạo 10 phút, bạn sẽ thấy tâm hồn nhẹ nhõm ngay nhen! Đăng Ký Kênh Thảo Dương Animation nhen!",
        "category": "Tâm Lý Học Đời Sống",
        "tags": ["ThaoDuongAnimation", "DeepWork", "Mindset", "Shorts"]
    },
    {
        "post_index": 5,
        "title": "Trí Tuệ Của Cây Tre: Càng Nhún Nhường Càng Vươn Cao #Shorts #ThaoDuongAnimation",
        "hook": "Cây cổ thụ cứng ngắc gặp bão lớn liền gãy đôi, nhưng rặng tre mềm dẻo lại đứng vững...",
        "script": "Dạ chào bạn nhen! Trong triết học Phương Đông, sự khiêm nhường và linh hoạt mới là sức mạnh tối thượng. Người biết cúi đầu đúng lúc không phải là kẻ yếu đuối, mà là người có trí tuệ sâu sắc biết tích lũy nội lực để vươn cao sau sóng gió nhen! Bấm Đăng Ký Kênh Thảo Dương Animation nhen!",
        "category": "Triết Lý Nhân Sinh",
        "tags": ["ThaoDuongAnimation", "TrietLy", "KhoaHocCuocSong", "Shorts"]
    }
]

def generate_deep_animation_db():
    with open(ANIMATION_DB, "w", encoding="utf-8") as f:
        json.dump(PHILOSOPHICAL_ANIMATION_POSTS, f, ensure_ascii=False, indent=2)
    print(f"✅ Generated Deep Philosophical Animation DB at: {ANIMATION_DB}")

if __name__ == "__main__":
    generate_deep_animation_db()
