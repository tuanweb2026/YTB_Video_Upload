import urllib.request, json, re

TOKEN_FILE = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management/token.json"
with open(TOKEN_FILE) as f:
    tokens = json.load(f)

playlist_id = "UU-0dKn2s-7jpsz6H3XFKgow"
all_items = []
page_token = ""

while True:
    url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails&playlistId={playlist_id}&maxResults=50"
    if page_token:
        url += f"&pageToken={page_token}"
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + tokens["access_token"]})
    try:
        with urllib.request.urlopen(req) as r:
            data = json.loads(r.read().decode())
            all_items.extend(data.get("items", []))
            page_token = data.get("nextPageToken")
            if not page_token:
                break
    except Exception as e:
        print("Error fetching playlist items:", e)
        break

print(f"Tổng số video trên kênh: {len(all_items)}")

video_ids = [item["contentDetails"]["videoId"] for item in all_items]

def parse_iso_duration(dur):
    # e.g. PT1H2M3S, PT45S, PT3M12S
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', dur)
    if not match: return 0
    h, m, s = match.groups()
    total = int(h or 0)*3600 + int(m or 0)*60 + int(s or 0)
    return total

long_videos = []
for i in range(0, len(video_ids), 50):
    batch = video_ids[i:i+50]
    ids_param = ",".join(batch)
    url_v = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&id={ids_param}"
    req_v = urllib.request.Request(url_v, headers={"Authorization": "Bearer " + tokens["access_token"]})
    with urllib.request.urlopen(req_v) as r:
        data_v = json.loads(r.read().decode())
        for v in data_v.get("items", []):
            dur_sec = parse_iso_duration(v["contentDetails"]["duration"])
            # Video dài (thường > 60s hoặc > 120s)
            if dur_sec > 60:
                long_videos.append({
                    "id": v["id"],
                    "title": v["snippet"]["title"],
                    "description": v["snippet"]["description"],
                    "duration_sec": dur_sec,
                    "tags": v["snippet"].get("tags", [])
                })

print(f"Số lượng video dài (> 60s): {len(long_videos)}")

# Kiểm tra ghi chú và hashtag
need_update = []
has_note = []

keywords = ["thích", "like", "đăng ký", "đăng kí", "cảm ơn", "xin cảm ơn"]

for idx, v in enumerate(long_videos, 1):
    desc = v["description"].lower()
    # Check if has CTA
    found_like = any(k in desc for k in ["like", "thích"])
    found_sub = any(k in desc for k in ["đăng ký", "đăng kí", "subscribe"])
    found_thanks = any(k in desc for k in ["cảm ơn", "xin cảm ơn", "thank"])
    
    # Check hashtags
    hashtags = re.findall(r'#\w+', v["description"])

    has_cta = found_like and found_sub
    has_tag = len(hashtags) > 0

    status = {
        "id": v["id"],
        "title": v["title"],
        "duration_sec": v["duration_sec"],
        "has_cta": has_cta,
        "has_hashtags": has_tag,
        "hashtag_count": len(hashtags),
        "existing_hashtags": hashtags,
        "current_desc": v["description"]
    }
    if not has_cta or not has_tag:
        need_update.append(status)
    else:
        has_note.append(status)

print("\n--- KẾT QUẢ KIỂM TRA VIDEO DÀI ---")
print(f"Tổng số video dài: {len(long_videos)}")
print(f"Video ĐÃ CÓ đủ lời kêu gọi Like/Đăng ký & Hashtag: {len(has_note)}")
print(f"Video CHƯA ĐỦ lời kêu gọi Like/Đăng ký hoặc thiếu Hashtag: {len(need_update)}")

with open("/Users/abc/.gemini/antigravity/scratch/long_videos_audit.json", "w", encoding="utf-8") as f:
    json.dump({
        "total_long_videos": len(long_videos),
        "need_update_count": len(need_update),
        "need_update": need_update,
        "has_note": has_note
    }, f, ensure_ascii=False, indent=2)

