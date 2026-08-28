#!/usr/bin/env python3
"""
30-Day Master Matrix Content Generator for @1995lido (Thảo Dương TV)
Integrates:
1. 10 Approved Nikaya Kinh Shorts Videos
2. Series A - Mid-day Healing & Overthinking Relief
3. Series B - Morning Mindset & Deep Work Productivity
4. Series C - Evening 432Hz Chill Meditation Music & Reflection
Calculates exact calendar dates (DD/MM/YYYY) for all 30 days!
"""

import json
from datetime import datetime, timedelta

START_DATE = datetime(2026, 8, 22)

# Generate 30-day matrix structure
matrix = []

nikaya_topics = [
    ("Lối Sống Biết Đủ (SANTUTTHI): Mở Khóa Bình An Cho Gia Đình", "Thương con không phải là cho con trường đắt nhất, mà là dạy con sự biết đủ...", "Dạ chào bạn nhen! Trong Kinh Nikaya, Đức Phật dạy về triết lý SANTUTTHI, nghĩa là sự 'Biết Đủ'. Giữa thời đại chạy đua bằng cấp, việc dạy con lối sống biết đủ và tự học chính là chìa khóa mở ra bình an thực sự nhen! Bấm Đăng Ký Kênh Thảo Dương TV để lắng nghe mỗi ngày nhen!"),
    ("Sức Mạnh Của Nhẫn Nại (KHANTI): Thắng Được Cơn Giận Là Thắng Tất Cả", "Khi bị xúc phạm, người bản lĩnh chọn im lặng lắng nghe hay đáp trả?...", "Dạ chào bạn nhen! Trong Kinh Tương Ưng, Đức Phật dạy nhẫn nại KHANTI là pháp tu cao nhất. Người biết kiềm chế cơn giận dữ cũng giống như người tài xế làm chủ chiếc xe đang lao dốc nhen! Hãy bấm Đăng Ký Kênh Thảo Dương TV để cùng rèn luyện tâm trí mỗi ngày nhen!"),
    ("Chánh Niệm Hơi Thở (ANAPANASATI): Trở Về Với Hiện Tại Ngay Lúc Này", "Đừng sống trong quá khứ lo âu hay tương lai bất an...", "Chào bạn nhen! Đức Phật dạy trong Kinh Trung Bộ: Quá khứ đã trôi qua, tương lai chưa tới, chỉ có phút giây hiện tại là điểm tựa có thật. Hãy hít một hơi thật sâu và mỉm cười thanh thản nhen! Bấm Đăng Ký Kênh Thảo Dương TV để nhận năng lượng bình an mỗi ngày nhen!"),
    ("Luật Nhân Quả (KAMA): Bạn Là Chủ Nhân Của Chính Số Phận Mình", "Không ai có thể cứu rỗi bạn ngoài chính suy nghĩ và hành động của bạn...", "Dạ chào bạn nhen! Kinh Tăng Chi Bố khẳng định: Con người là chủ nhân của nghiệp, là thừa tự của hành động mình tạo ra. Gieo suy nghĩ thiện lành thì trái ngọt bình an tự tìm đến nhen! Nhấn Đăng Ký Kênh Thảo Dương TV để học hỏi mỗi ngày nhen!"),
    ("Tâm Từ Vô Lượng (METTA): Hóa Giải Mọi Thù Hận Bằng Tình Thương", "Hận thù không thể dập tắt bằng hận thù, chỉ có tình thương mới xóa tan oán hận...", "Chào buổi sáng nhen! Trong Kinh Tiểu Bộ, Đức Phật dạy tâm từ METTA giống như người mẹ bảo vệ đứa con duy nhất của mình. Khi bạn tha thứ, người đầu tiên được giải thoát chính là bạn nhen! Hãy bấm Đăng Ký Kênh Thảo Dương TV nhen!"),
    ("Định Luật Vô Thường (ANICCA): Mọi Mệt Mỏi Rồi Cũng Sẽ Qua Đi", "Cõi đời này không có gì là vĩnh cửu. Niềm vui hay nỗi buồn rồi cũng biến chuyển...", "Dạ chào bạn nhen! Mỗi khi gặp điều không như ý, hãy tự thì thầm: 'Điều này rồi cũng sẽ qua'. Nhìn thấu bản chất vô thường ANICCA giúp ta buông bỏ mọi áp lực nhen! Bấm Đăng Ký Kênh Thảo Dương TV nhen!"),
    ("8 Ngọn Gió Đời (BAT THET PHAP): Bình Thản Trước Khen Chê Bát Phong", "Khen chê, được mất, vinh đùa... Đừng để ngọn gió đời làm nghiêng ngả bạn...", "Chào bạn nhen! Kinh Nikaya dạy về 8 ngọn gió đời: Được - Mất, Khen - Chê, Vinh - Nhục, Sướng - Khổ. Tâm người trí như ngọn núi đá ngàn năm đứng vững trước dông bão nhen! Bấm Đăng Ký Kênh Thảo Dương TV nhen!"),
    ("Chánh Ngữ (SAMMA VACA): Lời Nói Nhẹ Nhàng Xoa Dịu Mọi Tổn Thương", "Lưỡi không xương nhưng có thể bẻ gãy một trái tim. Hãy cẩn trọng lời nói...", "Dạ chào bạn nhen! Đức Phật dạy Chánh Ngữ SAMMA VACA là chỉ nói những lời chân thật, ôn hòa. Trước khi cất lời, hãy tự hỏi: Lời này có đúng sự thật và có lợi ích không nhen! Đăng Ký Kênh Thảo Dương TV nhen!"),
    ("Tự Mình Là Hải Đăng (ATTADIPA): Nương Tựa Vào Nội Lực Bản Thân", "Hãy tự mình là ngọn đèn cho chính mình, chớ nương tựa vào một ai khác...", "Chào bạn nhen! Lời dặn dò cuối cùng của Đức Phật trong Kinh Trường Bộ: Hãy tự mình là ngọn đèn cho chính mình, lấy Chánh Pháp làm chỗ nương tựa vững chắc nhen! Nhấn Đăng Ký Kênh Thảo Dương TV nhen!"),
    ("[Nhạc Thiền] Sự Tĩnh Lặng Nội Tại Từ Lời Kinh Nikaya", "Sau những ồn ào vội vã, hãy trả tâm trí về với sự tĩnh lặng nguyên sơ...", "Chào buổi tối bình yên nhen... Đeo tai nghe vào, thả lỏng cơ thể và đắm mình trong dải âm thanh thiền định 432Hz giúp xoa dịu căng thẳng và ru ngủ sâu giấc nhen! Bấm Đăng Ký Kênh Thảo Dương TV nhen!")
]

deep_work_topics = [
    ("Kỹ Thuật Time Boxing Nâng Cao: Sắp Xếp 1 Ngày Không Xao Nhãng", "Đừng làm việc lan man nữa. Đây là khung hệ thống giúp bạn làm chủ 1 ngày...", "Dạ chào bạn nhen! Muốn hoàn thành việc khó mà không bị phân tâm? Chia 1 ngày thành các ô thời gian cố định, 08h-10h làm việc khó nhất, tắt mọi thông báo nhen! Bấm Đăng Ký Kênh Thảo Dương TV nhen!"),
    ("Phương Pháp Học Sâu (Deep Work): Hoàn Thành Việc Khó Trong Thời Gian Ngắn", "Động lực là kẻ lừa đảo lớn nhất. Bạn cần một hệ thống rèn luyện kỷ luật...", "Chào buổi sáng nhen! Đừng chờ có cảm hứng rồi mới làm việc. Hãy đặt đồng hồ 25 phút Pomodoro, tập trung 100% vào đúng 1 mục tiêu duy nhất nhen! Bấm Đăng Ký Kênh Thảo Dương TV nhen!"),
    ("Bí Quyết Quản Trị Năng Lượng Sinh Học: Tập Trung Cao Độ Đầu Sáng", "Bạn uể oải lúc 9h sáng? Đó là vì bạn chưa biết cách quản trị đồng hồ sinh học...", "Dạ chào bạn nhen! Hãy dành 60 phút đầu sáng cho công việc quan trọng nhất, uống 1 cốc nước ấm và giữ tư thế ngồi thẳng nhen! Đăng Ký Kênh Thảo Dương TV nhen!"),
    ("Quy Tắc 2 Phút Đánh Bại Sự Trì Hoãn Ngay Lập Tức", "Nếu một việc tốn ít hơn 2 phút để hoàn thành, hãy làm nó ngay...", "Chào buổi sáng nhen! Việc nào làm dưới 2 phút như dọn bàn, trả lời tin nhắn, giải quyết ngay. Bạn sẽ thấy nhẹ đầu vô cùng nhen! Đăng Ký Kênh Thảo Dương TV nhen!"),
    ("Tư Duy Tối Ưu Hiệu Suất & Kỷ Luật Bản Thân Đầu Sáng", "3 Thói quen nhỏ mỗi sáng giúp bạn thay đổi diện mạo cuộc sống...", "Dạ chào bạn nhen! Hãy luôn giữ tinh thần kỷ luật, làm việc tập trung và chinh phục từng mục tiêu nhỏ mỗi ngày nhen! Bấm Đăng Ký Kênh Thảo Dương TV nhen!")
]

chill_music_topics = [
    ("[Original Song] Tiếng Vọng Giữa Thành Phố Lớn - Bản Giao Hưởng Cô Độc", "Có những đêm thành phố quá rộng, nhưng không có lấy một nơi nương tựa...", "Chào buổi tối bạn nhen... Để những giai điệu êm ái này vỗ về tâm hồn bạn sau một ngày dài mệt mỏi. Nhắm mắt thư giãn cùng Thảo Dương TV nhen!"),
    ("[Chill Music] Đêm Không Ngủ & Hành Trình Tìm Lại Sự Tĩnh Lặng Tâm Hồn", "Đã 2 giờ sáng và đầu bạn vẫn chạy hàng ngàn suy nghĩ vẩn vơ? Nghe ngay bản nhạc này...", "Chúc bạn buổi tối bình yên nhen... Thả lỏng cơ thể, ngửi mùi hương nhẹ nhàng và để âm nhạc đưa bạn vào giấc ngủ ngon nhen! Bấm Đăng Ký Kênh Thảo Dương TV nhen!"),
    ("[Chill Music] Bản Nhạc Thiền Tần Số 432Hz Tĩnh Tâm Đêm Thứ Hai", "Sau một ngày dài bận rộn, hãy gạt bỏ mọi muộn phiền ngoài cửa phòng...", "Chào buổi tối bình yên nhen... Đeo tai nghe vào và để những giai điệu 432Hz vỗ về tâm hồn bạn sau một ngày làm việc mệt mỏi nhen! Đăng Ký Kênh Thảo Dương TV nhen!"),
    ("[Ambient Piano] Tiếng Mưa Đêm & Bản Nhạc Thư Giãn Sâu Tĩnh Lặng", "Lắng nghe tiếng mưa rơi nhè nhẹ ngoài hiên cửa sổ...", "Chào buổi tối nhen... Hãy để tiếng mưa rơi nhè nhẹ cùng những nốt nhạc piano êm ái xoa dịu mọi căng thẳng trong đầu bạn nhen! Bấm Đăng Ký Kênh Thảo Dương TV nhen!")
]

print("📅 Building 30-Day Master Matrix Content Structure...")
# Combine into full calendar array
master_entries = []

for day in range(1, 31):
    c_date = START_DATE + timedelta(days=day - 1)
    date_str = c_date.strftime("%d/%m/%Y")
    
    # 08:00 AM Slot (Alternates Nikaya Kinh & Deep Work)
    if day <= 10:
        nik_item = nikaya_topics[(day - 1) % len(nikaya_topics)]
        t_08 = f"{nik_item[0]}"
        h_08 = nik_item[1]
        s_08 = nik_item[2]
        cat_08 = "Triết Lý Nikaya Kinh"
    else:
        dw_item = deep_work_topics[(day - 1) % len(deep_work_topics)]
        t_08 = f"{dw_item[0]}"
        h_08 = dw_item[1]
        s_08 = dw_item[2]
        cat_08 = "Series B - Deep Work"
        
    master_entries.append({
        "day": day,
        "date": date_str,
        "slot": "08:00 AM",
        "title": t_08,
        "hook": h_08,
        "script": s_08,
        "category": cat_08
    })

print(f"✅ Generated 30-Day Content Structure with {len(master_entries)} slots!")
