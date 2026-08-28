#!/usr/bin/env python3
"""
Comprehensive Multi-Channel Dashboard Server for YouTube Management
Listens on http://localhost:8099
- Kênh 1: @1995lido (Thảo Dương TV - Triết Lý Nikaya & Tâm Lý)
- Kênh 2: @ThaoDuongAnimation (Thảo Dương Animation - Hoạt Hình & Hài Hước)
- Provides HTML5 Video Player Previews for all upcoming Channel 1 slot videos.
- Provides native macOS Finder folder opener buttons to open local directories directly.
"""

import os
import sys
import json
import ssl
import subprocess
import urllib.parse
from datetime import datetime, timedelta
from http.server import HTTPServer, SimpleHTTPRequestHandler
from content_generator import get_slot_content

ssl._create_default_https_context = ssl._create_unverified_context

PORT = 8099
SCRATCH_DIR = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management"
DB_FILE = f"{SCRATCH_DIR}/published_db.json"
ANIMATION_DB = f"{SCRATCH_DIR}/animation_posts.json"
PUBLISHED_ANIMATION_DB = f"{SCRATCH_DIR}/published_animation_db.json"
OUTPUT_QUEUE = f"{SCRATCH_DIR}/output_queue"

class DashboardRequestHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        parsed_path = urllib.parse.urlparse(path).path
        if parsed_path.startswith("/videos/"):
            rel = parsed_path.replace("/videos/", "")
            return os.path.join(OUTPUT_QUEUE, rel)
        return super().translate_path(path)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/" or parsed.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            html_content = generate_dashboard_html()
            self.wfile.write(html_content.encode("utf-8"))
            return
        elif parsed.path == "/api/open_folder":
            query_params = urllib.parse.parse_qs(parsed.query)
            folder_target = query_params.get("target", ["scratch"])[0]
            
            target_path = SCRATCH_DIR
            if folder_target == "output_queue":
                target_path = OUTPUT_QUEUE
            elif folder_target == "launchd":
                target_path = os.path.expanduser("~/Library/LaunchAgents")
            elif folder_target == "nikaya_pdf":
                target_path = "/Users/abc/Documents/Kenh_youtube/Nikaya_kinh"
                
            try:
                subprocess.run(["open", target_path], check=True)
                resp = {"status": "success", "message": f"Opened {target_path} in macOS Finder"}
            except Exception as e:
                resp = {"status": "error", "message": str(e)}
                
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(resp).encode("utf-8"))
            return
            
        elif parsed.path == "/api/log":
            query_params = urllib.parse.parse_qs(parsed.query)
            log_type = query_params.get("type", [""])[0]
            
            log_file = None
            if log_type == "short":
                log_file = os.path.join(SCRATCH_DIR, "upload_short_report.log")
            elif log_type == "daemon":
                log_file = os.path.join(SCRATCH_DIR, "daemon.log")
                
            content = "Log file not found."
            if log_file and os.path.exists(log_file):
                try:
                    # Đọc 200 dòng cuối để tránh file quá to
                    with open(log_file, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                        content = "".join(lines[-200:])
                except Exception as e:
                    content = f"Error reading log: {e}"
            
            self.send_response(200)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(content.encode("utf-8"))
            return
            
        return super().do_GET()

def load_animation_posts():
    if os.path.exists(ANIMATION_DB):
        try:
            with open(ANIMATION_DB, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return []

def load_published_animation():
    if os.path.exists(PUBLISHED_ANIMATION_DB):
        try:
            with open(PUBLISHED_ANIMATION_DB, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return []

def generate_dashboard_html():
    published_list = []
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    published_list = data
                elif isinstance(data, dict):
                    published_list = data.get("published", data.get("published_videos", []))
        except Exception:
            pass
            
    animation_list = load_animation_posts()
    published_animation = load_published_animation()

    # Generate Channel 1 Published List
    published_cards_html = ""
    for v in published_list:
        pub_url = v.get("youtube_url", "#")
        v_id = v.get("video_id", "N/A")
        c_date = v.get('calendar_date', datetime.now().strftime("%d/%m/%Y"))
        title = v.get("title", "Video Live YouTube")
        cat = v.get("category", "YouTube Shorts")
        idx = v.get("post_index", "")
        
        published_cards_html += f"""
        <div class="card-box">
            <div class="card-header-bar">
                <div>
                    <span class="badge bg-success">🔴 BÀI #{idx} LIVE ON YOUTUBE</span>
                    <strong style="margin-left: 10px;">{c_date}</strong>
                    <span class="slot-tag" style="margin-left: 8px;">{cat}</span>
                </div>
                <div>
                    <a href="{pub_url}" target="_blank" class="btn btn-sm btn-primary">🔗 Xem Video LIVE (ID: {v_id})</a>
                </div>
            </div>
            <div class="card-body-content">
                <h3 class="post-title">{title}</h3>
                <p class="file-path">📁 File Local: <code>{v.get('local_file', '')}</code></p>
                <div class="meta-row">
                    <span class="meta-tag">Trạng thái: <strong>{v.get('status', 'LIVE_SUCCESS')}</strong></span>
                    <span class="meta-tag">Thời gian: <strong>{v.get('published_at', '')[:19]}</strong></span>
                </div>
            </div>
        </div>
        """

    # Generate Channel 1 Upcoming Previews dynamically for tomorrow
    start_date = datetime(2026, 8, 22)
    tomorrow_dt = datetime.now() + timedelta(days=1)
    day = (tomorrow_dt - start_date).days + 1
    tomorrow_str = tomorrow_dt.strftime("%d/%m/%Y")
    
    upcoming_ch1_html = ""
    slots_list = [
        ("slot_08am", "🌅 08:00 AM (Tư Duy Deep Work & Kỷ Luật Sáng)"),
        ("slot_11am", "🌿 11:00 AM (Giải Tỏa Lo Âu & Sơ Cứu Tâm Lý Trưa)"),
        ("slot_18pm", "🌙 18:00 PM (Triết Lý Kinh Nikaya Đêm - Bài 1/3)"),
        ("slot_20pm", "🌙 20:00 PM (Triết Lý Kinh Nikaya Đêm - Bài 2/3)"),
        ("slot_2130pm", "💤 21:30 PM (Triết Lý Kinh Nikaya Đêm - Bài 3/3 - Thiền 432Hz)")
    ]
    
    for slot_key, slot_name in slots_list:
        filename = f"shorts_day_{day}_{slot_key}.mp4"
        video_rel_path = f"/videos/{filename}"
        local_mp4_full = os.path.join(OUTPUT_QUEUE, filename)
        has_local_video = os.path.exists(local_mp4_full)
        
        content = get_slot_content(day=day, slot_key=slot_key)
        
        player_html = ""
        if has_local_video:
            player_html = f"""
            <div class="mt-3 mb-3 p-2 bg-light rounded text-center">
                <p class="mb-1 text-muted" style="font-size: 0.85rem;">🎬 XEM TRƯỚC LOCAL VIDEO (HTML5):</p>
                <video controls width="280" height="480" preload="metadata" style="border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
                    <source src="{video_rel_path}" type="video/mp4">
                    Trình duyệt không hỗ trợ xem video MP4 HTML5.
                </video>
            </div>
            """
        else:
            player_html = """
            <div class="alert alert-warning mt-2 mb-2 p-2">
                ⏳ Video đang được dựng ngầm, vui lòng tải lại trang sau ít phút...
            </div>
            """
            
        upcoming_ch1_html += f"""
        <div class="card-box" style="border-left: 5px solid #3b82f6;">
            <div class="card-header-bar">
                <div>
                    <span class="badge bg-primary">⏳ CHUẨN BỊ ĐĂNG</span>
                    <span class="slot-tag" style="margin-left: 8px;">{slot_name}</span>
                </div>
                <div>
                    <span class="badge bg-secondary">Ngày mai {tomorrow_str}</span>
                </div>
            </div>
            <div class="card-body-content">
                <h3 class="post-title">{content['title']}</h3>
                <p style="color: #4b5563; font-style: italic; font-size: 0.9rem;">🎙️ Kịch bản: "{content['script']}"</p>
                {player_html}
            </div>
        </div>
        """

    # Generate Channel 2 (Animation/Comedy)
    animation_cards_html = ""
    for item in animation_list:
        idx = item.get("post_index", 1)
        title = item.get("title", "")
        script = item.get("script", "")
        cat = item.get("category", "Hoạt Hình Triết Lý Chiều Sâu")
        
        filename = f"animation_short_{idx}.mp4"
        video_rel_path = f"/videos/{filename}"
        local_mp4_full = os.path.join(OUTPUT_QUEUE, filename)
        has_local_video = os.path.exists(local_mp4_full)
        
        pub_info = None
        for p in published_animation:
            if p.get("post_index") == idx:
                pub_info = p
                break
                
        status_badge = '<span class="badge bg-warning">⏳ ĐANG DỰNG BÀI</span>'
        live_btn_html = ""
        
        if pub_info:
            v_id = pub_info.get("video_id", "")
            pub_url = pub_info.get("youtube_url", "#")
            if v_id and v_id not in ["QUEUED_SCHEDULED", "READY_TO_POST"]:
                status_badge = '<span class="badge bg-success">🔴 LIVE ON YOUTUBE</span>'
                live_btn_html = f'<a href="{pub_url}" target="_blank" class="btn btn-sm btn-danger">🔗 Xem Trên YouTube (ID: {v_id})</a>'
            else:
                status_badge = '<span class="badge bg-primary">⏰ ĐÃ LÊN LỊCH ĐĂNG (CÁCH 1 GIỜ/BÀI)</span>'

        player_html = ""
        if has_local_video:
            player_html = f"""
            <div class="mt-3 mb-3 p-2 bg-light rounded text-center">
                <p class="mb-1 text-muted" style="font-size: 0.85rem;">🎬 xem TRƯỚC LOCAL VIDEO (HTML5):</p>
                <video controls width="280" height="480" preload="metadata" style="border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
                    <source src="{video_rel_path}" type="video/mp4">
                </video>
            </div>
            """

        animation_cards_html += f"""
        <div class="card-box" style="border-left: 5px solid #ec4899;">
            <div class="card-header-bar">
                <div>
                    {status_badge}
                    <span class="slot-tag" style="margin-left: 8px;">BÀI HOẠT HÌNH #{idx}</span>
                </div>
                <div>
                    {live_btn_html}
                </div>
            </div>
            <div class="card-body-content">
                <h3 class="post-title">{title}</h3>
                <p style="color: #4b5563; font-style: italic; font-size: 0.9rem;">🎙️ Kịch bản: "{script}"</p>
                {player_html}
            </div>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Multi-Channel Control Dashboard - Thảo Dương Media</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{
            background-color: #f1f5f9;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            color: #1e293b;
        }}
        .navbar-custom {{
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            padding: 18px 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        .nav-tabs .nav-link.active {{
            font-weight: 700;
            border-bottom: 3px solid #3b82f6;
            color: #1e40af;
        }}
        .card-box {{
            background: #ffffff;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            border: 1px solid #e2e8f0;
        }}
        .card-header-bar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #f1f5f9;
            padding-bottom: 12px;
            margin-bottom: 12px;
        }}
        .post-title {{
            font-size: 1.1rem;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 8px;
        }}
        .slot-tag {{
            background: #e0f2fe;
            color: #0369a1;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }}
        .file-path {{
            font-size: 0.85rem;
            color: #64748b;
        }}
        .meta-row {{
            display: flex;
            gap: 15px;
            font-size: 0.85rem;
            color: #475569;
        }}
        .meta-tag {{
            background: #f8fafc;
            padding: 4px 10px;
            border-radius: 6px;
            border: 1px solid #e2e8f0;
        }}
        .btn-finder {{
            background: #e2e8f0;
            color: #1e293b;
            border: 1px solid #cbd5e1;
            font-weight: 600;
        }}
        .btn-finder:hover {{
            background: #cbd5e1;
        }}
        .section-title {{
            font-size: 1.4rem;
            font-weight: 700;
            color: #1e293b;
            margin-top: 30px;
            margin-bottom: 15px;
            border-bottom: 2px solid #cbd5e1;
            padding-bottom: 8px;
        }}
    </style>
</head>
<body>
    <nav class="navbar navbar-dark navbar-custom">
        <div class="container">
            <span class="navbar-brand mb-0 h1">🚀 HỆ THỐNG QUẢN LÝ ĐA KÊNH YOUTUBE AUTO-PILOT</span>
            <div>
                <button onclick="openFolder('scratch')" class="btn btn-sm btn-finder">📂 Mở Thư Mục Code Local</button>
                <button onclick="openFolder('nikaya_pdf')" class="btn btn-sm btn-finder">📄 File PDF Kinh Nikaya</button>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        <ul class="nav nav-tabs mb-4" id="channelTabs" role="tablist">
            <li class="nav-item" role="presentation">
                <button class="nav-link active" id="channel1-tab" data-bs-toggle="tab" data-bs-target="#channel1" type="button" role="tab">
                    🌸 KÊNH 1: @1995lido (Thảo Dương TV - Nikaya & Tâm Lý)
                </button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="channel2-tab" data-bs-toggle="tab" data-bs-target="#channel2" type="button" role="tab">
                    🤡 KÊNH 2: @ThaoDuongAnimation (Hoạt Hình & Hài Hước Triết Lý)
                </button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link text-danger" id="logs-tab" data-bs-toggle="tab" data-bs-target="#logs" type="button" role="tab">
                    ⚙️ HỆ THỐNG & LOGS
                </button>
            </li>
        </ul>

        <div class="tab-content" id="channelTabsContent">
            <!-- TAB CHANNEL 1 -->
            <div class="tab-pane fade show active" id="channel1" role="tabpanel">
                <div class="alert alert-info d-flex justify-content-between align-items-center">
                    <div>
                        <strong>Kênh 1: Thảo Dương TV (@1995lido)</strong> - Lịch phát sóng **5 bài/ngày** đã kích hoạt!
                    </div>
                    <a href="https://www.youtube.com/@1995lido" target="_blank" class="btn btn-sm btn-outline-primary">📺 Ghé thăm kênh @1995lido</a>
                </div>
                
                <h2 class="section-title">🎬 XEM TRƯỚC 5 VIDEO DỰ KIẾN PHÁT NGÀY MAI ({tomorrow_str})</h2>
                {upcoming_ch1_html}
                
                <h2 class="section-title">🔴 DANH SÁCH CÁC VIDEO ĐÃ XUẤT BẢN THÀNH CÔNG</h2>
                {published_cards_html}
            </div>

            <!-- TAB CHANNEL 2 -->
            <div class="tab-pane fade" id="channel2" role="tabpanel">
                <div class="alert alert-success d-flex justify-content-between align-items-center">
                    <div>
                        <strong>Kênh 2: Thảo Dương Animation (@ThaoDuongAnimation)</strong> - Hoạt Hình & Triết Lý Chiều Sâu!
                    </div>
                    <a href="https://www.youtube.com/@ThaoDuongAnimation" target="_blank" class="btn btn-sm btn-outline-success">📺 Ghé thăm kênh @ThaoDuongAnimation</a>
                </div>
                {animation_cards_html}
            </div>
            
            <!-- TAB LOGS -->
            <div class="tab-pane fade" id="logs" role="tabpanel">
                <div class="alert alert-warning">
                    <strong>Tình trạng hệ thống:</strong> macOS thường chặn Crontab mặc định. Nếu auto-short upload không chạy, hãy dùng terminal để chạy thủ công.
                </div>
                
                <div class="card-box">
                    <h4>📝 Lệnh Chạy Thủ Công Khẩn Cấp</h4>
                    <div style="background:#1e293b; color:#10b981; padding:15px; border-radius:8px; font-family:monospace; margin-bottom:15px;">
                        # 1. Chạy upload 1 short video thủ công:<br>
                        cd {SCRATCH_DIR} && python3 upload_short_videos.py<br><br>
                        # 2. Sửa lỗi Token nếu Token hết hạn/bị lỗi:<br>
                        cd {SCRATCH_DIR} && python3 setup_token_direct.py<br><br>
                        # 3. Chạy các slot video dài nếu LaunchD/Daemon không chạy:<br>
                        cd {SCRATCH_DIR} && bash run_schedule_slot.sh 08am<br>
                        # Tương tự cho: 11am, 18pm, 20pm, 2130pm
                    </div>
                </div>
                
                <div class="card-box">
                    <h4>🔄 Log Auto-Short Upload (upload_short_report.log)</h4>
                    <pre style="background:#f8fafc; padding:15px; border-radius:5px; max-height:400px; overflow-y:auto; font-size:0.85rem;" id="short-log-content">Đang tải log...</pre>
                    <button onclick="fetchLog('short')" class="btn btn-sm btn-secondary mt-2">Làm mới Log Short</button>
                </div>
                
                <div class="card-box">
                    <h4>🤖 Log Auto Pilot Daemon (daemon.log)</h4>
                    <pre style="background:#f8fafc; padding:15px; border-radius:5px; max-height:400px; overflow-y:auto; font-size:0.85rem;" id="daemon-log-content">Đang tải log...</pre>
                    <button onclick="fetchLog('daemon')" class="btn btn-sm btn-secondary mt-2">Làm mới Log Daemon</button>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        function openFolder(target) {{
            fetch('/api/open_folder?target=' + target)
                .then(r => r.json())
                .then(data => alert(data.message))
                .catch(err => alert('Lỗi mở thư mục: ' + err));
        }}
        
        function fetchLog(type) {{
            const el = document.getElementById(type + '-log-content');
            if (el) el.innerText = 'Đang tải...';
            fetch('/api/log?type=' + type)
                .then(r => r.text())
                .then(text => {{
                    if (el) {{
                        el.innerText = text || 'Log trống.';
                        el.scrollTop = el.scrollHeight;
                    }}
                }})
                .catch(err => {{
                    if (el) el.innerText = 'Lỗi tải log: ' + err;
                }});
        }}
        
        // Auto-load logs when tab is clicked
        document.getElementById('logs-tab').addEventListener('click', function() {{
            fetchLog('short');
            fetchLog('daemon');
        }});
    </script>
</body>
</html>
"""
    return html

def run():
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, DashboardRequestHandler)
    print(f"🚀 Multi-Channel Dashboard Server running at http://localhost:{PORT}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
