#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cập nhật ghi chú Like/Subscribe và Hashtag cho toàn bộ video dài trên kênh @1995lido
"""

import urllib.request
import urllib.parse
import json
import time
import re
import ssl
from pathlib import Path

# Fix SSL certificate verification on macOS Python
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

TOKEN_FILE = Path("/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management/token.json")
PROGRESS_FILE = Path("/Users/abc/.gemini/antigravity/scratch/update_long_videos_progress.json")
AUDIT_FILE = Path("/Users/abc/.gemini/antigravity/scratch/long_videos_audit.json")

CTA_TEXT = """
──────────────────────────────────────────────────
✨ Nếu bạn cảm thấy yêu thích giai điệu này, xin vui lòng nhấn LIKE và ĐĂNG KÝ KÊNH Thảo Dương TV để ủng hộ và đón nghe những bản nhạc mới nhất nhé. Xin chân thành cảm ơn!

👉 Đăng ký kênh: https://www.youtube.com/@1995lido
"""

HASHTAGS_DEFAULT = "#ThaoDuongTV #AmNhacThuGian #NhacThien #NhacChill #GiaiDieuChuaLanh #Subscribe"

def get_access_token():
    with open(TOKEN_FILE, "r", encoding="utf-8") as f:
        tokens = json.load(f)
    
    # Check or refresh token
    data = urllib.parse.urlencode({
        "client_id": tokens["client_id"],
        "client_secret": tokens["client_secret"],
        "refresh_token": tokens["refresh_token"],
        "grant_type": "refresh_token"
    }).encode("utf-8")
    req = urllib.request.Request(tokens.get("token_uri", "https://oauth2.googleapis.com/token"), data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    try:
        with urllib.request.urlopen(req, context=ssl_context) as r:
            res = json.loads(r.read().decode())
            tokens["access_token"] = res["access_token"]
            with open(TOKEN_FILE, "w", encoding="utf-8") as f_out:
                json.dump(tokens, f_out, indent=2)
            return tokens["access_token"]
    except Exception as e:
        print("Refresh token error, using existing access_token:", e)
        return tokens.get("access_token")

def update_videos():
    with open(AUDIT_FILE, "r", encoding="utf-8") as f:
        audit_data = json.load(f)

    videos = audit_data.get("need_update", [])
    total = len(videos)
    print(f"🚀 Bắt đầu cập nhật {total} video dài...")

    prog = {}
    if PROGRESS_FILE.exists():
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                prog = json.load(f)
        except Exception: pass

    token = get_access_token()

    updated_count = 0
    for idx, v in enumerate(videos, 1):
        vid = v["id"]
        title = v["title"]
        if vid in prog and prog[vid].get("status") == "updated":
            print(f"[{idx}/{total}] Đã có trước đó: {title}")
            continue

        print(f"[{idx}/{total}] Đang cập nhật: {title[:40]}... ({vid})")

        # 1. Lấy snippet hiện tại
        url_get = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id={vid}"
        req_get = urllib.request.Request(url_get, headers={"Authorization": "Bearer " + token})
        try:
            with urllib.request.urlopen(req_get, context=ssl_context) as r:
                item_data = json.loads(r.read().decode())["items"][0]
        except Exception as e:
            print(f"❌ Lỗi lấy thông tin video {vid}: {e}")
            continue

        snippet = item_data["snippet"]
        old_desc = snippet.get("description", "").strip()

        # Thêm CTA và Hashtag vào cuối
        new_desc = old_desc + "\n" + CTA_TEXT.strip() + "\n\n" + HASHTAGS_DEFAULT

        # Body update
        body = {
            "id": vid,
            "snippet": {
                "title": snippet["title"],
                "description": new_desc,
                "categoryId": snippet.get("categoryId", "10")
            }
        }
        if "tags" in snippet:
            body["snippet"]["tags"] = snippet["tags"]

        # 2. Gửi request PUT
        url_update = "https://www.googleapis.com/youtube/v3/videos?part=snippet"
        req_update = urllib.request.Request(
            url_update,
            data=json.dumps(body).encode("utf-8"),
            headers={
                "Authorization": "Bearer " + token,
                "Content-Type": "application/json"
            },
            method="PUT"
        )
        try:
            with urllib.request.urlopen(req_update, context=ssl_context) as r:
                print(f"   ✅ OK ({vid})")
                prog[vid] = {
                    "id": vid,
                    "title": title,
                    "status": "updated",
                    "time": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                updated_count += 1
                with open(PROGRESS_FILE, "w", encoding="utf-8") as f_out:
                    json.dump(prog, f_out, ensure_ascii=False, indent=2)
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode(errors="ignore")
            print(f"   ❌ HTTP {e.code}: {err_msg[:200]}")
            if e.code == 401:
                token = get_access_token()
        except Exception as e:
            print(f"   ❌ Lỗi: {e}")

        time.sleep(0.3)

    print(f"\n🎉 HOÀN TẤT CẬP NHẬT TOÀN BỘ {total} VIDEO DÀI! (Mới cập nhật: {updated_count})")

if __name__ == "__main__":
    update_videos()
