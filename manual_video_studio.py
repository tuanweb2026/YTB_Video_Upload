#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================
  🎬 Manual Video Studio — @1995lido YouTube Management
  Web UI tạo video Shorts thủ công · Port 8098
=============================================================
"""

import os, sys, json, re, time, random, subprocess, threading, uuid, shutil, logging
from datetime import datetime
from pathlib import Path

# ── Auto-install Flask ─────────────────────────────────
try:
    from flask import Flask, request, jsonify, send_file, Response, render_template_string
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "flask", "--user"], check=True)
    from flask import Flask, request, jsonify, send_file, Response, render_template_string

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_OK = True
except ImportError:
    PIL_OK = False

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# ── Paths ──────────────────────────────────────────────
BASE_DIR   = Path(__file__).parent
BG_DIR     = BASE_DIR / "studio_backgrounds"
MUSIC_DIR  = BASE_DIR / "studio_music"
OUT_DIR    = BASE_DIR / "output_manual"
TMP_DIR    = BASE_DIR / "studio_tmp"
DB_FILE    = BASE_DIR / "manual_upload_log.json"
LOG_FILE   = BASE_DIR / "studio_server.log"
TOKEN_FILE = BASE_DIR / "token.json"
FFMPEG     = "/Users/abc/bin/ffmpeg"
PORT       = 8098

for d in [BG_DIR, MUSIC_DIR, OUT_DIR, TMP_DIR]:
    d.mkdir(exist_ok=True)

# ── Logging ─────────────────────────────────────────────
class ColorFormatter(logging.Formatter):
    RESET  = "\033[0m"
    COLORS = {logging.DEBUG:"\033[36m", logging.INFO:"\033[32m",
              logging.WARNING:"\033[33m", logging.ERROR:"\033[31m", logging.CRITICAL:"\033[35m"}
    ICONS  = {logging.DEBUG:"🔍 DEBUG", logging.INFO:"✅ INFO ", logging.WARNING:"⚠️  WARN ",
              logging.ERROR:"❌ ERROR", logging.CRITICAL:"💥 CRIT "}
    def format(self, record):
        c  = self.COLORS.get(record.levelno, self.RESET)
        ic = self.ICONS.get(record.levelno, "   LOG ")
        ts = datetime.now().strftime("%H:%M:%S")
        return f"{c}[{ts}] {ic} | {record.getMessage()}{self.RESET}"

class PlainFormatter(logging.Formatter):
    def format(self, record):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lv = record.levelname[:5]
        return f"[{ts}] {lv} | {record.getMessage()}"

log = logging.getLogger("studio")
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG); ch.setFormatter(ColorFormatter()); log.addHandler(ch)
fh = logging.FileHandler(str(LOG_FILE), encoding="utf-8")
fh.setLevel(logging.DEBUG); fh.setFormatter(PlainFormatter()); log.addHandler(fh)
logging.getLogger("werkzeug").setLevel(logging.ERROR)

BUILD_JOBS = {}

# ══════════════════════════════════════════════════════════
# 📚 TITLE BANKS — Đa dạng nội dung
# ══════════════════════════════════════════════════════════

# Load từ nikaya_30_authentic_posts.json nếu có
def _load_nikaya_from_json():
    p = BASE_DIR / "nikaya_30_authentic_posts.json"
    if not p.exists():
        return []
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        result = []
        for item in data:
            title  = item.get("title", "")
            script = item.get("script", "")
            if title and script and len(script) > 30:
                # Cắt script nếu quá dài (TTS chỉ cần ~60-80 từ)
                words  = script.split()
                if len(words) > 90:
                    script = " ".join(words[:85]) + " nhen!"
                result.append((title, script))
        return result
    except Exception as e:
        log.warning(f"Không load được nikaya JSON: {e}")
        return []

NIKAYA_FROM_JSON = _load_nikaya_from_json()

TITLE_BANKS = {
    # ── Kinh Nikaya (từ JSON + thêm nhiều bài) ────────────────
    "nikaya": NIKAYA_FROM_JSON if NIKAYA_FROM_JSON else [
        ("Kinh Nikaya: Lối Sống Biết Đủ (SANTUTTHI) — Mở Khóa Bình An",
         "Dạ chào bạn nhen! Trong Kinh Tăng Chi Bộ, Đức Phật dạy triết lý SANTUTTHI: Sự biết đủ là giàu có nhất. Hãy dừng lại ngắm những gì mình đang có và cảm ơn từng điều nhỏ bé trong cuộc sống nhen! Bấm Đăng Ký Kênh Thảo Dương TV nhen!"),
        ("Kinh Nikaya: Sức Mạnh Của Nhẫn Nại (KHANTI) — Thắng Cơn Giận",
         "Chào bạn nhen! Kinh Tương Ưng: Nhẫn nại KHANTI là pháp tối thắng trong đời. Khi cơn giận bùng lên hãy hít thở 3 nhịp sâu, nhớ rằng giận dữ chỉ đốt cháy chính mình nhen! Đăng Ký Kênh Thảo Dương TV nhen!"),
        ("Kinh Nikaya: Vô Thường (ANICCA) — Mọi Mệt Mỏi Rồi Cũng Sẽ Qua",
         "Dạ chào bạn nhen! Đức Phật dạy trong Kinh Tương Ưng: Tất cả những gì có sinh ra đều sẽ thay đổi. Nỗi đau hôm nay không phải mãi mãi, hãy để nó qua đi như mây trôi nhen! Đăng Ký Kênh Thảo Dương TV nhen!"),
    ],

    # ── Tư Duy & Deep Work ───────────────────────────────────
    "deep_work": [
        ("Kỹ Thuật Time Boxing Nâng Cao — Làm Chủ 1 Ngày Không Xao Nhãng",
         "Dạ chào bạn nhen! Muốn hoàn thành việc khó mà không bị phân tâm? Chia 1 ngày thành các ô thời gian cố định, làm việc khó nhất từ 08h đến 10h, tắt mọi thông báo nhen! Bấm Đăng Ký Kênh Thảo Dương TV nhen!"),
        ("Quy Tắc 2 Phút Đánh Bại Sự Trì Hoãn Ngay Lập Tức",
         "Chào buổi sáng nhen! Việc nào làm dưới 2 phút như dọn bàn, trả lời tin nhắn thì giải quyết ngay. Bạn sẽ thấy nhẹ đầu vô cùng nhen! Đăng Ký Kênh Thảo Dương TV nhen!"),
        ("Bí Quyết Quản Trị Năng Lượng — Tập Trung Cao Độ Suốt Cả Ngày",
         "Dạ chào bạn nhen! Dành 60 phút đầu sáng cho công việc quan trọng nhất, uống 1 cốc nước ấm và giữ tư thế ngồi thẳng nhen! Đăng Ký Kênh Thảo Dương TV nhen!"),
        ("Phương Pháp Deep Work — Hoàn Thành Việc Khó Trong Thời Gian Ngắn",
         "Chào bạn nhen! Đừng chờ có cảm hứng mới làm. Đặt đồng hồ 25 phút Pomodoro và tập trung 100% vào đúng 1 mục tiêu duy nhất nhen! Bấm Đăng Ký Kênh Thảo Dương TV nhen!"),
        ("5 Phút Sáng Quyết Định Năng Suất Cả Ngày Của Bạn",
         "Dạ chào bạn nhen! Đừng mở điện thoại khi vừa thức dậy. Hít thở sâu 10 nhịp, uống nước và viết 3 việc quan trọng nhất hôm nay nhen! Đăng Ký Kênh Thảo Dương TV nhen!"),
        ("Tại Sao Kẻ Thành Công Luôn Thức Dậy Sớm Hơn Bạn 1 Tiếng",
         "Chào bạn nhen! 1 tiếng yên tĩnh buổi sáng không điện thoại không thông báo bằng 3 tiếng làm việc ban ngày. Thử thức 5h sáng 7 ngày và xem sự khác biệt nhen! Đăng Ký Kênh Thảo Dương TV nhen!"),
        ("Kỹ Thuật Second Brain — Ghi Chú Để Không Bao Giờ Quên Ý Tưởng Hay",
         "Dạ chào bạn nhen! Không ai nhớ được tất cả ý tưởng hay. Hãy dùng app ghi chú để capture ngay khi nghĩ ra, phân loại và kết nối ý tưởng. Não bạn để suy nghĩ không phải để lưu trữ nhen! Thảo Dương TV nhen!"),
        ("Ngừng Đa Nhiệm — Tại Sao Làm Một Việc Lại Hiệu Quả Hơn 5 Việc Cùng Lúc",
         "Chào bạn nhen! Não người không thể đa nhiệm thật sự, chỉ chuyển đổi nhanh giữa các việc. Mỗi lần chuyển tốn 23 phút để lấy lại tập trung. Làm 1 việc đến hết nhen! Thảo Dương TV nhen!"),
        ("4 Loại Việc Theo Ma Trận Eisenhower — Phân Loại Để Làm Đúng Việc",
         "Dạ chào bạn nhen! Chia việc thành: Quan trọng và Khẩn cấp làm ngay, Quan trọng nhưng không khẩn lên kế hoạch, Không quan trọng nhưng khẩn thì ủy thác, còn lại thì loại bỏ nhen! Thảo Dương TV nhen!"),
        ("Bí Quyết Đọc Sách 52 Cuốn Mỗi Năm Mà Không Cần Đọc Nhiều Hơn",
         "Chào bạn nhen! Chỉ cần đọc 20 trang mỗi ngày bạn sẽ đọc xong 18-20 cuốn sách mỗi năm. Đọc vào buổi sáng trước khi mở điện thoại và kiến thức sẽ ngấm sâu hơn nhen! Thảo Dương TV nhen!"),
        ("Tại Sao Bạn Mệt Dù Không Làm Gì — Decision Fatigue Là Gì",
         "Dạ chào bạn nhen! Mỗi quyết định trong ngày từ ăn gì đến mặc gì đều tiêu tốn năng lượng não. Hãy tự động hóa những quyết định nhỏ để dành sức cho việc quan trọng nhen! Thảo Dương TV nhen!"),
        ("Phương Pháp 1 Giờ Vàng Sáng Sớm — Cal Newport Dạy Gì Về Deep Work",
         "Chào bạn nhen! Cal Newport chứng minh 1 giờ tập trung không gián đoạn bằng 3 giờ làm việc thông thường. Tắt wifi, tắt điện thoại và đặt đồng hồ bấm giờ nhen! Đăng Ký Kênh Thảo Dương TV nhen!"),
    ],

    # ── Chữa Lành & Tâm Lý ──────────────────────────────────
    "healing": [
        ("Khi Sự Nhiệt Huyết Biến Mất — Vượt Qua Giai Đoạn Tê Liệt Cảm Xúc",
         "Dạ chào bạn nhen... Nếu hôm nay bạn thấy cạn kiệt năng lượng đừng cố gồng mình. Cho phép bản thân nghỉ ngơi 15 phút lắng nghe hơi thở nhen! Đăng Ký Kênh Thảo Dương TV nhen!"),
        ("Nghệ Thuật Buông Bỏ Kỳ Vọng — Giải Tỏa Áp Lực So Sánh Bản Thân",
         "Dạ chào bạn nhen! Mỗi người có một múi giờ phát triển riêng. Đừng so sánh trang đầu của bạn với trang 20 của người khác nhen! Bấm Đăng Ký Kênh Thảo Dương TV nhen!"),
        ("Học Cách Nói KHÔNG Mà Không Cảm Thấy Áy Nấy",
         "Dạ chào bạn nhen! Mỗi lần nói CÓ với người khác khi lòng mệt mỏi là bạn đang nói KHÔNG với chính mình. Bảo vệ năng lượng bản thân nhen! Đăng Ký Kênh Thảo Dương TV nhen!"),
        ("Hội Chứng Sợ Ngày Mai — Tại Sao Luôn Lo Âu Khi Chiều Buông Xuống",
         "Chào bạn nhen... Khi lo âu chiều muộn kéo đến hãy hít thở sâu 3 nhịp. Viết hết lo lắng ra giấy để giải phóng bộ não khỏi vòng lặp suy nghĩ tiêu cực nhen! Thảo Dương TV nhen!"),
        ("5 Dấu Hiệu Bạn Đang Burnout — Trước Khi Quá Muộn",
         "Dạ chào bạn nhen! Mệt mỏi dù ngủ đủ giấc, không còn cảm giác vui vẻ khi hoàn thành việc, dễ cáu gắt... Đây là dấu hiệu burnout. Hãy dừng lại và chăm sóc bản thân nhen! Thảo Dương TV nhen!"),
        ("Tại Sao Người Mạnh Mẽ Cũng Cần Được Khóc Đôi Khi",
         "Chào bạn nhen... Nước mắt không phải yếu đuối. Khóc là cách cơ thể giải phóng cortisol và adrenaline dư thừa. Cho phép mình cảm nhận cảm xúc để tiếp tục mạnh mẽ hơn nhen! Thảo Dương TV nhen!"),
        ("Kỹ Thuật 5-4-3-2-1 Chặn Cơn Lo Âu Trong 60 Giây",
         "Dạ chào bạn nhen! Khi lo âu tấn công: nhìn 5 thứ bạn thấy, nghe 4 âm thanh, chạm 3 vật liệu, ngửi 2 mùi hương, nếm 1 vị. Não bạn sẽ quay về hiện tại ngay nhen! Thảo Dương TV nhen!"),
        ("Làm Sao Để Tha Thứ Cho Người Làm Mình Đau",
         "Chào bạn nhen! Tha thứ không phải vì họ xứng đáng mà vì bạn xứng đáng được sống nhẹ nhàng. Tha thứ là món quà bạn tặng cho chính mình nhen! Đăng Ký Kênh Thảo Dương TV nhen!"),
        ("Inner Child — Đứa Bé Bên Trong Bạn Đang Cần Gì",
         "Dạ chào bạn nhen! Đôi khi sự cáu kỉnh hay sợ hãi của chúng ta đến từ vết thương tuổi thơ chưa lành. Hãy nói chuyện với đứa bé trong tim bạn như một người bạn thân thiện nhen! Thảo Dương TV nhen!"),
        ("Tại Sao Bạn Cứ Lặp Lại Cùng Một Mối Quan Hệ Độc Hại",
         "Chào bạn nhen! Não bộ bị lập trình từ những trải nghiệm cũ. Khi nhận ra pattern lặp lại hãy dừng lại và tự hỏi: tôi đang tìm kiếm điều gì từ người này nhen! Thảo Dương TV nhen!"),
        ("Nghệ Thuật Sống Chậm Trong Thế Giới Quá Vội Vàng",
         "Dạ chào bạn nhen! Không phải ai nhanh hơn cũng thành công hơn. Thở sâu một lần, uống từng ngụm cà phê, trân trọng khoảnh khắc này. Sống chậm là kỹ năng quý giá nhen! Thảo Dương TV nhen!"),
        ("Cách Thoát Khỏi Vòng Lặp Overthinking Mỗi Đêm",
         "Chào bạn nhen! Khi não không tắt được ban đêm hãy viết ra giấy tất cả lo lắng. Não nhận ra đã lưu trữ an toàn và sẽ cho phép bạn nghỉ ngơi nhen! Đăng Ký Kênh Thảo Dương TV nhen!"),
    ],

    # ── Kỷ Luật & Thói Quen ─────────────────────────────────
    "discipline": [
        ("Atomic Habits — Thay Đổi 1% Mỗi Ngày Để Tạo Bước Nhảy Vọt",
         "Dạ chào bạn nhen! James Clear chứng minh cải thiện 1% mỗi ngày sau 1 năm bạn sẽ tốt hơn 37 lần. Đừng cố thay đổi tất cả một lúc, hãy bắt đầu từ 1 thói quen nhỏ nhen! Thảo Dương TV nhen!"),
        ("Habit Stacking — Ghép Thói Quen Mới Vào Thói Quen Cũ",
         "Chào bạn nhen! Sau khi pha cà phê xong thì ngồi thiền 5 phút. Sau khi đánh răng thì đọc sách 10 trang. Ghép thói quen mới vào trigger quen thuộc giúp bạn duy trì dễ hơn nhen! Thảo Dương TV nhen!"),
        ("Tại Sao Kỷ Luật Quan Trọng Hơn Cảm Hứng 100 Lần",
         "Dạ chào bạn nhen! Cảm hứng đến rồi đi nhưng kỷ luật thì ở lại. Những người thành công không chờ có hứng mới làm việc, họ làm vì đó là thói quen không thể thiếu nhen! Thảo Dương TV nhen!"),
        ("No-Zero Day — Quy Tắc Không Ngày Nào Là Ngày Trống Rỗng",
         "Chào bạn nhen! Mỗi ngày dù bận đến đâu hãy làm ít nhất 1 việc hướng đến mục tiêu của bạn. Chỉ 1 trang sách, 10 cái squat, 1 ý tưởng viết ra. Đừng để ngày nào là zero day nhen! Thảo Dương TV nhen!"),
        ("Cách Xây Dựng Buổi Sáng 30 Phút Thay Đổi Cả Đời",
         "Dạ chào bạn nhen! 5 phút thiền định, 10 phút vận động nhẹ, 5 phút viết nhật ký, 10 phút đọc sách. Chỉ 30 phút sáng bạn đã nạp đủ năng lượng cho cả ngày nhen! Đăng Ký Kênh Thảo Dương TV nhen!"),
        ("Tại Sao Bạn Bỏ Cuộc Sau 3 Ngày — Và Cách Vượt Qua",
         "Chào bạn nhen! Não bộ cần 21 ngày để quen và 66 ngày để tự động hóa thói quen. 3 ngày đầu khó nhất vì não đang kháng cự. Hãy vượt qua 3 ngày đó bằng kế hoạch cụ thể nhen! Thảo Dương TV nhen!"),
        ("Sức Mạnh Của Journaling — Viết Nhật Ký 10 Phút Mỗi Tối",
         "Dạ chào bạn nhen! Viết ra những gì đang nghĩ giúp não giải phóng căng thẳng, nhận ra pattern trong hành vi và đưa ra quyết định sáng suốt hơn. Chỉ cần bút và giấy nhen! Thảo Dương TV nhen!"),
        ("Cold Shower Challenge — Tắm Nước Lạnh 30 Ngày Thay Đổi Điều Gì",
         "Chào bạn nhen! Tắm nước lạnh 2 phút kích hoạt norepinephrine tăng 300%, tăng đề kháng và rèn luyện sức chịu đựng tinh thần. Thử 7 ngày và cảm nhận sự khác biệt nhen! Thảo Dương TV nhen!"),
    ],

    # ── Tài Chính & Đầu Tư Cá Nhân ──────────────────────────
    "finance": [
        ("Quy Tắc 50-30-20 — Phân Chia Thu Nhập Thông Minh Nhất",
         "Dạ chào bạn nhen! 50% cho nhu cầu thiết yếu ăn ở điện nước, 30% cho bản thân giải trí phát triển, 20% tiết kiệm và đầu tư. Quy tắc đơn giản giúp bạn không bao giờ hết tiền cuối tháng nhen! Thảo Dương TV nhen!"),
        ("Tại Sao Bạn Phải Tiết Kiệm Ngay Cả Khi Thu Nhập Thấp",
         "Chào bạn nhen! Tiết kiệm không phải về số tiền bạn có mà là thói quen. Bắt đầu từ 50 nghìn mỗi tháng để não quen với việc trữ tiền. Số tiền tăng dần theo thói quen nhen! Thảo Dương TV nhen!"),
        ("Emergency Fund — Tại Sao Cần Có 6 Tháng Chi Phí Dự Phòng",
         "Dạ chào bạn nhen! Khi mất việc hay bệnh tật ập đến bạn có 6 tháng để xoay sở mà không phải vay nợ hay bán tài sản. Đây là lớp giáp bảo vệ tài chính quan trọng nhất nhen! Thảo Dương TV nhen!"),
        ("5 Thói Quen Tài Chính Của Người Triệu Phú Tự Thân",
         "Chào bạn nhen! Trả bản thân trước, không vay để tiêu dùng, đầu tư dài hạn, học liên tục về tài chính và sống dưới mức thu nhập. 5 thói quen đơn giản nhưng ít người làm được nhen! Thảo Dương TV nhen!"),
    ],

    # ── Kỹ Năng Sống & Giao Tiếp ────────────────────────────
    "life_skills": [
        ("Nghệ Thuật Lắng Nghe Chủ Động — Kỹ Năng Hiếm Người Có",
         "Dạ chào bạn nhen! 80% mâu thuẫn xảy ra vì không thực sự lắng nghe. Hãy tắt màn hình, nhìn vào mắt người nói, gật đầu và phản chiếu lại những gì họ vừa nói. Kỹ năng này thay đổi mọi mối quan hệ nhen! Thảo Dương TV nhen!"),
        ("Cách Đặt Câu Hỏi Hay Để Bất Kỳ Cuộc Trò Chuyện Nào Cũng Sâu Sắc",
         "Chào bạn nhen! Thay vì hỏi Bạn làm gì hãy hỏi Điều gì khiến bạn chọn công việc đó? Câu hỏi mở khơi dậy câu chuyện thú vị và tạo kết nối thật sự giữa người với người nhen! Thảo Dương TV nhen!"),
        ("First Impression — 7 Giây Đầu Tiên Quyết Định Mọi Thứ",
         "Dạ chào bạn nhen! Trong 7 giây đầu não người đã đánh giá bạn qua tư thế đứng, ánh mắt và nụ cười. Đứng thẳng, nhìn thẳng và mỉm cười chân thành là công thức không bao giờ lỗi thời nhen! Thảo Dương TV nhen!"),
        ("Kỹ Thuật Sandwich Feedback — Chỉ Trích Mà Không Làm Tổn Thương",
         "Chào bạn nhen! Khen thật lòng trước, đưa ra vấn đề cần cải thiện ở giữa, kết thúc bằng sự tin tưởng và động viên. Kỹ thuật sandwich giúp người nghe dễ tiếp nhận phê bình nhen! Thảo Dương TV nhen!"),
        ("Tại Sao Người Ít Nói Lại Thường Được Tin Tưởng Hơn",
         "Dạ chào bạn nhen! Người ít nói nhiều nhưng nói đúng lúc thường được đánh giá cao hơn. Hãy lọc trước khi nói: điều này có thật không, có cần thiết không, có tử tế không nhen! Thảo Dương TV nhen!"),
    ],
}

# ── DB helpers ────────────────────────────────────────
def load_db():
    if DB_FILE.exists():
        try: return json.loads(DB_FILE.read_text(encoding="utf-8"))
        except Exception as e: log.error(f"load_db lỗi: {e}")
    return []

def save_db(data):
    DB_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def add_to_db(entry):
    db = load_db()
    db.append(entry)
    save_db(db)
    log.info(f"DB: Lưu [{entry['id'][:8]}] '{entry['title'][:40]}'")

def update_db_entry(video_id, **kwargs):
    db = load_db()
    for e in db:
        if e.get("id") == video_id:
            e.update(kwargs)
    save_db(db)

# ── YouTube Upload ─────────────────────────────────────
import urllib.request, urllib.parse, urllib.error

def refresh_access_token(tokens):
    log.info("OAuth: Refresh access_token...")
    data = urllib.parse.urlencode({
        "client_id": tokens["client_id"], "client_secret": tokens["client_secret"],
        "refresh_token": tokens["refresh_token"], "grant_type": "refresh_token"
    }).encode("utf-8")
    req = urllib.request.Request(
        tokens.get("token_uri", "https://oauth2.googleapis.com/token"), data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req) as r:
        tokens["access_token"] = json.loads(r.read().decode())["access_token"]
    TOKEN_FILE.write_text(json.dumps(tokens, indent=2), encoding="utf-8")
    log.info("OAuth: refresh OK ✅")
    return tokens

def get_tokens():
    if TOKEN_FILE.exists():
        t = json.loads(TOKEN_FILE.read_text(encoding="utf-8"))
        if "refresh_token" in t:
            return refresh_access_token(t)
    return None

def youtube_upload(video_path, title, description, tags):
    log.info(f"YT Upload: '{title[:50]}'  [{video_path}]")
    tokens = get_tokens()
    if not tokens:
        return None, "Chưa có token.json — chạy: python3 setup_token_direct.py"

    metadata = {
        "snippet": {"title": title[:95], "description": description,
                    "tags": tags, "categoryId": "22"},
        "status":  {"privacyStatus": "public", "selfMade": True}
    }
    file_size = os.path.getsize(video_path)
    log.info(f"YT Upload: file size = {file_size/1024/1024:.2f} MB")

    req = urllib.request.Request(
        "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
        data=json.dumps(metadata).encode("utf-8"),
        headers={"Authorization": f"Bearer {tokens['access_token']}",
                 "Content-Type": "application/json; charset=UTF-8",
                 "X-Upload-Content-Length": str(file_size),
                 "X-Upload-Content-Type": "video/mp4"},
        method="POST")
    try:
        with urllib.request.urlopen(req) as r:
            location = r.headers.get("Location")
        log.info("YT Upload: session OK — đang transfer...")
    except urllib.error.HTTPError as e:
        err = f"HTTP {e.code}: {e.read().decode(errors='ignore')[:300]}"
        log.error(f"YT Upload session lỗi: {err}")
        return None, err

    with open(video_path, "rb") as f:
        video_bytes = f.read()
    try:
        with urllib.request.urlopen(urllib.request.Request(
            location, data=video_bytes,
            headers={"Content-Length": str(file_size), "Content-Type": "video/mp4"},
            method="PUT")) as r:
            res = json.loads(r.read().decode())
            vid_id = res.get("id")
        log.info(f"YT Upload: ✅ ID={vid_id}  https://www.youtube.com/watch?v={vid_id}")
        return vid_id, None
    except urllib.error.HTTPError as e:
        err = f"HTTP {e.code}: {e.read().decode(errors='ignore')[:300]}"
        log.error(f"YT Upload binary lỗi: {err}")
        return None, err

# ── Title Card (PIL) ──────────────────────────────────
def _create_title_card(base_path, title_text, output_path):
    img = Image.open(base_path).convert("RGBA")
    W, H = img.size
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    draw    = ImageDraw.Draw(overlay)
    cl, cr  = int(W*.06), int(W*.94)
    ct, cb  = int(H*.15), int(H*.48)
    draw.rounded_rectangle([cl,ct,cr,cb], radius=28, fill=(15,23,42,215), outline=(255,215,0,180), width=3)
    try:
        fn = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", index=1, size=50)
        fs = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", index=0, size=26)
    except:
        fn = fs = ImageFont.load_default()
    draw.rounded_rectangle([cl+18,ct+18,cl+290,ct+56], radius=14, fill=(139,92,246,220))
    draw.text((cl+34,ct+24), "THAO DUONG TV", fill=(255,255,255), font=fs)
    words = title_text.split()
    lines, curr = [], ""
    for w in words:
        t = f"{curr} {w}".strip()
        if len(t) <= 20: curr = t
        else:
            if curr: lines.append(curr)
            curr = w
    if curr: lines.append(curr)
    y = ct + 72
    for line in lines[:4]:
        draw.text((cl+28, y), line, fill=(255,255,255), font=fn)
        y += 56
    Image.alpha_composite(img, overlay).convert("RGB").save(output_path, quality=95)
    log.debug(f"Title card: {output_path}")

# ── Build pipeline ─────────────────────────────────────
def build_video_job(job_id, params):
    job = BUILD_JOBS[job_id]

    def prog(pct, msg):
        job.update({"progress": pct, "message": msg})
        log.info(f"[{job_id[:8]}] {pct:3d}% | {msg}")

    def fail(msg):
        job.update({"status": "error", "error": msg})
        log.error(f"[{job_id[:8]}] FAILED: {msg}")

    try:
        title      = params["title"]
        script     = params["script"]
        voice      = params.get("voice", "vi-VN-HoaiMyNeural")
        bg_path    = params.get("bg_path", "")
        music_path = params.get("music_path", "")
        tags       = params.get("tags", ["Thảo Dương TV","1995lido","Shorts"])
        description= params.get("description", title)

        log.info(f"[{job_id[:8]}] === START BUILD: {title}")
        safe   = re.sub(r"[^\w]", "_", title[:40])
        ts     = datetime.now().strftime("%Y%m%d_%H%M%S")
        vname  = f"manual_{ts}_{safe}.mp4"
        out    = OUT_DIR / vname
        pfx    = str(TMP_DIR / f"tmp_{job_id[:8]}")

        # Step 1
        prog(5, "Bước 1/6: Kiểm tra hình nền...")
        if not bg_path or not os.path.exists(bg_path):
            bgs = sorted(list(BG_DIR.glob("*.jpg")) + list(BG_DIR.glob("*.png")) +
                         list(BG_DIR.glob("*.jpeg")) + list(BG_DIR.glob("*.webp")))
            if bgs:
                bg_path = str(bgs[0])
                log.info(f"[{job_id[:8]}] Auto BG: {bg_path}")
            else:
                fb = sorted(BASE_DIR.glob("title_card_shorts_day_*.jpg"))
                if fb: bg_path = str(fb[0])
                else: return fail("Không có hình nền! Bỏ JPG/PNG vào studio_backgrounds/")

        # Step 2
        prog(15, "Bước 2/6: Tạo title card overlay...")
        tc = pfx + "_tc.jpg"
        if PIL_OK:
            try: _create_title_card(bg_path, title, tc)
            except Exception as e: log.warning(f"Title card lỗi: {e}"); shutil.copy(bg_path, tc)
        else:
            shutil.copy(bg_path, tc)

        # Step 3
        prog(28, f"Bước 3/6: TTS giọng {voice}...")
        tts_mp3  = pfx + "_s.mp3"
        tts_wav  = pfx + "_s.wav"
        proc_wav = pfx + "_p.wav"
        mix_wav  = pfx + "_m.wav"

        clean = re.sub(r"[^\w\s\.,!?àáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđÀÁẢÃẠÂẦẤẨẪẬĂẰẮẲẴẶÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ]", " ", script)
        clean = re.sub(r"\s+", " ", clean).strip()

        ok = False
        for att in range(3):
            r = subprocess.run([sys.executable, "-m", "edge_tts", "--voice", voice,
                               "--text", clean, "--write-media", tts_mp3],
                              capture_output=True, text=True, timeout=90)
            if r.returncode == 0 and os.path.exists(tts_mp3) and os.path.getsize(tts_mp3) > 500:
                ok = True; break
            log.warning(f"[{job_id[:8]}] TTS attempt {att+1} fail: {r.stderr[:100]}")
            time.sleep(2)
        if not ok:
            return fail("TTS thất bại sau 3 lần. Fix: pip3 install edge-tts --user  |  Kiểm tra kết nối internet")

        # Step 4
        prog(45, "Bước 4/6: EQ audio + mix nhạc...")
        for cmd in [
            [FFMPEG,"-y","-i",tts_mp3,tts_wav],
            [FFMPEG,"-y","-i",tts_wav,"-af","equalizer=f=250:width_type=h:width=200:g=3.5,equalizer=f=3500:width_type=h:width=1200:g=2.0,lowpass=f=6000",proc_wav]
        ]:
            r = subprocess.run(cmd, capture_output=True, timeout=60)
            if r.returncode != 0:
                return fail(f"FFmpeg audio lỗi: {r.stderr.decode()[-200:]}")

        # Đo duration
        rd = subprocess.run([FFMPEG,"-i",proc_wav], stderr=subprocess.PIPE, timeout=10)
        duration = 32.0
        for line in rd.stderr.decode().split("\n"):
            if "Duration:" in line:
                try:
                    p = line.split("Duration:")[1].split(",")[0].strip().split(":")
                    duration = float(p[0])*3600 + float(p[1])*60 + float(p[2])
                except: pass
                break
        log.info(f"[{job_id[:8]}] Duration: {duration:.1f}s")

        if music_path and os.path.exists(music_path):
            r = subprocess.run([FFMPEG,"-y","-i",proc_wav,"-i",music_path,
                "-filter_complex","[0:a]volume=1.35[a0];[1:a]volume=0.22[a1];[a0][a1]amix=inputs=2:duration=first[aout]",
                "-map","[aout]",mix_wav], capture_output=True, timeout=90)
            if r.returncode != 0:
                log.warning(f"Mix nhạc lỗi — dùng giọng đọc gốc"); shutil.copy(proc_wav, mix_wav)
        else:
            shutil.copy(proc_wav, mix_wav)

        # Step 5
        prog(62, "Bước 5/6: Chọn ảnh 3 cảnh...")
        all_bgs = sorted([str(f) for ext in ["*.jpg","*.png","*.jpeg","*.webp"]
                          for f in BG_DIR.glob(ext) if str(f) != bg_path])
        img1 = tc
        img2 = all_bgs[0] if len(all_bgs) >= 1 else img1
        img3 = all_bgs[1] if len(all_bgs) >= 2 else img1
        d1, d2, d3 = duration*.35, duration*.30, duration*.35

        # Step 6
        prog(75, "Bước 6/6: Encode MP4...")
        fc = (f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
              f"loop=loop=-1:size=1:start=0,setpts=N/TB[v0];"
              f"[1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
              f"loop=loop=-1:size=1:start=0,setpts=N/TB[v1];"
              f"[2:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
              f"loop=loop=-1:size=1:start=0,setpts=N/TB[v2];"
              f"[v0][v1][v2]concat=n=3:v=1:a=0[outv]")
        cmd = [FFMPEG,"-y",
               "-loop","1","-t",str(d1),"-i",img1,
               "-loop","1","-t",str(d2),"-i",img2,
               "-loop","1","-t",str(d3),"-i",img3,
               "-i",mix_wav,
               "-filter_complex",fc,"-map","[outv]","-map","3:a",
               "-c:v","libx264","-pix_fmt","yuv420p","-r","30",
               "-c:a","aac","-b:a","192k","-shortest",str(out)]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if r.returncode != 0 or not out.exists():
            return fail(f"FFmpeg encode lỗi:\n{r.stderr[-400:]}")

        sz = out.stat().st_size/1024/1024
        log.info(f"[{job_id[:8]}] Encode OK: {vname} ({sz:.2f}MB)")

        prog(95, "Dọn file tạm...")
        for f in TMP_DIR.glob(f"tmp_{job_id[:8]}*"):
            try: f.unlink()
            except: pass

        prog(98, "Lưu database...")
        entry = {
            "id": job_id, "created_at": datetime.now().isoformat(),
            "title": title, "script": script, "voice": voice,
            "bg_image": bg_path, "music": music_path or "",
            "video_file": str(out), "video_name": vname,
            "duration": round(duration,1), "description": description, "tags": tags,
            "status": "ready",
            "youtube_video_id": None, "youtube_url": None,
            "uploaded_at": None, "upload_count": 0,
        }
        add_to_db(entry)
        job.update({"status":"done","progress":100,"message":f"✅ {vname} ({sz:.1f}MB)","video_path":str(out),"video_name":vname})
        log.info(f"[{job_id[:8]}] === DONE ✅ {vname} ===")

    except Exception as e:
        import traceback
        log.error(f"[{job_id[:8]}] EXCEPTION:\n{traceback.format_exc()}")
        job.update({"status":"error","error":f"{type(e).__name__}: {e}"})

# ════════════════════════════════════════════════════════
# FLASK APP
# ════════════════════════════════════════════════════════
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 200*1024*1024
ALLOWED_IMAGE = {".jpg",".jpeg",".png",".webp"}
ALLOWED_AUDIO = {".wav",".mp3",".aiff",".m4a",".ogg"}

@app.before_request
def _log_req():
    if not request.path.startswith(("/api/status","/api/bg-thumb")):
        log.debug(f"→ {request.method} {request.path}")

@app.after_request
def _log_resp(resp):
    if not request.path.startswith(("/api/status","/api/video-file","/api/bg-thumb")):
        sym = "✅" if resp.status_code < 400 else "❌"
        log.debug(f"← {sym} {resp.status_code} {request.method} {request.path}")
    return resp

# ── Xây dựng danh sách category cho dropdown ─────────
def get_categories():
    return [
        {"id":"nikaya",      "name":"🌙 Kinh Nikaya (Phật giáo)", "count": len(TITLE_BANKS.get("nikaya",[]))},
        {"id":"deep_work",   "name":"🌅 Tư Duy & Deep Work",       "count": len(TITLE_BANKS.get("deep_work",[]))},
        {"id":"healing",     "name":"🌿 Chữa Lành & Tâm Lý",       "count": len(TITLE_BANKS.get("healing",[]))},
        {"id":"discipline",  "name":"💪 Kỷ Luật & Thói Quen",      "count": len(TITLE_BANKS.get("discipline",[]))},
        {"id":"finance",     "name":"💰 Tài Chính Cá Nhân",         "count": len(TITLE_BANKS.get("finance",[]))},
        {"id":"life_skills", "name":"🗣️ Kỹ Năng Sống",              "count": len(TITLE_BANKS.get("life_skills",[]))},
    ]

# ════════════════════════════════════════════════════════
HTML = r"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>🎬 Manual Video Studio — @1995lido</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#0f172a;--surface:#1e293b;--s2:#263346;--border:#334155;
  --blue:#3b82f6;--purple:#8b5cf6;--green:#10b981;--red:#ef4444;
  --orange:#f59e0b;--pink:#ec4899;--text:#e2e8f0;--muted:#94a3b8}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
  background:var(--bg);color:var(--text);font-size:13px;min-height:100vh}
.navbar{background:linear-gradient(135deg,#0f172a,#1e3a5f);padding:13px 26px;
  display:flex;align-items:center;justify-content:space-between;
  border-bottom:1px solid var(--border);position:sticky;top:0;z-index:100}
.nav-brand{font-size:17px;font-weight:800;color:#fff}
.nav-links a{color:var(--muted);text-decoration:none;margin-left:18px;font-size:12px}
.nav-links a:hover{color:var(--blue)}
.main-wrap{display:grid;grid-template-columns:420px 1fr;min-height:calc(100vh - 50px)}
.left-panel{background:var(--surface);border-right:1px solid var(--border);
  padding:22px 20px;overflow-y:auto;max-height:calc(100vh - 50px)}
.right-panel{padding:22px 24px;overflow-y:auto;max-height:calc(100vh - 50px)}
.shead{font-size:10px;font-weight:800;letter-spacing:2px;color:var(--purple);
  text-transform:uppercase;margin:18px 0 9px;padding-bottom:6px;border-bottom:1px solid var(--border)}
.shead:first-child{margin-top:0}
label{display:block;font-size:11.5px;color:var(--muted);margin-bottom:4px;font-weight:600}
input[type=text],textarea,select{width:100%;background:var(--s2);border:1px solid var(--border);
  border-radius:8px;color:var(--text);padding:8px 11px;font-size:12.5px;outline:none;
  transition:border-color .2s;font-family:inherit}
input:focus,textarea:focus,select:focus{border-color:var(--blue)}
textarea{min-height:96px;resize:vertical}
.frow{margin-bottom:13px}
.row2{display:flex;gap:7px}
.row2 input{flex:1}
.btn{padding:7px 14px;border:none;border-radius:8px;font-size:12px;font-weight:700;
  cursor:pointer;transition:all .15s;display:inline-flex;align-items:center;
  gap:5px;white-space:nowrap;line-height:1.4}
.btn:hover{transform:translateY(-1px);opacity:.92}
.btn:disabled{opacity:.5;cursor:not-allowed;transform:none!important}
.btn-auto{background:var(--purple);color:#fff}
.btn-up{background:var(--s2);color:var(--text);border:1px solid var(--border)}
.btn-process{background:linear-gradient(135deg,var(--blue),var(--purple));
  color:#fff;padding:11px 20px;font-size:13.5px;width:100%;justify-content:center;
  margin-top:6px;border-radius:10px}
.btn-approve{background:var(--green);color:#fff;font-size:11px;padding:7px 16px;border-radius:8px}
.btn-reupload{background:transparent;color:var(--orange);border:1px solid var(--orange);
  font-size:11px;padding:5px 12px;border-radius:6px}
.btn-reupload:hover{background:var(--orange);color:#000}
.btn-del{background:transparent;color:var(--red);border:1px solid #991b1b;
  font-size:11px;padding:5px 12px;border-radius:6px}
.btn-del:hover{background:#991b1b;color:#fff}
.btn-sm{padding:5px 11px;font-size:11px}
/* Category stats */
.cat-stats{background:var(--s2);border:1px solid var(--border);border-radius:8px;
  padding:8px 11px;margin-top:6px;font-size:10.5px}
.cat-stat-row{display:flex;align-items:center;gap:6px;margin-bottom:3px}
.cat-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0}
.cat-name{flex:1;color:var(--text)}
.cat-cnt{color:var(--orange);font-weight:700}
/* Drop zone */
.drop-zone{border:2px dashed var(--border);border-radius:10px;padding:18px;
  text-align:center;cursor:pointer;background:var(--s2);position:relative;
  transition:border-color .2s}
.drop-zone:hover{border-color:var(--blue)}
.drop-zone input{position:absolute;inset:0;opacity:0;cursor:pointer;width:100%;height:100%}
.dz-icon{font-size:26px;margin-bottom:6px}
.dz-text{color:var(--muted);font-size:11.5px}
.dz-fmt{color:var(--orange);font-size:10.5px;margin-top:3px}
.preview-thumb{width:100%;border-radius:8px;margin-top:6px;max-height:130px;object-fit:cover}
/* Alert box */
.alert-box{border-radius:8px;padding:8px 12px;font-size:11px;margin-top:6px;display:none}
.alert-warn{background:#78350f20;border:1px solid var(--orange);color:var(--orange)}
.alert-err{background:#7f1d1d20;border:1px solid var(--red);color:var(--red)}
.alert-ok{background:#052e1620;border:1px solid var(--green);color:var(--green)}
/* BG grid */
.bg-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:7px;margin-top:8px;
  max-height:210px;overflow-y:auto}
.bgi{border-radius:8px;overflow:hidden;cursor:pointer;border:2px solid transparent;
  transition:border-color .2s;position:relative}
.bgi:hover{border-color:var(--blue)}
.bgi.sel{border-color:var(--purple)}
.bgi img{width:100%;height:66px;object-fit:cover;display:block}
.bgi .bgn{font-size:9px;color:var(--muted);padding:3px 4px;background:var(--s2);
  text-overflow:ellipsis;overflow:hidden;white-space:nowrap}
.bgi .bgck{position:absolute;top:4px;right:4px;background:var(--purple);color:#fff;
  border-radius:50%;width:15px;height:15px;font-size:9px;display:none;
  align-items:center;justify-content:center}
.bgi.sel .bgck{display:flex}
/* Music list */
.mlist{margin-top:7px}
.mi{display:flex;align-items:center;gap:8px;padding:7px 10px;border-radius:8px;
  border:1px solid var(--border);margin-bottom:5px;cursor:pointer;
  background:var(--s2);transition:all .15s}
.mi:hover,.mi.sel{border-color:var(--purple)}
.mi .mii{font-size:15px}.mi .min{flex:1;font-size:12px;font-weight:600}
.mi .msz{font-size:10px;color:var(--muted)}.mi .mck{color:var(--purple);font-size:13px;display:none}
.mi.sel .mck{display:block}
/* Voice grid */
.vgrid{display:grid;grid-template-columns:1fr 1fr;gap:7px;margin-top:8px}
.vc{border:2px solid var(--border);border-radius:10px;padding:11px;cursor:pointer;
  text-align:center;background:var(--s2);transition:all .15s}
.vc:hover{border-color:var(--blue)}.vc.sel{border-color:var(--purple);background:#3b0dbf12}
.vc .vce{font-size:26px;margin-bottom:5px}.vc .vcn{font-weight:700;font-size:12px}
.vc .vci{font-size:10px;color:var(--muted);margin-top:2px}
/* Progress */
.prog-wrap{margin-top:14px;display:none}
.prog-bg{background:var(--border);border-radius:20px;height:8px;overflow:hidden}
.prog-fill{height:100%;border-radius:20px;width:0%;transition:width .4s;
  background:linear-gradient(90deg,var(--blue),var(--purple))}
.prog-msg{font-size:11.5px;color:var(--muted);margin-top:5px;min-height:17px}
/* Panel */
.panel-title{font-size:17px;font-weight:800;color:#fff;margin-bottom:4px}
.panel-sub{color:var(--muted);font-size:11.5px;margin-bottom:18px}
/* Video cards */
.vcard{background:var(--surface);border:1px solid var(--border);border-radius:12px;
  padding:15px;margin-bottom:14px;transition:border-color .2s}
.vcard.uploaded{border-left:4px solid var(--green)}
.vcard.ready{border-left:4px solid var(--blue)}
.vc-head{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px}
.vc-title{font-weight:700;font-size:13px;flex:1;margin-right:8px;color:#fff;line-height:1.35}
.badge{padding:3px 9px;border-radius:10px;font-size:10px;font-weight:700;flex-shrink:0}
.badge-ready{background:#1d4ed820;color:var(--blue);border:1px solid var(--blue)}
.badge-live{background:#05432020;color:var(--green);border:1px solid var(--green)}
.vc-meta{display:flex;gap:10px;margin-bottom:8px;flex-wrap:wrap}
.vc-meta span{color:var(--muted);font-size:10.5px}
.vc-script{color:var(--muted);font-size:10.5px;font-style:italic;border-left:3px solid var(--purple);
  padding-left:9px;margin-bottom:10px;max-height:54px;overflow:hidden;line-height:1.5}
.vc-player{display:flex;justify-content:center;margin:10px 0;
  background:var(--s2);border-radius:10px;padding:7px}
.vc-upload-box{background:#0f172a;border-radius:10px;padding:12px 14px;margin-bottom:10px;
  border:1px solid var(--border)}
.vc-upload-label{font-size:10px;font-weight:700;letter-spacing:1px;text-transform:uppercase;
  color:var(--muted);margin-bottom:8px}
.vc-uploaded-info{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:6px}
.vc-yt-badge{background:#05432030;color:var(--green);border:1px solid var(--green);
  padding:2px 8px;border-radius:8px;font-size:10px;font-weight:700}
.vc-yt-link{color:var(--green);font-weight:700;font-size:11px;text-decoration:none}
.vc-yt-link:hover{text-decoration:underline}
.reupload-row{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-top:6px;
  padding-top:6px;border-top:1px dashed var(--border)}
.upload-log{background:#070e1a;border:1px solid var(--border);border-radius:8px;
  padding:8px 11px;margin:8px 0;max-height:100px;overflow-y:auto;font-family:monospace}
.vc-actions{display:flex;gap:7px;flex-wrap:wrap;align-items:center;margin-top:6px}
/* History */
.hist-section{margin-top:28px;border-top:1px solid var(--border);padding-top:18px}
.hist-title{font-size:14px;font-weight:700;color:#fff;margin-bottom:10px}
.hist-table{width:100%;border-collapse:collapse;font-size:11.5px}
.hist-table th{padding:7px 10px;text-align:left;font-weight:700;color:var(--muted);
  background:var(--s2);font-size:10.5px;text-transform:uppercase;letter-spacing:.5px}
.hist-table td{padding:7px 10px;border-bottom:1px solid var(--border)}
.hist-table tr:hover td{background:var(--s2)}
/* Toast */
#toast{position:fixed;bottom:22px;right:22px;padding:11px 18px;border-radius:10px;
  font-weight:700;font-size:12.5px;display:none;z-index:9999;min-width:240px;
  box-shadow:0 4px 20px rgba(0,0,0,.5)}
#toast.s{background:var(--green);color:#fff}
#toast.e{background:var(--red);color:#fff}
#toast.i{background:#1d4ed8;color:#fff}
#toast.w{background:var(--orange);color:#000}
/* Misc */
.empty{text-align:center;padding:52px 20px;color:var(--muted)}
.empty .ei{font-size:46px;margin-bottom:10px}
.finfo{background:var(--s2);border:1px solid var(--border);border-radius:7px;
  padding:9px 13px;font-size:10.5px;color:var(--muted);margin-top:7px}
.finfo code{color:var(--orange);font-size:10px}
.tags{display:flex;gap:5px;flex-wrap:wrap;margin-top:5px}
.tag{background:var(--s2);border:1px solid var(--border);border-radius:10px;
  padding:3px 9px;font-size:10.5px;color:var(--text);cursor:pointer;user-select:none}
.tag.on{background:var(--purple);border-color:var(--purple);color:#fff}
hr{border:none;border-top:1px solid var(--border);margin:15px 0}
@media(max-width:880px){.main-wrap{grid-template-columns:1fr}}
</style>
</head>
<body>
<nav class="navbar">
  <span class="nav-brand">🎬 Manual Video Studio · Port 8098</span>
  <div class="nav-links">
    <a href="http://localhost:8099" target="_blank">📊 Dashboard</a>
    <a href="#gallery">🎥 Gallery</a>
    <a href="#hist">📋 Log Upload</a>
  </div>
</nav>
<div class="main-wrap">
<!-- ══════ LEFT PANEL ══════ -->
<div class="left-panel">
  <div class="shead">1 · Tiêu Đề & Kịch Bản</div>

  <div class="frow">
    <label>Thể loại</label>
    <div class="row2">
      <select id="category" onchange="updateCatInfo()">
        <option value="nikaya">🌙 Kinh Nikaya (Phật giáo)</option>
        <option value="deep_work">🌅 Tư Duy & Deep Work</option>
        <option value="healing">🌿 Chữa Lành & Tâm Lý</option>
        <option value="discipline">💪 Kỷ Luật & Thói Quen</option>
        <option value="finance">💰 Tài Chính Cá Nhân</option>
        <option value="life_skills">🗣️ Kỹ Năng Sống</option>
      </select>
      <button class="btn btn-auto btn-sm" onclick="autoTitle()">✨ Auto</button>
    </div>
    <div id="catInfo" class="finfo" style="margin-top:5px">Đang tải...</div>
  </div>

  <div class="frow">
    <label>Tiêu đề video *</label>
    <input type="text" id="title" placeholder="Nhập tiêu đề hoặc nhấn Auto...">
  </div>

  <div class="frow">
    <label>Script / Kịch bản giọng đọc *</label>
    <textarea id="script" placeholder="Dạ chào bạn nhen! [Nội dung]... Bấm Đăng Ký Kênh Thảo Dương TV nhen!"></textarea>
    <div class="finfo">💡 Kết thúc bằng <strong>"nhen!"</strong> · Không dùng emoji · ~60–90 từ (~30–40s)</div>
  </div>

  <div class="frow">
    <label>Tags YouTube</label>
    <div class="tags" id="tagbox">
      <span class="tag on" data-t="Thảo Dương TV">Thảo Dương TV</span>
      <span class="tag on" data-t="1995lido">1995lido</span>
      <span class="tag on" data-t="Shorts">Shorts</span>
      <span class="tag" data-t="phát triển bản thân">PT Bản Thân</span>
      <span class="tag" data-t="tâm lý">Tâm lý</span>
      <span class="tag" data-t="Kinh Nikaya">Kinh Nikaya</span>
      <span class="tag" data-t="thiền định">Thiền định</span>
      <span class="tag" data-t="kỷ luật">Kỷ luật</span>
      <span class="tag" data-t="tài chính">Tài chính</span>
    </div>
  </div>

  <hr>
  <div class="shead">2 · Hình Nền (Khuyến nghị 1080×1920)</div>
  <div class="finfo" style="margin-bottom:8px">
    📂 Bỏ ảnh vào: <code>studio_backgrounds/</code> · Tỉ lệ lý tưởng: <strong>1080×1920 (9:16)</strong>
    <br>⚠️ Nếu sai tỉ lệ video vẫn tạo được nhưng sẽ bị crop/zoom
  </div>

  <div class="frow">
    <label>Upload ảnh mới</label>
    <div class="drop-zone">
      <input type="file" id="bgFile" accept="image/jpeg,image/png,image/webp"
             onchange="uploadBg(this)">
      <div class="dz-icon">🖼️</div>
      <div class="dz-text">Kéo thả hoặc click chọn ảnh</div>
      <div class="dz-fmt">JPG · PNG · WEBP · Khuyến nghị 1080×1920</div>
    </div>
    <!-- Alert size ảnh -->
    <div class="alert-box" id="bgSizeAlert"></div>
    <img id="bgPrev" class="preview-thumb" style="display:none">
  </div>

  <div class="frow">
    <div style="display:flex;justify-content:space-between;align-items:center">
      <label>Chọn từ thư mục có sẵn</label>
      <button class="btn btn-up btn-sm" onclick="loadBgs()">🔄 Tải lại</button>
    </div>
    <div class="bg-grid" id="bgGrid">
      <div style="text-align:center;color:var(--muted);padding:16px;font-size:11px;grid-column:1/-1">Đang tải...</div>
    </div>
  </div>
  <input type="hidden" id="selBg" value="">

  <hr>
  <div class="shead">3 · Giọng Đọc (Miền Nam)</div>
  <div class="vgrid">
    <div class="vc sel" onclick="selVoice('vi-VN-HoaiMyNeural',this)">
      <div class="vce">👩</div><div class="vcn">Hoài My (Nữ)</div>
      <div class="vci">Ngọt ngào · Nam Bộ</div>
    </div>
    <div class="vc" onclick="selVoice('vi-VN-NamMinhNeural',this)">
      <div class="vce">👨</div><div class="vcn">Nam Minh (Nam)</div>
      <div class="vci">Truyền cảm · Nam Bộ</div>
    </div>
  </div>
  <input type="hidden" id="selVoice" value="vi-VN-HoaiMyNeural">

  <hr>
  <div class="shead">4 · Nhạc Nền</div>
  <div class="finfo" style="margin-bottom:8px">📂 Bỏ nhạc vào: <code>studio_music/</code> · WAV · MP3 · AIFF · M4A</div>

  <div class="frow">
    <label>Upload nhạc mới</label>
    <div class="drop-zone">
      <input type="file" id="musicFile" accept="audio/*" onchange="uploadMusic(this)">
      <div class="dz-icon">🎵</div>
      <div class="dz-text">Kéo thả hoặc click chọn nhạc</div>
      <div class="dz-fmt">WAV · MP3 · AIFF · M4A</div>
    </div>
  </div>

  <div class="frow">
    <div style="display:flex;justify-content:space-between;align-items:center">
      <label>Chọn nhạc có sẵn</label>
      <button class="btn btn-up btn-sm" onclick="loadMusic()">🔄 Tải lại</button>
    </div>
    <div class="mlist" id="mlist">
      <div style="text-align:center;color:var(--muted);padding:12px;font-size:11px">Đang tải...</div>
    </div>
  </div>
  <input type="hidden" id="selMusic" value="">

  <hr>
  <button class="btn btn-process" id="procBtn" onclick="processVideo()">🚀 Tạo Video Ngay</button>
  <div class="prog-wrap" id="progWrap">
    <div class="prog-bg"><div class="prog-fill" id="progFill"></div></div>
    <div class="prog-msg" id="progMsg">Đang chuẩn bị...</div>
  </div>

</div><!-- end left -->

<!-- ══════ RIGHT PANEL ══════ -->
<div class="right-panel" id="gallery">
  <div class="panel-title">🎥 Video Gallery</div>
  <div class="panel-sub">Review và Upload — mọi video đều có nút Upload YouTube</div>
  <div id="videoGallery"></div>
  <div class="hist-section" id="hist">
    <div class="hist-title">📋 Nhật Ký Upload YouTube</div>
    <div id="histTable">Đang tải...</div>
  </div>
</div>
</div>

<div id="toast"></div>

<script>
let selBgPath='', selMusicPath='', pollTimer=null;
let catData = {};

document.addEventListener('DOMContentLoaded',()=>{
  loadCats(); loadBgs(); loadMusic(); loadGallery(); loadHistory();
  document.querySelectorAll('#tagbox .tag').forEach(t=>
    t.addEventListener('click',()=>t.classList.toggle('on')));
});

function getTags(){
  return Array.from(document.querySelectorAll('#tagbox .tag.on')).map(t=>t.dataset.t);
}

// ── CATEGORIES ──
async function loadCats(){
  const r = await fetch('/api/categories');
  const d = await r.json();
  catData = {};
  d.categories.forEach(c => catData[c.id]=c);
  updateCatInfo();
}

function updateCatInfo(){
  const cat = document.getElementById('category').value;
  const c   = catData[cat];
  const el  = document.getElementById('catInfo');
  if(c){
    el.innerHTML = `📚 <strong>${c.count} bài</strong> trong kho — nhấn <strong>Auto</strong> để ngẫu nhiên chọn 1 bài`;
  } else {
    el.innerHTML = 'Đang tải dữ liệu...';
  }
}

// ── AUTO TITLE ──
async function autoTitle(){
  const cat = document.getElementById('category').value;
  const r   = await fetch('/api/auto-title?category='+cat);
  const d   = await r.json();
  if(d.title){
    document.getElementById('title').value  = d.title;
    document.getElementById('script').value = d.script;
    toast('✨ Sinh tiêu đề mới! ('+d.bank_size+' bài trong kho)','s');
  }
}

// ── BACKGROUNDS ──
function loadBgs(){
  fetch('/api/backgrounds').then(r=>r.json()).then(d=>renderBgs(d.backgrounds)).catch(()=>{});
}
function renderBgs(bgs){
  const g=document.getElementById('bgGrid');
  if(!bgs||!bgs.length){
    g.innerHTML='<div style="grid-column:1/-1;color:var(--muted);font-size:11px;padding:18px;text-align:center">Chưa có ảnh — bỏ vào <strong>studio_backgrounds/</strong></div>';
    return;
  }
  g.innerHTML=bgs.map(b=>`
    <div class="bgi${b.path===selBgPath?' sel':''}" onclick="pickBg('${b.path}',this,'${b.w||0}','${b.h||0}')" title="${b.name}">
      <img src="/api/bg-thumb?path=${encodeURIComponent(b.path)}" loading="lazy">
      <div class="bgn">${b.name}</div>
      <div class="bgck">✓</div>
    </div>`).join('');
}
function pickBg(path,el,w,h){
  selBgPath=path; document.getElementById('selBg').value=path;
  document.querySelectorAll('.bgi').forEach(e=>e.classList.remove('sel'));
  el.classList.add('sel');
  // Kiểm tra tỉ lệ
  checkBgSize(parseInt(w),parseInt(h),'bgSizeAlert');
  toast('🖼️ Chọn: '+path.split('/').pop(),'i');
}

// ── ALERT SIZE ẢNH ──
function checkBgSize(w, h, alertId){
  const el = document.getElementById(alertId);
  if(!el) return;
  if(!w || !h){ el.style.display='none'; return; }
  const ratio = w/h;
  const idealRatio = 9/16; // 0.5625
  const diff = Math.abs(ratio - idealRatio);
  if(diff < 0.05){
    el.className='alert-box alert-ok';
    el.innerHTML='✅ Tỉ lệ ảnh lý tưởng: '+w+'×'+h+' (9:16 Shorts)';
    el.style.display='block';
  } else if(diff < 0.2){
    el.className='alert-box alert-warn';
    el.innerHTML='⚠️ Ảnh '+w+'×'+h+' — Tỉ lệ không lý tưởng. Video sẽ bị crop. Khuyến nghị: <strong>1080×1920</strong> (9:16)';
    el.style.display='block';
  } else {
    el.className='alert-box alert-err';
    el.innerHTML='❌ Ảnh '+w+'×'+h+' — Sai tỉ lệ nghiêm trọng! Ảnh nằm ngang sẽ bị crop xấu. <strong>Cần ảnh đứng 1080×1920</strong> (tỉ lệ 9:16) để video không bị lỗi hình nhen!';
    el.style.display='block';
  }
}

async function uploadBg(inp){
  if(!inp.files[0]) return;
  const file = inp.files[0];

  // Đọc kích thước ảnh trước khi upload
  const reader = new FileReader();
  reader.onload = function(e){
    const img   = new Image();
    img.onload  = function(){
      const w=this.naturalWidth, h=this.naturalHeight;
      // Hiện preview
      const prev = document.getElementById('bgPrev');
      prev.src=e.target.result; prev.style.display='block';
      // Check size
      checkBgSize(w,h,'bgSizeAlert');
      // Nếu ảnh nằm ngang thì cảnh báo mạnh
      if(w > h){
        toast('⚠️ Ảnh nằm ngang ('+w+'×'+h+')! Video Shorts cần ảnh đứng 1080×1920 nhen!','w');
      }
    };
    img.src = e.target.result;
  };
  reader.readAsDataURL(file);

  const fd=new FormData(); fd.append('file',file);
  toast('⏳ Upload ảnh...','i');
  const res=await fetch('/api/upload-bg',{method:'POST',body:fd});
  const d=await res.json();
  if(d.success){
    toast('✅ Upload ảnh OK! ('+d.w+'×'+d.h+')','s');
    selBgPath=d.path;
    loadBgs();
  } else {
    toast('❌ '+d.error,'e');
  }
}

// ── MUSIC ──
function loadMusic(){
  fetch('/api/music').then(r=>r.json()).then(d=>renderMusic(d.music)).catch(()=>{});
}
function renderMusic(tracks){
  const el=document.getElementById('mlist');
  const none=`<div class="mi${selMusicPath===''?' sel':''}" onclick="pickMusic('',this)">
    <span class="mii">🔇</span><span class="min">Không nhạc nền</span><span class="mck">✓</span></div>`;
  if(!tracks||!tracks.length){
    el.innerHTML=none+'<p style="color:var(--muted);font-size:10.5px;padding:7px">Bỏ nhạc vào <strong>studio_music/</strong></p>';
    return;
  }
  el.innerHTML=none+tracks.map(t=>`
    <div class="mi${t.path===selMusicPath?' sel':''}" onclick="pickMusic('${t.path}',this)">
      <span class="mii">🎵</span><span class="min">${t.name}</span>
      <span class="msz">${t.size}</span><span class="mck">✓</span></div>`).join('');
}
function pickMusic(path,el){
  selMusicPath=path; document.getElementById('selMusic').value=path;
  document.querySelectorAll('.mi').forEach(e=>e.classList.remove('sel'));
  el.classList.add('sel');
  if(path) toast('🎵 '+el.querySelector('.min').textContent,'i');
}
async function uploadMusic(inp){
  if(!inp.files[0]) return;
  const fd=new FormData(); fd.append('file',inp.files[0]);
  toast('⏳ Upload nhạc...','i');
  const res=await fetch('/api/upload-music',{method:'POST',body:fd});
  const d=await res.json();
  if(d.success){toast('✅ Upload nhạc OK!','s');loadMusic();}
  else toast('❌ '+d.error,'e');
}

// ── VOICE ──
function selVoice(v,el){
  document.getElementById('selVoice').value=v;
  document.querySelectorAll('.vc').forEach(c=>c.classList.remove('sel'));
  el.classList.add('sel');
}

// ── PROCESS VIDEO ──
async function processVideo(){
  const title=document.getElementById('title').value.trim();
  const script=document.getElementById('script').value.trim();
  if(!title){toast('⚠️ Nhập tiêu đề!','e');return;}
  if(!script){toast('⚠️ Nhập script!','e');return;}

  const btn=document.getElementById('procBtn');
  btn.disabled=true; btn.textContent='⏳ Đang xử lý...';
  document.getElementById('progWrap').style.display='block';
  setProg(0,'Đang khởi động pipeline...');

  const r=await fetch('/api/process',{
    method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({title,script,
      voice:document.getElementById('selVoice').value,
      bg_path:selBgPath, music_path:selMusicPath,
      description:title, tags:getTags()})
  });
  const d=await r.json();
  if(!d.job_id){
    toast('❌ '+(d.error||'Lỗi khởi động'),'e');
    btn.disabled=false; btn.textContent='🚀 Tạo Video Ngay'; return;
  }
  pollJob(d.job_id);
}

function pollJob(jid){
  if(pollTimer) clearInterval(pollTimer);
  pollTimer=setInterval(async()=>{
    const r=await fetch('/api/status/'+jid);
    const d=await r.json();
    setProg(d.progress||0, d.message||'...');
    if(d.status==='done'){
      clearInterval(pollTimer);
      toast('🎉 Video tạo xong!','s');
      const btn=document.getElementById('procBtn');
      btn.disabled=false; btn.textContent='🚀 Tạo Video Ngay';
      loadGallery(); loadHistory();
      setTimeout(()=>document.getElementById('gallery').scrollIntoView({behavior:'smooth'}),400);
    } else if(d.status==='error'){
      clearInterval(pollTimer);
      setProg(0,'❌ '+(d.error||'').substring(0,80));
      toast('❌ Lỗi pipeline — xem log terminal','e');
      const btn=document.getElementById('procBtn');
      btn.disabled=false; btn.textContent='🚀 Tạo Video Ngay';
    }
  },1200);
}

function setProg(p,msg){
  document.getElementById('progFill').style.width=p+'%';
  document.getElementById('progMsg').textContent=msg;
}

// ── GALLERY ──
async function loadGallery(){
  const r=await fetch('/api/videos');
  const d=await r.json();
  renderGallery(d.videos||[]);
}

function renderGallery(videos){
  const el=document.getElementById('videoGallery');
  if(!videos.length){
    el.innerHTML='<div class="empty"><div class="ei">🎬</div><div>Chưa có video. Điền form và nhấn <strong>Tạo Video Ngay</strong></div></div>';
    return;
  }
  el.innerHTML=[...videos].reverse().map(v=>`
    <div class="vcard ${v.status}" id="vcard_${v.id}">
      <div class="vc-head">
        <div class="vc-title">${esc(v.title)}</div>
        ${v.status==='uploaded'
          ?'<span class="badge badge-live">🔴 LIVE</span>'
          :'<span class="badge badge-ready">⏳ Chờ Upload</span>'}
      </div>
      <div class="vc-meta">
        <span>${v.voice==='vi-VN-HoaiMyNeural'?'👩 Hoài My (Nữ)':'👨 Nam Minh (Nam)'}</span>
        <span>⏱️ ${v.duration}s</span>
        <span>📅 ${(v.created_at||'').substring(0,16).replace('T',' ')}</span>
        ${v.music?'<span>🎵 '+v.music.split('/').pop()+'</span>':''}
      </div>
      <div class="vc-script">"${esc((v.script||'').substring(0,140))}${(v.script||'').length>140?'...':''}"</div>
      <div class="vc-player">
        <video controls width="196" height="348" preload="metadata"
               style="border-radius:9px;box-shadow:0 4px 16px rgba(0,0,0,.45)">
          <source src="/api/video-file/${v.video_name}" type="video/mp4">
        </video>
      </div>
      <!-- UPLOAD BOX — luôn hiện cho MỌI video -->
      <div class="vc-upload-box">
        <div class="vc-upload-label">📡 Upload lên YouTube</div>
        ${v.status==='uploaded'?`
          <div class="vc-uploaded-info">
            <span class="vc-yt-badge">✅ Đã upload</span>
            <a class="vc-yt-link" href="${v.youtube_url||'#'}" target="_blank">🔗 ${v.youtube_video_id||''}</a>
            <span style="font-size:10px;color:var(--muted)">Lúc ${(v.uploaded_at||'').substring(0,16).replace('T',' ')}</span>
          </div>
          <div class="reupload-row">
            <span style="font-size:10px;color:var(--muted)">Upload lại = tạo bản mới trên YT:</span>
            <button class="btn btn-reupload" onclick="doUpload('${v.id}',this,true)">🔁 Upload lại</button>
          </div>`:`
          <button class="btn btn-approve" id="upbtn_${v.id}" onclick="doUpload('${v.id}',this,false)">
            📡 Upload lên YouTube</button>`
        }
        <div class="upload-log" id="ulog_${v.id}" style="display:none"></div>
      </div>
      <div class="vc-actions">
        <button class="btn btn-del btn-sm" onclick="delVideo('${v.id}',this)">🗑️ Xóa</button>
        ${v.upload_count>0?'<span style="font-size:10px;color:var(--muted)">Đã upload '+v.upload_count+' lần</span>':''}
      </div>
    </div>`).join('');
}

function esc(s){return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;')}

// ── UPLOAD ──
async function doUpload(vid,btn,force){
  const msg=force
    ?'⚠️ Video đã có trên YouTube.\nUpload lại sẽ TẠO BẢN MỚI.\n\nXác nhận?'
    :'📡 Xác nhận upload video này lên YouTube?';
  if(!confirm(msg)) return;
  btn.disabled=true; btn.textContent='⏳ Đang upload...';
  ulog(vid,'i','📡 Bắt đầu upload YouTube API...');
  toast('📡 Đang upload lên YouTube...','i');

  const r=await fetch('/api/upload-youtube',{
    method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({video_id:vid,force})
  });
  const d=await r.json();
  if(d.success){
    ulog(vid,'s','✅ THÀNH CÔNG!  YT ID: '+d.youtube_video_id);
    ulog(vid,'s','🔗 '+d.youtube_url);
    ulog(vid,'s','🕐 '+new Date().toLocaleString('vi-VN'));
    toast('🎉 Upload OK! ID: '+d.youtube_video_id,'s');
    loadGallery(); loadHistory();
  } else {
    ulog(vid,'e','❌ THẤT BẠI: '+(d.error||'Lỗi không xác định'));
    ulog(vid,'e','💡 Xem log terminal để biết chi tiết');
    toast('❌ '+(d.error||'Upload thất bại').substring(0,70),'e');
    btn.disabled=false;
    btn.textContent=force?'🔁 Upload lại':'📡 Upload lên YouTube';
  }
}

function ulog(vid,type,msg){
  const el=document.getElementById('ulog_'+vid);
  if(!el) return;
  el.style.display='block';
  const c={i:'#3b82f6',s:'#10b981',e:'#ef4444',w:'#f59e0b'};
  const ts=new Date().toLocaleTimeString('vi-VN');
  el.innerHTML+=`<div style="color:${c[type]||'#e2e8f0'};font-size:10.5px;margin-bottom:1px"><span style="color:#475569">[${ts}]</span> ${msg}</div>`;
  el.scrollTop=el.scrollHeight;
}

// ── DELETE ──
async function delVideo(vid,btn){
  if(!confirm('Xóa video này? (File MP4 sẽ bị xóa)')) return;
  const r=await fetch('/api/delete-video',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({video_id:vid})});
  const d=await r.json();
  if(d.success){toast('🗑️ Đã xóa','i');loadGallery();}
  else toast('❌ '+d.error,'e');
}

// ── HISTORY ──
async function loadHistory(){
  const r=await fetch('/api/history');
  const d=await r.json();
  const up=(d.history||[]).filter(v=>v.status==='uploaded');
  const el=document.getElementById('histTable');
  if(!up.length){el.innerHTML='<p style="color:var(--muted);font-size:11.5px">Chưa có video nào upload lên YouTube.</p>';return;}
  el.innerHTML=`<table class="hist-table">
    <thead><tr><th>#</th><th>Tiêu đề</th><th>YT ID</th><th>Số lần</th><th>Thời gian</th><th>Link</th></tr></thead>
    <tbody>${[...up].reverse().map((v,i)=>`<tr>
      <td>${i+1}</td>
      <td style="max-width:180px;font-size:11px">${esc(v.title)}</td>
      <td><code style="color:var(--orange);font-size:10.5px">${v.youtube_video_id||''}</code></td>
      <td style="text-align:center">${v.upload_count||1}</td>
      <td style="font-size:10.5px">${(v.uploaded_at||'').substring(0,16).replace('T',' ')}</td>
      <td><a href="${v.youtube_url||'#'}" target="_blank" style="color:var(--green);font-weight:700;font-size:11px">🔗 Xem</a></td>
    </tr>`).join('')}</tbody></table>`;
}

// ── TOAST ──
let _tt=null;
function toast(msg,type='i'){
  const el=document.getElementById('toast');
  el.textContent=msg; el.className=type; el.style.display='block';
  if(_tt) clearTimeout(_tt);
  _tt=setTimeout(()=>el.style.display='none',4500);
}
</script>
</body>
</html>"""

# ════════════════════════════════════════════════════════
# FLASK ROUTES
# ════════════════════════════════════════════════════════
@app.route("/")
def index():
    log.info("UI page served")
    return render_template_string(HTML)

@app.route("/api/categories")
def api_categories():
    return jsonify({"categories": get_categories()})

@app.route("/api/auto-title")
def api_auto_title():
    cat  = request.args.get("category", "nikaya")
    bank = TITLE_BANKS.get(cat, TITLE_BANKS.get("nikaya", []))
    if not bank:
        bank = [(t, s) for lst in TITLE_BANKS.values() for t, s in lst]
    pick = random.choice(bank)
    log.info(f"Auto-title [{cat}]: {pick[0][:60]}")
    return jsonify({"title": pick[0], "script": pick[1], "bank_size": len(bank)})

@app.route("/api/backgrounds")
def api_backgrounds():
    bgs = []
    for ext in ["*.jpg","*.jpeg","*.png","*.webp"]:
        for f in sorted(BG_DIR.glob(ext)):
            entry = {"name": f.name, "path": str(f),
                     "size": f"{f.stat().st_size/1024:.0f}KB", "w": 0, "h": 0}
            if PIL_OK:
                try:
                    with Image.open(f) as im:
                        entry["w"], entry["h"] = im.width, im.height
                except: pass
            bgs.append(entry)
    log.info(f"BG list: {len(bgs)} files")
    return jsonify({"backgrounds": bgs})

@app.route("/api/bg-thumb")
def api_bg_thumb():
    path = request.args.get("path","")
    if path and os.path.exists(path):
        return send_file(path, mimetype="image/jpeg")
    svg = b'<svg xmlns="http://www.w3.org/2000/svg" width="80" height="80"><rect width="80" height="80" fill="#1e293b"/><text x="40" y="44" text-anchor="middle" fill="#64748b" font-size="14">IMG</text></svg>'
    return Response(svg, mimetype="image/svg+xml")

@app.route("/api/upload-bg", methods=["POST"])
def api_upload_bg():
    if "file" not in request.files:
        return jsonify({"success":False,"error":"Không có file"})
    f   = request.files["file"]
    ext = Path(f.filename).suffix.lower()
    if ext not in ALLOWED_IMAGE:
        return jsonify({"success":False,"error":f"Format không hỗ trợ: {ext}. Dùng JPG/PNG/WEBP"})
    dest = BG_DIR / f.filename
    f.save(str(dest))
    w = h = 0
    if PIL_OK:
        try:
            with Image.open(str(dest)) as im:
                w, h = im.width, im.height
        except: pass
    log.info(f"Upload BG: {f.filename} ({w}x{h}, {dest.stat().st_size//1024}KB)")
    # Log cảnh báo nếu sai tỉ lệ
    if w and h:
        ratio = w/h
        if w > h:
            log.warning(f"BG ảnh NẰM NGANG {w}x{h} — cần ảnh đứng 1080x1920 cho Shorts!")
        elif abs(ratio - 9/16) > 0.05:
            log.warning(f"BG tỉ lệ {w}x{h} ({ratio:.2f}) ≠ 9:16 (0.5625) — sẽ bị crop")
    return jsonify({"success":True, "name":f.filename, "path":str(dest), "w":w, "h":h})

@app.route("/api/music")
def api_music():
    tracks = []
    for ext in ["*.wav","*.mp3","*.aiff","*.m4a","*.ogg"]:
        for f in sorted(MUSIC_DIR.glob(ext)):
            sz = f.stat().st_size
            tracks.append({"name":f.name, "path":str(f),
                           "size":f"{sz/1024/1024:.1f}MB" if sz>1024*1024 else f"{sz/1024:.0f}KB"})
    log.info(f"Music list: {len(tracks)} files")
    return jsonify({"music": tracks})

@app.route("/api/upload-music", methods=["POST"])
def api_upload_music():
    if "file" not in request.files:
        return jsonify({"success":False,"error":"Không có file"})
    f   = request.files["file"]
    ext = Path(f.filename).suffix.lower()
    if ext not in ALLOWED_AUDIO:
        return jsonify({"success":False,"error":f"Format không hỗ trợ: {ext}"})
    dest = MUSIC_DIR / f.filename
    f.save(str(dest))
    log.info(f"Upload Music: {f.filename}")
    return jsonify({"success":True, "name":f.filename, "path":str(dest)})

@app.route("/api/process", methods=["POST"])
def api_process():
    params = request.get_json() or {}
    if not params.get("title") or not params.get("script"):
        return jsonify({"error":"Thiếu title hoặc script"}), 400
    job_id = str(uuid.uuid4())
    BUILD_JOBS[job_id] = {"status":"running","progress":0,"message":"Khởi động...","error":None}
    log.info(f"New job {job_id[:8]}: '{params.get('title','')[:50]}'")
    threading.Thread(target=build_video_job, args=(job_id, params), daemon=True).start()
    return jsonify({"job_id": job_id})

@app.route("/api/status/<job_id>")
def api_status(job_id):
    return jsonify(BUILD_JOBS.get(job_id, {"status":"not_found","progress":0,"message":"Job không tồn tại"}))

@app.route("/api/videos")
def api_videos():
    return jsonify({"videos": load_db()})

@app.route("/api/video-file/<filename>")
def api_video_file(filename):
    path = OUT_DIR / filename
    if path.exists():
        return send_file(str(path), mimetype="video/mp4", conditional=True)
    return "Not found", 404

@app.route("/api/upload-youtube", methods=["POST"])
def api_upload_youtube():
    data     = request.get_json() or {}
    video_id = data.get("video_id")
    force    = data.get("force", False)
    if not video_id:
        return jsonify({"success":False,"error":"Thiếu video_id"})

    db    = load_db()
    entry = next((v for v in db if v["id"]==video_id), None)
    if not entry:
        return jsonify({"success":False,"error":"Không tìm thấy video trong database"})

    if entry.get("status")=="uploaded" and not force:
        return jsonify({"success":False,"error":"Video đã upload rồi! Dùng nút 'Upload lại' để tạo bản mới."})

    vpath = entry.get("video_file","")
    if not vpath or not os.path.exists(vpath):
        return jsonify({"success":False,"error":f"File MP4 không tồn tại: {vpath}"})

    log.info(f"Upload: video={video_id[:8]} force={force} title='{entry['title'][:50]}'")
    yt_id, err = youtube_upload(vpath, entry["title"],
        entry.get("description",entry["title"]), entry.get("tags",["Thảo Dương TV","1995lido","Shorts"]))

    if yt_id:
        count = entry.get("upload_count",0) + 1
        update_db_entry(video_id,
            status="uploaded", youtube_video_id=yt_id,
            youtube_url=f"https://www.youtube.com/watch?v={yt_id}",
            uploaded_at=datetime.now().isoformat(), upload_count=count)
        log.info(f"Upload OK lần {count}: YT_ID={yt_id}")
        return jsonify({"success":True, "youtube_video_id":yt_id,
                        "youtube_url":f"https://www.youtube.com/watch?v={yt_id}"})
    else:
        log.error(f"Upload FAILED: {err}")
        return jsonify({"success":False,"error":err or "Upload thất bại"})

@app.route("/api/delete-video", methods=["POST"])
def api_delete_video():
    data  = request.get_json() or {}
    vid   = data.get("video_id")
    db    = load_db()
    entry = next((v for v in db if v["id"]==vid), None)
    if not entry:
        return jsonify({"success":False,"error":"Không tìm thấy"})
    vf = entry.get("video_file","")
    if vf and os.path.exists(vf):
        try: os.remove(vf)
        except: pass
    save_db([v for v in db if v["id"]!=vid])
    log.info(f"Deleted [{vid[:8]}] '{entry['title'][:40]}'")
    return jsonify({"success":True})

@app.route("/api/history")
def api_history():
    return jsonify({"history": load_db()})

# ════════════════════════════════════════════════════════
if __name__ == "__main__":
    cats = get_categories()
    total = sum(c["count"] for c in cats)
    print()
    print("=" * 64)
    print("  🎬 Manual Video Studio — @1995lido")
    print("=" * 64)
    print(f"  🌐 URL         : http://localhost:{PORT}")
    print(f"  📚 Kho nội dung: {total} bài ({len(cats)} thể loại)")
    for c in cats:
        print(f"     • {c['name']}: {c['count']} bài")
    print(f"  📂 Hình nền    : {BG_DIR}")
    print(f"  🎵 Nhạc nền    : {MUSIC_DIR}")
    print(f"  🎬 Output      : {OUT_DIR}")
    print(f"  📋 Log file    : {LOG_FILE}")
    print(f"  🕐 Khởi động   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 64)
    print("  📌 Nhấn Ctrl+C để dừng")
    print("=" * 64)
    print()
    app.run(host="0.0.0.0", port=PORT, debug=False, threaded=True)
