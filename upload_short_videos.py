#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================
  upload_short_videos.py — Wrapper tự động upload short video
  @1995lido · Kênh Thảo Dương TV

  Script này được gọi bởi crontab mỗi giờ.
  Nó gọi yt_upload.py --auto-short để upload 1 video chưa upload
  từ output_manual/ lên YouTube (mục Shorts).

  Cách dùng thủ công:
    python3 upload_short_videos.py

  Crontab (mỗi giờ):
    0 * * * * /path/to/upload_short_videos.py

  Log: upload_short_report.log
=================================================================
"""

import subprocess
import os
import sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
YT_UPLOAD  = os.path.join(SCRIPT_DIR, "yt_upload.py")
REPORT_LOG = os.path.join(SCRIPT_DIR, "upload_short_report.log")

def main():
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Ghi header
    with open(REPORT_LOG, "a", encoding="utf-8") as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"[{ts}] === AUTO-SHORT UPLOAD START ===\n")

    # Chạy yt_upload.py --auto-short
    python_cmd = sys.executable or "python3"
    cmd = [python_cmd, YT_UPLOAD, "--auto-short"]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=SCRIPT_DIR,
            timeout=300  # Timeout 5 phút
        )

        # Ghi stdout vào report
        if result.stdout:
            with open(REPORT_LOG, "a", encoding="utf-8") as f:
                f.write(result.stdout)
            print(result.stdout, end="")

        # Ghi stderr nếu có lỗi
        if result.stderr:
            with open(REPORT_LOG, "a", encoding="utf-8") as f:
                f.write(f"[STDERR] {result.stderr}\n")
            sys.stderr.write(result.stderr)

        # Ghi footer
        ts_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        exit_msg = "OK" if result.returncode == 0 else f"EXIT CODE: {result.returncode}"
        with open(REPORT_LOG, "a", encoding="utf-8") as f:
            f.write(f"[{ts_end}] === AUTO-SHORT UPLOAD END ({exit_msg}) ===\n")

        sys.exit(result.returncode)

    except subprocess.TimeoutExpired:
        ts_err = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = f"[{ts_err}] ERROR: Upload timeout (>5 phút). Kiểm tra mạng hoặc token.\n"
        with open(REPORT_LOG, "a", encoding="utf-8") as f:
            f.write(msg)
        print(msg, end="")
        sys.exit(2)

    except Exception as e:
        ts_err = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = f"[{ts_err}] ERROR: {e}\n"
        with open(REPORT_LOG, "a", encoding="utf-8") as f:
            f.write(msg)
        print(msg, end="")
        sys.exit(2)


if __name__ == "__main__":
    main()
