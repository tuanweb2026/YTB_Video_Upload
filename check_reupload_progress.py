import os
import json
import urllib.request
from datetime import datetime
from yt_upload import get_tokens
from pathlib import Path

BASE_DIR = Path(__file__).parent
MANUAL_DB = BASE_DIR / "manual_upload_log.json"
TERMINAL_DB = BASE_DIR / "yt_terminal_upload_log.json"

def get_all_uploaded_shorts():
    files = {}
    for db in [MANUAL_DB, TERMINAL_DB]:
        if db.exists():
            with open(db) as f:
                try:
                    for entry in json.load(f):
                        vid = entry.get("youtube_video_id") or entry.get("video_id")
                        if vid: files[vid] = entry
                except: pass
    return files

def get_video_views(access_token, video_ids):
    views_map = {}
    ids_list = list(video_ids)
    for i in range(0, len(ids_list), 50):
        batch = ids_list[i:i+50]
        url = f"https://www.googleapis.com/youtube/v3/videos?part=statistics&id={','.join(batch)}"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {access_token}"})
        try:
            with urllib.request.urlopen(req) as r:
                res = json.loads(r.read().decode())
                for item in res.get("items", []):
                    views_map[item["id"]] = int(item["statistics"].get("viewCount", 0))
        except: pass
    return views_map

def main():
    print("\n" + "="*60)
    print("📊 BÁO CÁO TIẾN ĐỘ RE-UPLOAD VIDEO DƯỚI 200 VIEWS")
    print("="*60)
    
    tokens = get_tokens()
    if not tokens:
        print("❌ Lỗi token.")
        return
        
    all_videos = get_all_uploaded_shorts()
    if not all_videos:
        print("Chưa có dữ liệu video.")
        return
        
    views_map = get_video_views(tokens["access_token"], all_videos.keys())
    
    low_view_count = sum(1 for v in views_map.values() if v < 200)
    
    # Check how many reuploaded today
    reuploaded_today = 0
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    if TERMINAL_DB.exists():
        with open(TERMINAL_DB) as f:
            try:
                log_data = json.load(f)
                for entry in log_data:
                    # yt_upload saves 'uploaded_at': '2026-08-27T14:31:00...'
                    uploaded_at = entry.get("uploaded_at", "")
                    if uploaded_at.startswith(today_str):
                        reuploaded_today += 1
            except: pass

    print(f"🔹 Tổng số video đã kiểm tra: {len(all_videos)}")
    print(f"🔹 Số video CÒN LẠI dưới 200 views (cần re-upload): {low_view_count}")
    print(f"🔹 Số video ĐÃ RE-UPLOAD thành công trong hôm nay: {reuploaded_today}")
    
    if low_view_count > 0:
        print(f"\n⏳ Tiến trình chạy ngầm vẫn đang tiếp tục xử lý {low_view_count} video còn lại.")
        print(f"   (Khoảng 15 phút 1 video)")
    else:
        print(f"\n🎉 Chúc mừng! Đã không còn video nào dưới 200 views trên kênh.")
        
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
