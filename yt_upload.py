#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================
  yt_upload.py — Upload video lên YouTube từ Terminal
  @1995lido · Kênh Thảo Dương TV

  Cách dùng:
    # Upload 1 file
    python3 yt_upload.py video.mp4

    # Upload nhiều file
    python3 yt_upload.py video1.mp4 video2.mp4 video3.mp4

    # Upload cả folder
    python3 yt_upload.py --folder output_manual/

    # Upload với tiêu đề tùy chỉnh
    python3 yt_upload.py video.mp4 --title "Tiêu đề video"

    # Upload folder với tiêu đề prefix
    python3 yt_upload.py --folder output_manual/ --prefix "Thảo Dương TV:"

    # Chọn privacy (public/unlisted/private)
    python3 yt_upload.py video.mp4 --privacy unlisted

    # Xem danh sách video đã upload (không upload lại)
    python3 yt_upload.py --history

    # Upload nhưng bỏ qua các file đã upload rồi
    python3 yt_upload.py --folder output_manual/ --skip-uploaded
=================================================================
"""

import os, sys, json, re, argparse, time
from datetime import datetime
from pathlib import Path

BASE_DIR   = Path(__file__).parent
TOKEN_FILE = BASE_DIR / "token.json"
UPLOAD_LOG = BASE_DIR / "yt_terminal_upload_log.json"   # Log riêng cho terminal upload
MAIN_LOG   = BASE_DIR / "manual_upload_log.json"         # Log chính của studio
REPORT_LOG = BASE_DIR / "upload_short_report.log"        # Báo cáo auto-short upload

VIDEO_EXTS = {".mp4", ".mov", ".avi", ".mkv", ".webm"}

# ── ANSI Colors ────────────────────────────────────────
R = "\033[0m"
BOLD   = "\033[1m"
GREEN  = "\033[32m"
RED    = "\033[31m"
YELLOW = "\033[33m"
CYAN   = "\033[36m"
PURPLE = "\033[35m"
BLUE   = "\033[34m"
GRAY   = "\033[90m"

def c(color, text): return f"{color}{text}{R}"
def ok(msg):   print(f"{GREEN}✅ {msg}{R}")
def err(msg):  print(f"{RED}❌ {msg}{R}")
def warn(msg): print(f"{YELLOW}⚠️  {msg}{R}")
def info(msg): print(f"{CYAN}ℹ️  {msg}{R}")
def step(msg): print(f"{BLUE}🔵 {msg}{R}")

# ── Log helpers ────────────────────────────────────────
def load_log():
    if UPLOAD_LOG.exists():
        try: return json.loads(UPLOAD_LOG.read_text(encoding="utf-8"))
        except: pass
    return []

def save_log(data):
    UPLOAD_LOG.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def load_main_log():
    if MAIN_LOG.exists():
        try: return json.loads(MAIN_LOG.read_text(encoding="utf-8"))
        except: pass
    return []

def get_uploaded_files():
    """Trả về set các filepath đã upload (từ cả 2 log)"""
    uploaded = set()
    for entry in load_log():
        if entry.get("status") == "uploaded":
            uploaded.add(entry.get("file_path", ""))
            uploaded.add(entry.get("file_name", ""))
    for entry in load_main_log():
        if entry.get("status") == "uploaded":
            uploaded.add(entry.get("video_file", ""))
            uploaded.add(entry.get("video_name", ""))
    return uploaded

# ── YouTube OAuth ──────────────────────────────────────
import urllib.request, urllib.parse, urllib.error

def get_tokens():
    if not TOKEN_FILE.exists():
        err(f"Không tìm thấy token.json tại: {TOKEN_FILE}")
        print(f"{YELLOW}   Fix: chạy python3 setup_token_direct.py{R}")
        return None
    tokens = json.loads(TOKEN_FILE.read_text(encoding="utf-8"))
    if "refresh_token" not in tokens:
        err("token.json thiếu refresh_token")
        print(f"{YELLOW}   Fix: chạy python3 setup_token_direct.py{R}")
        return None
    return refresh_token(tokens)

def refresh_token(tokens):
    try:
        data = urllib.parse.urlencode({
            "client_id":     tokens["client_id"],
            "client_secret": tokens["client_secret"],
            "refresh_token": tokens["refresh_token"],
            "grant_type":    "refresh_token"
        }).encode("utf-8")
        req = urllib.request.Request(
            tokens.get("token_uri", "https://oauth2.googleapis.com/token"),
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        with urllib.request.urlopen(req) as r:
            tokens["access_token"] = json.loads(r.read().decode())["access_token"]
        TOKEN_FILE.write_text(json.dumps(tokens, indent=2), encoding="utf-8")
        return tokens
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="ignore")
        err(f"Refresh token thất bại: HTTP {e.code} — {body[:200]}")
        return None
    except Exception as e:
        err(f"Refresh token lỗi: {e}")
        return None

# ── Sinh tiêu đề từ tên file ───────────────────────────
def title_from_filename(filepath, prefix=""):
    stem = Path(filepath).stem
    # Xóa timestamp prefix kiểu: manual_20260825_143022_
    stem = re.sub(r"^(manual|auto)_\d{8}_\d{6}_?", "", stem)
    # Thay _ và - thành space
    stem = re.sub(r"[_\-]+", " ", stem).strip()
    # Capitalize từng từ
    title = " ".join(w.capitalize() for w in stem.split())
    if prefix:
        title = f"{prefix.rstrip()} {title}"
    return title or Path(filepath).name

# ── Upload 1 file ──────────────────────────────────────
def upload_one(filepath, title, description, tags, privacy, tokens):
    """
    Upload 1 file video lên YouTube.
    Return: (youtube_video_id, error_message)
    """
    file_size = os.path.getsize(filepath)
    size_mb   = file_size / 1024 / 1024

    print(f"\n{BOLD}{'─'*60}{R}")
    print(f"  📁 File   : {c(CYAN, Path(filepath).name)}")
    print(f"  📝 Tiêu đề: {c(BOLD, title[:70])}")
    print(f"  📦 Size   : {c(YELLOW, f'{size_mb:.1f} MB')}")
    print(f"  🔒 Privacy: {c(PURPLE, privacy)}")
    print(f"{BOLD}{'─'*60}{R}")

    metadata = {
        "snippet": {
            "title":       title[:100],
            "description": description,
            "tags":        tags,
            "categoryId":  "22"
        },
        "status": {
            "privacyStatus": privacy,
            "selfMade":      True
        }
    }

    # Tạo resumable session
    step("Tạo upload session...")
    try:
        req = urllib.request.Request(
            "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
            data=json.dumps(metadata).encode("utf-8"),
            headers={
                "Authorization":           f"Bearer {tokens['access_token']}",
                "Content-Type":            "application/json; charset=UTF-8",
                "X-Upload-Content-Length": str(file_size),
                "X-Upload-Content-Type":   "video/mp4"
            },
            method="POST"
        )
        with urllib.request.urlopen(req) as r:
            location = r.headers.get("Location")
        ok("Upload session OK")
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="ignore")
        return None, f"HTTP {e.code} khi tạo session: {body[:300]}"
    except Exception as e:
        return None, f"Lỗi tạo session: {e}"

    # Upload binary với progress bar
    step(f"Đang upload {size_mb:.1f} MB lên YouTube...")
    start_time = time.time()

    CHUNK = 8 * 1024 * 1024  # 8MB per chunk
    uploaded = 0

    try:
        with open(filepath, "rb") as f:
            while True:
                chunk_data = f.read(CHUNK)
                if not chunk_data:
                    break
                chunk_size  = len(chunk_data)
                content_range = f"bytes {uploaded}-{uploaded+chunk_size-1}/{file_size}"
                try:
                    chunk_req = urllib.request.Request(
                        location,
                        data=chunk_data,
                        headers={
                            "Content-Length": str(chunk_size),
                            "Content-Range":  content_range,
                            "Content-Type":   "video/mp4"
                        },
                        method="PUT"
                    )
                    with urllib.request.urlopen(chunk_req) as r:
                        uploaded += chunk_size
                        pct      = uploaded / file_size * 100
                        elapsed  = time.time() - start_time
                        speed    = uploaded / elapsed / 1024 / 1024 if elapsed > 0 else 0
                        bar_len  = 30
                        filled   = int(bar_len * pct / 100)
                        bar      = "█" * filled + "░" * (bar_len - filled)
                        print(f"\r  [{bar}] {pct:5.1f}% · {speed:.1f} MB/s", end="", flush=True)
                        # Lấy video ID từ response cuối
                        try:
                            body = r.read().decode("utf-8")
                            if body:
                                result   = json.loads(body)
                                video_id = result.get("id")
                                if video_id:
                                    print()  # newline sau progress bar
                                    return video_id, None
                        except: pass
                except urllib.error.HTTPError as e:
                    # 308 Resume Incomplete = chunk OK, tiếp tục
                    if e.code == 308:
                        uploaded += chunk_size
                        pct      = uploaded / file_size * 100
                        elapsed  = time.time() - start_time
                        speed    = uploaded / elapsed / 1024 / 1024 if elapsed > 0 else 0
                        bar_len  = 30
                        filled   = int(bar_len * pct / 100)
                        bar      = "█" * filled + "░" * (bar_len - filled)
                        print(f"\r  [{bar}] {pct:5.1f}% · {speed:.1f} MB/s", end="", flush=True)
                    else:
                        body = e.read().decode(errors="ignore")
                        print()
                        return None, f"HTTP {e.code} khi upload chunk: {body[:300]}"
        print()
        return None, "Upload hoàn tất nhưng không lấy được video ID"
    except Exception as e:
        print()
        return None, f"Lỗi upload: {e}"

# ── Ghi kết quả vào log ────────────────────────────────
def record_result(filepath, title, yt_id, yt_url, privacy, error=None):
    log  = load_log()
    ts   = datetime.now().isoformat()
    entry = {
        "uploaded_at": ts,
        "file_path":   str(filepath),
        "file_name":   Path(filepath).name,
        "title":       title,
        "privacy":     privacy,
        "status":      "uploaded" if yt_id else "failed",
        "youtube_video_id": yt_id,
        "youtube_url":      yt_url,
        "error":            error,
    }
    log.append(entry)
    save_log(log)

    # Cũng cập nhật manual_upload_log.json nếu file khớp
    main_log = load_main_log()
    for item in main_log:
        vf = item.get("video_file","") or ""
        vn = item.get("video_name","") or ""
        fp = str(filepath)
        fn = Path(filepath).name
        if fp in (vf, vn) or fn in (vf, vn) or vf.endswith(fn):
            if yt_id:
                item.update({
                    "status":           "uploaded",
                    "youtube_video_id": yt_id,
                    "youtube_url":      yt_url,
                    "uploaded_at":      ts,
                    "upload_count":     item.get("upload_count", 0) + 1,
                })
            break
    MAIN_LOG.write_text(json.dumps(main_log, ensure_ascii=False, indent=2), encoding="utf-8")

# ── Hiển thị lịch sử ──────────────────────────────────
def show_history():
    log = load_log()
    if not log:
        print(f"\n{YELLOW}Chưa có lịch sử upload nào từ terminal.{R}\n")
        return

    uploaded = [e for e in log if e.get("status") == "uploaded"]
    failed   = [e for e in log if e.get("status") == "failed"]

    print(f"\n{BOLD}{'='*70}{R}")
    print(f"  📋 LỊCH SỬ UPLOAD YOUTUBE — Terminal")
    print(f"{BOLD}{'='*70}{R}")
    print(f"  Tổng: {len(log)} lần · {GREEN}{len(uploaded)} thành công{R} · {RED}{len(failed)} thất bại{R}")
    print()

    for i, e in enumerate(reversed(log[-30:]), 1):  # Hiện 30 mục gần nhất
        st  = e.get("status","")
        ico = "✅" if st=="uploaded" else "❌"
        ts  = (e.get("uploaded_at","") or "")[:16].replace("T"," ")
        fn  = e.get("file_name","")
        tit = (e.get("title","") or "")[:50]
        ytid= e.get("youtube_video_id","") or ""
        print(f"  {ico} {GRAY}[{ts}]{R} {c(CYAN,fn[:35])}")
        print(f"       📝 {tit}")
        if ytid:
            print(f"       🔗 {c(GREEN, 'https://www.youtube.com/watch?v='+ytid)}")
        elif e.get("error"):
            print(f"       ❗ {c(RED, str(e['error'])[:80])}")
        print()

    print(f"{BOLD}{'='*70}{R}\n")
    print(f"  Log đầy đủ: {UPLOAD_LOG}\n")

# ── Auto-short: upload 1 video chưa upload ─────────────
def report_log(msg):
    """Ghi 1 dòng report vào upload_short_report.log"""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}\n"
    with open(REPORT_LOG, "a", encoding="utf-8") as f:
        f.write(line)
    print(line.rstrip())

def auto_short_upload():
    """
    Tự động upload 1 short video chưa upload từ output_manual/.
    Dùng cho crontab — mỗi lần chạy chỉ upload 1 video.
    Exit code:
      0 = đã upload thành công 1 video
      1 = không có video pending
      2 = lỗi (OAuth, upload fail, ...)
    """
    output_dir = BASE_DIR / "output_manual"
    if not output_dir.exists():
        report_log("ERROR: Thư mục output_manual/ không tồn tại.")
        sys.exit(2)

    # Lấy tất cả file video có dung lượng hợp lệ (> 1KB)
    all_videos = sorted([
        f for f in output_dir.iterdir()
        if f.suffix.lower() in VIDEO_EXTS and not f.name.startswith(".")
        and f.stat().st_size > 1024
    ])

    if not all_videos:
        report_log("No pending short videos — thư mục output_manual/ trống.")
        sys.exit(1)

    # Lọc ra video chưa upload
    uploaded = get_uploaded_files()
    pending = [
        f for f in all_videos
        if str(f) not in uploaded
        and f.name not in uploaded
        and str(f.resolve()) not in uploaded
    ]

    if not pending:
        report_log(f"No pending short videos — tất cả {len(all_videos)} video đã upload.")
        sys.exit(1)

    # Chọn video cũ nhất (đầu danh sách đã sort)
    target = pending[0]
    title = title_from_filename(target)
    desc = title
    tags = ["Thảo Dương TV", "1995lido", "Shorts"]

    report_log(f"STARTING: {target.name} ({target.stat().st_size / 1024 / 1024:.1f} MB)")
    info(f"Pending: {len(pending)} video · Đang upload: {target.name}")

    # Lấy token
    try:
        tokens = get_tokens()
        if not tokens:
            report_log(f"ERROR: OAuth token không hợp lệ — chạy: python3 setup_token_direct.py")
            sys.exit(2)
    except Exception as e:
        report_log(f"ERROR: Lỗi OAuth: {e}")
        sys.exit(2)

    # Upload
    try:
        yt_id, error = upload_one(
            filepath=str(target),
            title=title,
            description=desc,
            tags=tags,
            privacy="public",
            tokens=tokens
        )
    except Exception as e:
        report_log(f"ERROR: Exception khi upload {target.name}: {e}")
        record_result(target, title, None, None, "public", error=str(e))
        sys.exit(2)

    if yt_id:
        yt_url = f"https://www.youtube.com/watch?v={yt_id}"
        record_result(target, title, yt_id, yt_url, "public")
        report_log(f"FILE: {target.name} → YT ID: {yt_id} (status: uploaded)")
        report_log(f"URL: {yt_url}")
        remaining = len(pending) - 1
        report_log(f"DONE: Còn {remaining} video chờ upload.")
        sys.exit(0)
    else:
        record_result(target, title, None, None, "public", error=error)
        report_log(f"FAILED: {target.name} → Error: {error}")
        sys.exit(2)

# ── Main ────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        prog="python3 yt_upload.py",
        description=f"{BOLD}🎬 Upload video lên YouTube — @1995lido{R}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
{BOLD}Ví dụ:{R}
  python3 yt_upload.py video.mp4
  python3 yt_upload.py video1.mp4 video2.mp4 video3.mp4
  python3 yt_upload.py --folder output_manual/
  python3 yt_upload.py --folder output_manual/ --skip-uploaded
  python3 yt_upload.py video.mp4 --title "Tiêu đề tùy chỉnh"
  python3 yt_upload.py video.mp4 --privacy unlisted
  python3 yt_upload.py --history
        """
    )

    parser.add_argument("files",     nargs="*",             help="Đường dẫn tới 1 hoặc nhiều file video")
    parser.add_argument("--folder",  type=str,              help="Upload tất cả video trong folder này")
    parser.add_argument("--title",   type=str, default="",  help="Tiêu đề tùy chỉnh (chỉ dùng khi upload 1 file)")
    parser.add_argument("--prefix",  type=str, default="",  help="Prefix thêm vào tiêu đề (VD: 'Thảo Dương TV:')")
    parser.add_argument("--desc",    type=str, default="",  help="Mô tả video")
    parser.add_argument("--tags",    type=str, default="",  help="Tags, cách nhau bởi dấu phẩy")
    parser.add_argument("--privacy", type=str, default="public",
                        choices=["public","unlisted","private"],
                        help="Privacy (mặc định: public)")
    parser.add_argument("--skip-uploaded", action="store_true", help="Bỏ qua file đã upload rồi")
    parser.add_argument("--history",       action="store_true", help="Xem lịch sử upload")
    parser.add_argument("--dry-run",       action="store_true", help="Chỉ liệt kê file, không upload thật")
    parser.add_argument("--auto-short",    action="store_true",
                        help="Tự động upload 1 file từ output_manual/ (chạy ngầm cron)")
    parser.add_argument("--auto-confirm",  action="store_true",
                        help="Bỏ qua bước hỏi Enter xác nhận")

    args = parser.parse_args()

    # Banner
    print(f"\n{PURPLE}{BOLD}╔══════════════════════════════════════════════════════════╗{R}")
    print(f"{PURPLE}{BOLD}║  🎬 YouTube Terminal Uploader — @1995lido                ║{R}")
    print(f"{PURPLE}{BOLD}╚══════════════════════════════════════════════════════════╝{R}\n")

    if args.history:
        show_history()
        return

    # ── Auto-short mode: upload 1 video chưa upload từ output_manual/ ──
    if args.auto_short:
        auto_short_upload()
        return

    # Thu thập danh sách file
    files_to_upload = []

    if args.folder:
        folder = Path(args.folder)
        if not folder.exists():
            err(f"Folder không tồn tại: {folder}")
            sys.exit(1)
        for f in sorted(folder.iterdir()):
            if f.suffix.lower() in VIDEO_EXTS and not f.name.startswith("."):
                files_to_upload.append(f)
        if not files_to_upload:
            warn(f"Không tìm thấy file video nào trong: {folder}")
            sys.exit(0)

    for fp in args.files:
        p = Path(fp)
        if not p.exists():
            err(f"File không tồn tại: {fp}")
        elif p.suffix.lower() not in VIDEO_EXTS:
            warn(f"Bỏ qua (không phải video): {fp}")
        else:
            files_to_upload.append(p)

    if not files_to_upload:
        err("Không có file nào để upload!")
        print()
        parser.print_help()
        sys.exit(1)

    # Tags
    default_tags = ["Thảo Dương TV", "1995lido", "Shorts"]
    if args.tags:
        extra_tags = [t.strip() for t in args.tags.split(",") if t.strip()]
        tags = list(set(default_tags + extra_tags))
    else:
        tags = default_tags

    # Bỏ qua file đã upload
    uploaded_files = get_uploaded_files() if args.skip_uploaded else set()

    # Lọc
    final_files = []
    skipped     = []
    for f in files_to_upload:
        fp_str = str(f)
        fn_str = f.name
        if args.skip_uploaded and (fp_str in uploaded_files or fn_str in uploaded_files):
            skipped.append(f)
        else:
            final_files.append(f)

    # Preview danh sách
    print(f"{BOLD}📋 Danh sách file sẽ upload:{R}")
    for i, f in enumerate(final_files, 1):
        sz = f.stat().st_size / 1024 / 1024
        t  = (args.title if len(final_files)==1 and args.title
              else title_from_filename(f, args.prefix))
        print(f"  {i:2d}. {c(CYAN, f.name):<45} {c(YELLOW, f'{sz:.1f}MB')}")
        print(f"      📝 {c(GRAY, t[:65])}")

    if skipped:
        print(f"\n{YELLOW}  Bỏ qua {len(skipped)} file đã upload:{R}")
        for f in skipped:
            print(f"  {GRAY}  ↷ {f.name}{R}")

    print(f"\n  Tổng: {BOLD}{len(final_files)} file{R} · Privacy: {c(PURPLE, args.privacy)}")

    if args.dry_run:
        print(f"\n{YELLOW}[DRY RUN] Không upload thật — chỉ xem danh sách.{R}\n")
        return

    if not final_files:
        warn("Không có file nào cần upload.")
        return

    # Xác nhận
    print()
    if not args.auto_confirm:
        try:
            confirm = input(f"  {BOLD}Nhấn Enter để upload, hoặc Ctrl+C để hủy...{R}")
        except KeyboardInterrupt:
            print(f"\n{YELLOW}Đã hủy.{R}\n")
            return
        except EOFError:
            pass

    # Lấy token
    tokens = get_tokens()
    if not tokens:
        sys.exit(1)
    ok("Xác thực YouTube OAuth OK")

    # Upload từng file
    success = 0
    failed  = 0
    results = []

    total = len(final_files)
    for idx, filepath in enumerate(final_files, 1):
        print(f"\n{BOLD}[{idx}/{total}]{R} Đang xử lý...")

        # Sinh tiêu đề
        if len(final_files) == 1 and args.title:
            title = args.title
        else:
            title = title_from_filename(filepath, args.prefix)

        desc = args.desc or title

        yt_id, error = upload_one(
            filepath=str(filepath),
            title=title,
            description=desc,
            tags=tags,
            privacy=args.privacy,
            tokens=tokens
        )

        if yt_id:
            yt_url = f"https://www.youtube.com/watch?v={yt_id}"
            ok(f"Upload thành công!")
            print(f"  🎬 Video ID : {c(GREEN, yt_id)}")
            print(f"  🔗 URL      : {c(GREEN, yt_url)}")
            record_result(filepath, title, yt_id, yt_url, args.privacy)
            results.append({"file": filepath.name, "status": "ok", "yt_id": yt_id, "url": yt_url})
            success += 1
        else:
            err(f"Upload thất bại: {error or 'Lỗi không xác định'}")
            record_result(filepath, title, None, None, args.privacy, error=error)
            results.append({"file": filepath.name, "status": "fail", "error": error})
            failed += 1

        # Refresh token sau mỗi file để tránh hết hạn
        if idx < total:
            tokens = refresh_token(tokens) or tokens
            time.sleep(2)  # Nghỉ 2 giây giữa các file

    # Tổng kết
    print(f"\n{BOLD}{'='*60}{R}")
    print(f"  📊 KẾT QUẢ UPLOAD")
    print(f"{'='*60}{R}")
    for r in results:
        if r["status"] == "ok":
            print(f"  {GREEN}✅{R} {r['file'][:40]}")
            print(f"     🔗 {c(GREEN, r['url'])}")
        else:
            print(f"  {RED}❌{R} {r['file'][:40]}")
            print(f"     ❗ {c(RED, (r.get('error','') or '')[:70])}")
    print()
    print(f"  Tổng: {BOLD}{total} file{R} · {c(GREEN, f'{success} thành công')} · {c(RED, f'{failed} thất bại')}")
    print(f"  Log : {UPLOAD_LOG}")
    print(f"{BOLD}{'='*60}{R}\n")

    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
