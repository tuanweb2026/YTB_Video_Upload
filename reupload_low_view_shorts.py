import os
import json
import time
import subprocess
import urllib.request
from pathlib import Path
from yt_upload import get_tokens

BASE_DIR = Path(__file__).parent
MANUAL_DB = BASE_DIR / "manual_upload_log.json"
TERMINAL_DB = BASE_DIR / "yt_terminal_upload_log.json"

def get_all_uploaded_shorts():
    files = {}
    if MANUAL_DB.exists():
        with open(MANUAL_DB) as f:
            try:
                for entry in json.load(f):
                    if entry.get("youtube_video_id"): files[entry["youtube_video_id"]] = entry
                    elif entry.get("video_id"): files[entry["video_id"]] = entry
            except: pass
            
    if TERMINAL_DB.exists():
        with open(TERMINAL_DB) as f:
            try:
                for entry in json.load(f):
                    if entry.get("youtube_video_id"): files[entry["youtube_video_id"]] = entry
                    elif entry.get("video_id"): files[entry["video_id"]] = entry
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
                    views = int(item["statistics"].get("viewCount", 0))
                    views_map[item["id"]] = views
        except Exception as e:
            print(f"⚠️ Lỗi fetch views: {e}")
            
    return views_map

def main():
    print("🔍 Đang phân tích các short video đã đăng để tìm video < 200 views...")
    tokens = get_tokens()
    if not tokens or "access_token" not in tokens:
        print("❌ Lỗi lấy access_token! Vui lòng kiểm tra lại token.json")
        return

    uploaded_files = get_all_uploaded_shorts()
    video_ids = list(uploaded_files.keys())
    
    if not video_ids:
        print("❌ Chưa có video nào được đăng.")
        return
        
    print(f"📊 Tìm thấy {len(video_ids)} video trong lịch sử.")
    views_map = get_video_views(tokens["access_token"], video_ids)
    
    low_view_videos = []
    for vid, views in views_map.items():
        if views < 200:
            low_view_videos.append(uploaded_files[vid])
            
    print(f"⚠️ Có {len(low_view_videos)} video dưới 200 views cần re-upload.")
    
    for i, video in enumerate(low_view_videos):
        local_file = video.get("local_file") or video.get("file_path") or video.get("video_file")
        if not local_file or not os.path.exists(local_file):
            print(f"  ❌ Không tìm thấy file gốc cho video ID: {video.get('youtube_video_id', video.get('video_id'))}")
            continue
            
        print(f"\n🔄 [{i+1}/{len(low_view_videos)}] Đang chuẩn bị re-upload: {local_file}")
        
        with open(local_file, "ab") as f:
            f.write(b"\x00")
            
        title = video.get("title", "YouTube Short")
        if not "#Shorts" in title:
            title += " #Shorts"
            
        cmd = [
            "python3", "yt_upload.py",
            "--auto-confirm",
            "--title", title,
            local_file
        ]
        
        print(f"🚀 Bắt đầu upload...")
        r = subprocess.run(cmd, input=b"\n")
        if r.returncode == 0:
            print(f"✅ Re-upload thành công!")
        else:
            print(f"❌ Re-upload thất bại!")
            
        if i < len(low_view_videos) - 1:
            print("⏳ Chờ 15 phút (900s) trước khi upload video tiếp theo để an toàn kênh...")
            time.sleep(900)
            
    print("\n🎉 HOÀN THÀNH QUÁ TRÌNH RE-UPLOAD!")

if __name__ == "__main__":
    main()
