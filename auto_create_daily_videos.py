#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================
  auto_create_daily_videos.py
  Tự động tạo 5 video Shorts mỗi ngày — @1995lido
  Lịch phát: 08:00 · 11:00 · 18:00 · 20:00 · 21:30

  Cách dùng:
    python3 auto_create_daily_videos.py            ← Tạo hôm nay
    python3 auto_create_daily_videos.py --day 27   ← Tạo cho ngày 27
    python3 auto_create_daily_videos.py --range 6 30 ← Tạo từ ngày 6→30
    python3 auto_create_daily_videos.py --status   ← Xem tiến độ
=================================================================
"""

import os, sys, json, re, random, subprocess, shutil, time, argparse
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR   = Path(__file__).parent
BG_DIR     = BASE_DIR / "studio_backgrounds"
MUSIC_DIR  = BASE_DIR / "studio_music"
OUT_DIR    = BASE_DIR / "output_manual"
AUTO_DB    = BASE_DIR / "auto_schedule_db.json"   # DB riêng cho auto
UPLOAD_DB  = BASE_DIR / "manual_upload_log.json"  # DB chung với studio
LOG_FILE   = BASE_DIR / "auto_create.log"
FFMPEG     = "/Users/abc/bin/ffmpeg"
PYTHON     = sys.executable

# 5 slot phát mỗi ngày
DAILY_SLOTS = ["08:00", "11:00", "18:00", "20:00", "21:30"]
SLOT_LABELS = ["🌅 Sáng 8h", "☀️ Trưa 11h", "🌆 Chiều 18h", "🌙 Tối 20h", "⭐ Đêm 21h30"]

# ── Load Nikaya content ─────────────────────────────────
def load_title_bank():
    bank = {"nikaya": [], "deep_work": [], "healing": [], "discipline": [], "finance": [], "life_skills": []}

    # Load Nikaya từ JSON
    nj = BASE_DIR / "nikaya_30_authentic_posts.json"
    if nj.exists():
        try:
            data = json.loads(nj.read_text(encoding="utf-8"))
            for item in data:
                t = item.get("title","")
                s = item.get("script","")
                if t and s:
                    words = s.split()
                    if len(words) > 90:
                        s = " ".join(words[:85]) + " nhen!"
                    bank["nikaya"].append((t, s))
        except: pass

    # Deep work
    bank["deep_work"] = [
        ("Kỹ Thuật Time Boxing Nâng Cao — Làm Chủ 1 Ngày Không Xao Nhãng",
         "Dạ chào bạn nhen! Muốn hoàn thành việc khó mà không bị phân tâm? Chia ngày thành ô thời gian cố định, làm việc khó nhất 8h-10h, tắt mọi thông báo nhen! Đăng Ký Kênh Thảo Dương TV nhen!"),
        ("Quy Tắc 2 Phút Đánh Bại Sự Trì Hoãn Ngay Lập Tức",
         "Chào bạn nhen! Việc nào làm dưới 2 phút thì giải quyết ngay. Bạn sẽ thấy nhẹ đầu vô cùng sau 1 tuần áp dụng nhen! Đăng Ký Kênh Thảo Dương TV nhen!"),
        ("5 Phút Sáng Quyết Định Năng Suất Cả Ngày Của Bạn",
         "Dạ chào bạn nhen! Đừng mở điện thoại khi vừa thức. Hít thở 10 nhịp, uống nước và viết 3 việc quan trọng nhất hôm nay nhen! Đăng Ký Kênh Thảo Dương TV nhen!"),
        ("Tại Sao Người Thành Công Thức Dậy Sớm Hơn Bạn 1 Tiếng",
         "Chào bạn nhen! 1 tiếng sáng yên tĩnh không thông báo bằng 3 tiếng làm việc ban ngày. Thử thức 5h sáng 7 ngày và xem sự khác biệt nhen! Thảo Dương TV nhen!"),
        ("Ngừng Đa Nhiệm — Làm Một Việc Hiệu Quả Hơn 5 Việc Cùng Lúc",
         "Dạ chào bạn nhen! Mỗi lần chuyển việc tốn 23 phút để lấy lại tập trung. Hãy làm 1 việc đến hết rồi mới sang việc khác nhen! Thảo Dương TV nhen!"),
        ("Ma Trận Eisenhower — Phân Loại Công Việc Để Làm Đúng Việc",
         "Chào bạn nhen! Quan trọng và khẩn: làm ngay. Quan trọng nhưng không khẩn: lên kế hoạch. Không quan trọng nhưng khẩn: ủy thác. Còn lại: loại bỏ nhen! Thảo Dương TV nhen!"),
        ("Phương Pháp Deep Work Của Cal Newport — 1 Giờ Bằng 4 Giờ",
         "Dạ chào bạn nhen! 1 giờ tập trung tuyệt đối không gián đoạn bằng 4 giờ làm việc thông thường. Tắt wifi, đặt đồng hồ và không nhìn điện thoại nhen! Thảo Dương TV nhen!"),
        ("Tại Sao Bạn Mệt Dù Không Làm Gì — Decision Fatigue",
         "Chào bạn nhen! Mỗi quyết định nhỏ trong ngày đều tiêu tốn năng lượng não. Hãy tự động hóa những quyết định nhỏ để dành sức cho việc quan trọng nhen! Thảo Dương TV nhen!"),
    ]

    # Healing
    bank["healing"] = [
        ("Khi Sự Nhiệt Huyết Biến Mất — Vượt Qua Tê Liệt Cảm Xúc",
         "Dạ chào bạn nhen... Nếu hôm nay bạn thấy cạn kiệt đừng gồng mình. Cho phép bản thân nghỉ ngơi 15 phút và lắng nghe hơi thở nhen! Đăng Ký Kênh Thảo Dương TV nhen!"),
        ("Nghệ Thuật Buông Bỏ Kỳ Vọng — Giải Tỏa Áp Lực So Sánh",
         "Dạ chào bạn nhen! Mỗi người có múi giờ phát triển riêng. Đừng so sánh trang đầu của bạn với trang 20 của người khác nhen! Thảo Dương TV nhen!"),
        ("Học Cách Nói KHÔNG Mà Không Cảm Thấy Áy Nấy",
         "Chào bạn nhen! Mỗi lần nói CÓ khi mệt là bạn đang nói KHÔNG với chính mình. Bảo vệ năng lượng bản thân là điều thiết yếu nhen! Thảo Dương TV nhen!"),
        ("5 Dấu Hiệu Bạn Đang Burnout — Nhận Ra Trước Khi Quá Muộn",
         "Dạ chào bạn nhen! Mệt mỏi dù ngủ đủ, không vui khi hoàn thành việc, dễ cáu gắt... Đây là dấu hiệu burnout. Hãy dừng lại chăm sóc bản thân nhen! Thảo Dương TV nhen!"),
        ("Kỹ Thuật 5-4-3-2-1 Chặn Cơn Lo Âu Trong 60 Giây",
         "Dạ chào bạn nhen! Khi lo âu tấn công: nhìn 5 thứ, nghe 4 âm thanh, chạm 3 bề mặt, ngửi 2 mùi, nếm 1 vị. Não quay về hiện tại ngay nhen! Thảo Dương TV nhen!"),
        ("Tại Sao Người Mạnh Mẽ Cũng Cần Được Khóc Đôi Khi",
         "Chào bạn nhen... Nước mắt không phải yếu đuối. Khóc giải phóng cortisol dư thừa. Cho phép mình cảm nhận cảm xúc để tiếp tục mạnh mẽ hơn nhen! Thảo Dương TV nhen!"),
        ("Làm Sao Để Tha Thứ Cho Người Làm Mình Đau",
         "Chào bạn nhen! Tha thứ không phải vì họ xứng đáng mà vì bạn xứng đáng sống nhẹ nhàng. Tha thứ là món quà bạn tặng cho chính mình nhen! Thảo Dương TV nhen!"),
        ("Cách Thoát Khỏi Vòng Lặp Overthinking Mỗi Đêm",
         "Dạ chào bạn nhen! Khi não không tắt được hãy viết ra giấy tất cả lo lắng. Não nhận ra đã lưu trữ và cho phép bạn nghỉ ngơi nhen! Thảo Dương TV nhen!"),
    ]

    # Discipline
    bank["discipline"] = [
        ("Atomic Habits — Thay Đổi 1% Mỗi Ngày Để Tạo Bước Nhảy Vọt",
         "Dạ chào bạn nhen! Cải thiện 1% mỗi ngày, sau 1 năm bạn sẽ tốt hơn 37 lần. Đừng cố thay đổi tất cả, bắt đầu từ 1 thói quen nhỏ thôi nhen! Thảo Dương TV nhen!"),
        ("Habit Stacking — Ghép Thói Quen Mới Vào Thói Quen Cũ",
         "Chào bạn nhen! Sau pha cà phê thì thiền 5 phút. Sau đánh răng thì đọc sách 10 trang. Ghép thói quen mới vào trigger quen thuộc giúp bạn duy trì dễ hơn nhen! Thảo Dương TV nhen!"),
        ("No-Zero Day — Không Ngày Nào Là Ngày Trống Rỗng",
         "Chào bạn nhen! Dù bận đến đâu hãy làm ít nhất 1 việc hướng đến mục tiêu. Chỉ 1 trang sách hay 10 cái squat cũng đủ. Đừng để ngày nào là zero day nhen! Thảo Dương TV nhen!"),
        ("Sức Mạnh Của Journaling — Viết Nhật Ký 10 Phút Mỗi Tối",
         "Dạ chào bạn nhen! Viết ra những gì đang nghĩ giúp não giải phóng căng thẳng và đưa ra quyết định sáng suốt hơn. Chỉ cần bút và giấy nhen! Thảo Dương TV nhen!"),
        ("Tại Sao Kỷ Luật Quan Trọng Hơn Cảm Hứng 100 Lần",
         "Dạ chào bạn nhen! Cảm hứng đến rồi đi nhưng kỷ luật ở lại. Người thành công không chờ cảm hứng, họ làm vì đó là thói quen không thể thiếu nhen! Thảo Dương TV nhen!"),
        ("Cách Xây Dựng Buổi Sáng 30 Phút Thay Đổi Cả Đời",
         "Chào bạn nhen! 5 phút thiền, 10 phút vận động nhẹ, 5 phút viết nhật ký, 10 phút đọc sách. 30 phút sáng đủ nạp năng lượng cho cả ngày nhen! Thảo Dương TV nhen!"),
    ]

    # Finance
    bank["finance"] = [
        ("Quy Tắc 50-30-20 — Phân Chia Thu Nhập Thông Minh",
         "Dạ chào bạn nhen! 50% cho nhu cầu thiết yếu, 30% cho bản thân, 20% tiết kiệm đầu tư. Quy tắc đơn giản giúp bạn không bao giờ hết tiền cuối tháng nhen! Thảo Dương TV nhen!"),
        ("Tại Sao Phải Tiết Kiệm Ngay Cả Khi Thu Nhập Thấp",
         "Chào bạn nhen! Tiết kiệm không phải về số tiền mà là thói quen. Bắt đầu từ 50 nghìn mỗi tháng để não quen với việc trữ tiền nhen! Thảo Dương TV nhen!"),
        ("Emergency Fund — Tại Sao Cần 6 Tháng Chi Phí Dự Phòng",
         "Dạ chào bạn nhen! Khi mất việc hay bệnh tật ập đến, bạn có 6 tháng xoay sở mà không phải vay nợ. Đây là lớp giáp tài chính quan trọng nhất nhen! Thảo Dương TV nhen!"),
    ]

    # Life skills
    bank["life_skills"] = [
        ("Nghệ Thuật Lắng Nghe Chủ Động — Kỹ Năng Hiếm Người Có",
         "Dạ chào bạn nhen! 80% mâu thuẫn vì không thực sự lắng nghe. Tắt màn hình, nhìn vào mắt người nói và phản chiếu lại những gì họ vừa nói nhen! Thảo Dương TV nhen!"),
        ("First Impression — 7 Giây Đầu Quyết Định Mọi Thứ",
         "Dạ chào bạn nhen! Trong 7 giây đầu não đã đánh giá bạn qua tư thế, ánh mắt và nụ cười. Đứng thẳng, nhìn thẳng và mỉm cười chân thành nhen! Thảo Dương TV nhen!"),
        ("Tại Sao Người Ít Nói Lại Thường Được Tin Tưởng Hơn",
         "Dạ chào bạn nhen! Người ít nói nhưng nói đúng lúc thường được đánh giá cao hơn. Lọc trước khi nói: thật không, cần thiết không, tử tế không nhen! Thảo Dương TV nhen!"),
    ]

    return bank


# ── DB helpers ─────────────────────────────────────────
def load_auto_db():
    if AUTO_DB.exists():
        try: return json.loads(AUTO_DB.read_text(encoding="utf-8"))
        except: pass
    return {"created": [], "uploaded": [], "schedule": {}}

def save_auto_db(data):
    AUTO_DB.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def load_upload_db():
    if UPLOAD_DB.exists():
        try: return json.loads(UPLOAD_DB.read_text(encoding="utf-8"))
        except: pass
    return []

def save_upload_db(data):
    UPLOAD_DB.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def log_print(msg, level="INFO"):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    icons = {"INFO":"✅","WARN":"⚠️ ","ERROR":"❌","STEP":"🔵"}
    ic = icons.get(level, "  ")
    line = f"[{ts}] {ic} {msg}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


# ── Build 1 video (no Flask) ──────────────────────────
def build_one_video(title, script, voice, bg_path, music_path, tags, description=""):
    import uuid
    job_id  = str(uuid.uuid4())
    safe    = re.sub(r"[^\w]", "_", title[:40])
    ts      = datetime.now().strftime("%Y%m%d_%H%M%S")
    vname   = f"auto_{ts}_{safe}.mp4"
    out     = OUT_DIR / vname
    pfx     = str(BASE_DIR / "studio_tmp" / f"tmp_{job_id[:8]}")
    OUT_DIR.mkdir(exist_ok=True)
    (BASE_DIR / "studio_tmp").mkdir(exist_ok=True)

    log_print(f"BUILD: {title[:60]}", "STEP")

    try:
        from PIL import Image, ImageDraw, ImageFont
        PIL_OK = True
    except: PIL_OK = False

    # Step 1: BG
    log_print(f"  Step 1: BG = {Path(bg_path).name}")
    tc = pfx + "_tc.jpg"
    if PIL_OK:
        try:
            img = Image.open(bg_path).convert("RGBA")
            W,H = img.size
            ov  = Image.new("RGBA",(W,H),(0,0,0,0))
            dr  = ImageDraw.Draw(ov)
            cl,cr = int(W*.06),int(W*.94)
            ct,cb = int(H*.15),int(H*.48)
            dr.rounded_rectangle([cl,ct,cr,cb],radius=28,fill=(15,23,42,215),outline=(255,215,0,180),width=3)
            try:
                fn = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc",index=1,size=50)
            except: fn = ImageFont.load_default()
            words = title.split(); lines,curr = [],""
            for w in words:
                t2 = f"{curr} {w}".strip()
                if len(t2)<=20: curr=t2
                else:
                    if curr: lines.append(curr)
                    curr=w
            if curr: lines.append(curr)
            y = ct+72
            for line in lines[:4]:
                dr.text((cl+28,y),line,fill=(255,255,255),font=fn); y+=56
            Image.alpha_composite(img,ov).convert("RGB").save(tc,quality=95)
        except Exception as e:
            log_print(f"  Title card lỗi: {e} — dùng ảnh gốc","WARN")
            shutil.copy(bg_path, tc)
    else:
        shutil.copy(bg_path, tc)

    # Step 2: TTS
    log_print(f"  Step 2: TTS ({voice})")
    clean = re.sub(r"\s+"," ",re.sub(
        r"[^\w\s\.,!?àáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđÀÁẢÃẠÂẦẤẨẪẬĂẰẮẲẴẶÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ]",
        " ", script)).strip()
    tts_mp3 = pfx+"_s.mp3"; tts_wav=pfx+"_s.wav"; proc_wav=pfx+"_p.wav"; mix_wav=pfx+"_m.wav"

    ok = False
    for att in range(3):
        r = subprocess.run(["/Users/abc/Library/Python/3.9/bin/edge-tts", "--voice", voice, "--text", clean, "--write-media", tts_mp3],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=90)
        if r.returncode==0 and os.path.exists(tts_mp3) and os.path.getsize(tts_mp3)>500:
            ok=True; break
        log_print(f"  TTS attempt {att+1} thất bại","WARN"); time.sleep(3)
    if not ok:
        raise RuntimeError("TTS thất bại sau 3 lần — kiểm tra kết nối internet hoặc cài edge-tts")

    # Step 3: Audio EQ
    log_print("  Step 3: Audio EQ + Mix nhạc")
    for cmd in [
        [FFMPEG,"-y","-i",tts_mp3,tts_wav],
        [FFMPEG,"-y","-i",tts_wav,"-af","equalizer=f=250:width_type=h:width=200:g=3.5,equalizer=f=3500:width_type=h:width=1200:g=2.0,lowpass=f=6000",proc_wav]
    ]:
        r = subprocess.run(cmd,capture_output=True,timeout=60)
        if r.returncode!=0:
            raise RuntimeError(f"FFmpeg audio lỗi: {r.stderr.decode()[-200:]}")

    # Duration
    rd  = subprocess.run([FFMPEG,"-i",proc_wav],stderr=subprocess.PIPE,timeout=10)
    dur = 32.0
    for line in rd.stderr.decode().split("\n"):
        if "Duration:" in line:
            try:
                p = line.split("Duration:")[1].split(",")[0].strip().split(":")
                dur = float(p[0])*3600+float(p[1])*60+float(p[2])
            except: pass
            break

    if music_path and os.path.exists(music_path):
        r = subprocess.run([FFMPEG,"-y","-i",proc_wav,"-i",music_path,
            "-filter_complex","[0:a]volume=1.35[a0];[1:a]volume=0.22[a1];[a0][a1]amix=inputs=2:duration=first[aout]",
            "-map","[aout]",mix_wav],capture_output=True,timeout=90)
        if r.returncode!=0: shutil.copy(proc_wav,mix_wav)
    else:
        shutil.copy(proc_wav,mix_wav)

    # Step 4: Encode
    log_print(f"  Step 4: FFmpeg encode ({dur:.1f}s)")
    all_bgs = sorted([str(f) for ext in ["*.jpg","*.png","*.jpeg","*.webp"]
                      for f in BG_DIR.glob(ext) if str(f)!=bg_path])
    img1=tc; img2=all_bgs[0] if len(all_bgs)>=1 else img1; img3=all_bgs[1] if len(all_bgs)>=2 else img1
    d1,d2,d3 = dur*.35,dur*.30,dur*.35
    fc = (f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,loop=loop=-1:size=1:start=0,setpts=N/TB[v0];"
          f"[1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,loop=loop=-1:size=1:start=0,setpts=N/TB[v1];"
          f"[2:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,loop=loop=-1:size=1:start=0,setpts=N/TB[v2];"
          f"[v0][v1][v2]concat=n=3:v=1:a=0[outv]")
    r = subprocess.run([FFMPEG,"-y",
        "-loop","1","-t",str(d1),"-i",img1,
        "-loop","1","-t",str(d2),"-i",img2,
        "-loop","1","-t",str(d3),"-i",img3,
        "-i",mix_wav,"-filter_complex",fc,"-map","[outv]","-map","3:a",
        "-c:v","libx264","-pix_fmt","yuv420p","-r","30",
        "-c:a","aac","-b:a","192k","-shortest",str(out)],
        capture_output=True,text=True,timeout=300)
    if r.returncode!=0 or not out.exists():
        raise RuntimeError(f"FFmpeg encode lỗi: {r.stderr}")

    sz = out.stat().st_size/1024/1024
    log_print(f"  ✅ OK: {vname} ({sz:.2f}MB)")

    # Cleanup tmp
    for f in (BASE_DIR/"studio_tmp").glob(f"tmp_{job_id[:8]}*"):
        try: f.unlink()
        except: pass

    return {
        "id": job_id, "created_at": datetime.now().isoformat(),
        "title": title, "script": script, "voice": voice,
        "bg_image": bg_path, "music": music_path or "",
        "video_file": str(out), "video_name": vname,
        "duration": round(dur,1), "description": description or title,
        "tags": tags, "status": "ready",
        "youtube_video_id": None, "youtube_url": None,
        "uploaded_at": None, "upload_count": 0,
    }


# ── Tạo 5 video cho 1 ngày ─────────────────────────────
def create_videos_for_day(target_day: int, force=False):
    """Tạo 5 video cho ngày `target_day` trong tháng hiện tại"""
    now = datetime.now()
    base_dt = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    target_dt = base_dt + timedelta(days=target_day - 1)
    day_key   = target_dt.strftime("%Y-%m-%d")

    auto_db = load_auto_db()
    schedule = auto_db.get("schedule", {})

    if day_key in schedule and not force:
        done  = sum(1 for s in schedule[day_key] if s.get("video_created"))
        total = len(schedule[day_key])
        log_print(f"Ngày {day_key}: đã tạo {done}/{total} video (dùng --force để tạo lại)","WARN")
        return

    bank     = load_title_bank()
    all_cats = list(bank.keys())

    # Chọn BG
    bgs    = sorted(list(BG_DIR.glob("*.jpg")) + list(BG_DIR.glob("*.png")) + list(BG_DIR.glob("*.webp")))
    musics = sorted(list(MUSIC_DIR.glob("*.wav")) + list(MUSIC_DIR.glob("*.mp3")))

    if not bgs:
        log_print("Không có hình nền trong studio_backgrounds/! Không thể tạo video.","ERROR")
        return

    # Shuffle để không dùng cùng thứ tự
    random.shuffle(bgs)
    random.shuffle(musics)

    # Luân phiên category cho 5 slot
    slot_cats = []
    # Ưu tiên Nikaya cho 1 slot, còn lại xoay vòng
    prio_cats = ["nikaya", "deep_work", "healing", "discipline", "life_skills"]
    for i in range(5):
        slot_cats.append(prio_cats[i % len(prio_cats)])

    day_schedule = []
    upload_db    = load_upload_db()

    log_print(f"=== Bắt đầu tạo 5 video cho ngày {day_key} ===")

    for i, (slot_time, slot_label) in enumerate(zip(DAILY_SLOTS, SLOT_LABELS)):
        cat        = slot_cats[i]
        cat_bank   = bank.get(cat, [])
        if not cat_bank:
            cat      = random.choice(all_cats)
            cat_bank = bank[cat]

        # Chọn bài chưa dùng hôm nay
        used_titles = [s["title"] for s in day_schedule]
        available   = [item for item in cat_bank if item[0] not in used_titles]
        if not available:
            available = cat_bank  # fallback: dùng lại

        title, script = random.choice(available)
        bg_path       = str(bgs[i % len(bgs)])
        music_path    = str(musics[i % len(musics)]) if musics else ""
        voice         = "vi-VN-HoaiMyNeural" if i % 2 == 0 else "vi-VN-NamMinhNeural"
        tags          = ["Thảo Dương TV","1995lido","Shorts",cat.replace("_"," ")]

        # Thời gian dự kiến phát
        h, m = slot_time.split(":")
        scheduled_at = target_dt.replace(hour=int(h), minute=int(m)).isoformat()

        log_print(f"\n[{i+1}/5] {slot_label} — {cat} — {title[:55]}")

        entry = {
            "slot": slot_time, "slot_label": slot_label, "scheduled_at": scheduled_at,
            "category": cat, "title": title, "voice": voice,
            "bg": bg_path, "music": music_path,
            "video_created": False, "video_name": None, "video_id": None,
        }

        try:
            result = build_one_video(
                title=title, script=script, voice=voice,
                bg_path=bg_path, music_path=music_path,
                tags=tags, description=title
            )
            entry.update({
                "video_created": True,
                "video_name":    result["video_name"],
                "video_id":      result["id"],
                "created_at":    result["created_at"],
            })
            upload_db.append(result)
            log_print(f"  ✅ Video tạo xong: {result['video_name']}")
        except Exception as e:
            log_print(f"  ❌ Lỗi tạo video slot {slot_time}: {e}","ERROR")

        day_schedule.append(entry)
        time.sleep(1)  # Nghỉ 1 giây giữa các video

    schedule[day_key] = day_schedule
    auto_db["schedule"] = schedule
    save_auto_db(auto_db)
    save_upload_db(upload_db)

    done = sum(1 for s in day_schedule if s["video_created"])
    log_print(f"\n=== Ngày {day_key}: Tạo {done}/5 video thành công ===")
    log_print(f"  📂 Xem video tại: {OUT_DIR}")
    log_print(f"  🌐 Review tại: http://localhost:8098")
    return done


# ── Xem status ─────────────────────────────────────────
def show_status():
    auto_db  = load_auto_db()
    schedule = auto_db.get("schedule", {})
    if not schedule:
        print("Chưa có lịch nào được tạo.")
        return

    upload_db = load_upload_db()
    uploaded  = {v["id"]: v for v in upload_db if v.get("status")=="uploaded"}

    print(f"\n{'='*70}")
    print(f"  📊 TRẠNG THÁI AUTO SCHEDULE — @1995lido")
    print(f"{'='*70}")

    total_created  = 0
    total_uploaded = 0

    for day_key in sorted(schedule.keys()):
        slots = schedule[day_key]
        day_created  = sum(1 for s in slots if s.get("video_created"))
        day_uploaded = sum(1 for s in slots if s.get("video_id") and s.get("video_id") in uploaded)
        total_created  += day_created
        total_uploaded += day_uploaded

        status_icon = "✅" if day_created==5 else ("⚠️ " if day_created>0 else "❌")
        print(f"\n  {status_icon} {day_key} — {day_created}/5 tạo · {day_uploaded}/5 upload")
        for s in slots:
            vid_ok  = "🎬" if s.get("video_created") else "  "
            up_ok   = "📡" if s.get("video_id") and s.get("video_id") in uploaded else "  "
            print(f"      {s['slot']} {vid_ok}{up_ok} {s['title'][:50]}")

    print(f"\n{'─'*70}")
    print(f"  Tổng: {total_created} video tạo · {total_uploaded} video upload")
    print(f"  DB:   {AUTO_DB}")
    print(f"  Log:  {LOG_FILE}")
    print(f"{'='*70}\n")


# ── Setup crontab (ngày 6-30) ──────────────────────────
def setup_crontab(start_day=6, end_day=30):
    """Cài crontab để tạo 5 video mỗi ngày lúc 2:00 AM cho ngày start_day→end_day"""
    python  = PYTHON
    script  = str(Path(__file__).resolve())
    now     = datetime.now()
    month   = now.month
    year    = now.year

    cron_lines = []
    cron_lines.append(f"# @1995lido auto video scheduler — {now.strftime('%Y-%m-%d')}")
    cron_lines.append(f"MAILTO=\"\"")
    cron_lines.append("")

    # Tạo 5 video lúc 2:00 AM mỗi ngày (đủ thời gian trước các giờ phát)
    days_str = ",".join(str(d) for d in range(start_day, end_day+1))
    cron_lines.append(f"# Tạo 5 video — chạy 2h sáng ngày {start_day}-{end_day} tháng {month}")
    cron_lines.append(f"0 2 {days_str} {month} * {python} {script} --today >> {LOG_FILE} 2>&1")
    cron_lines.append("")

    cron_text = "\n".join(cron_lines)

    # Lấy crontab hiện tại
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    current = result.stdout if result.returncode == 0 else ""

    # Xóa các dòng cũ của script này
    filtered_lines = []
    for line in current.split("\n"):
        if script not in line and "auto video scheduler" not in line and "1995lido auto" not in line:
            filtered_lines.append(line)
    new_crontab = "\n".join(filtered_lines).strip() + "\n\n" + cron_text + "\n"

    # Ghi crontab mới
    proc = subprocess.run(["crontab", "-"], input=new_crontab, text=True, capture_output=True)
    if proc.returncode == 0:
        log_print(f"✅ Crontab đã cài! Chạy lúc 2:00 AM mỗi ngày {start_day}-{end_day} tháng {month}")
        print("\n--- Crontab đã cài ---")
        print(cron_text)
        print("----------------------")
        print("Xem crontab: crontab -l")
        print("Xóa crontab: crontab -r")
    else:
        log_print(f"❌ Lỗi cài crontab: {proc.stderr}","ERROR")


# ── Main ────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Auto tạo 5 video Shorts mỗi ngày — @1995lido",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ:
  python3 auto_create_daily_videos.py              → Tạo video hôm nay
  python3 auto_create_daily_videos.py --today      → Tạo video hôm nay (dùng trong cron)
  python3 auto_create_daily_videos.py --day 27     → Tạo cho ngày 27
  python3 auto_create_daily_videos.py --range 6 30 → Tạo từ ngày 6 đến 30
  python3 auto_create_daily_videos.py --status     → Xem tiến độ
  python3 auto_create_daily_videos.py --setup-cron → Cài crontab tự động
        """
    )
    parser.add_argument("--today",      action="store_true", help="Tạo 5 video cho hôm nay")
    parser.add_argument("--day",        type=int,            help="Tạo cho ngày cụ thể (1-31)")
    parser.add_argument("--range",      type=int, nargs=2,   help="Tạo từ ngày X đến ngày Y (--range 6 30)")
    parser.add_argument("--status",     action="store_true", help="Xem trạng thái tiến độ")
    parser.add_argument("--setup-cron", action="store_true", help="Cài crontab ngày 6-30")
    parser.add_argument("--force",      action="store_true", help="Tạo lại dù đã tạo rồi")
    args = parser.parse_args()

    log_print("=" * 60)
    log_print(f"Auto Create Daily Videos — @1995lido — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log_print("=" * 60)

    if args.status:
        show_status()

    elif args.setup_cron:
        setup_crontab(start_day=6, end_day=30)

    elif args.range:
        s, e = args.range
        log_print(f"🗓️  Tạo video từ ngày {s} đến {e}")
        total = 0
        for day in range(s, e+1):
            try:
                n = create_videos_for_day(day, force=args.force)
                if n: total += n
                log_print(f"  Nghỉ 10 giây trước khi tạo ngày tiếp...")
                time.sleep(10)
            except Exception as ex:
                log_print(f"Ngày {day} lỗi: {ex}","ERROR")
        log_print(f"\n✅ Tổng kết: {total} video đã tạo cho ngày {s}-{e}")

    elif args.day:
        create_videos_for_day(args.day, force=args.force)

    elif args.today or len(sys.argv)==1:
        create_videos_for_day(datetime.now().day, force=args.force)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
