#!/usr/bin/env python3
"""
Generates a professional HTML guideline detailing the Auto-Pilot system,
and converts it to a PDF guide using headless Google Chrome.
"""

import os
import subprocess

OUTPUT_DIR = "/Users/abc/Documents/Kenh_youtube"
HTML_PATH = os.path.join(OUTPUT_DIR, "huong_dan_tam_thoi.html")
PDF_PATH = os.path.join(OUTPUT_DIR, "Huong_dan_he_thong_auto_pilot.pdf")
CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def build_pdf_guide():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    html_content = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>HƯỚNG DẪN VẬN HÀNH HỆ THỐNG AUTO-PILOT YOUTUBE</title>
    <style>
        body {
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #333333;
            padding: 40px;
            max-width: 900px;
            margin: auto;
        }
        h1 {
            color: #1e3a8a;
            border-bottom: 3px solid #1e3a8a;
            padding-bottom: 10px;
            text-align: center;
        }
        h2 {
            color: #0f766e;
            margin-top: 30px;
            border-bottom: 1.5px solid #0f766e;
            padding-bottom: 5px;
        }
        h3 {
            color: #1e293b;
        }
        code {
            background-color: #f1f5f9;
            color: #b91c1c;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: Consolas, monospace;
        }
        pre {
            background: #1e293b;
            color: #f8fafc;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
            font-family: Consolas, monospace;
        }
        .note {
            background-color: #f0fdf4;
            border-left: 5px solid #16a34a;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }
        .warning {
            background-color: #fffbeb;
            border-left: 5px solid #d97706;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            border: 1px solid #cbd5e1;
            padding: 10px;
            text-align: left;
        }
        th {
            background-color: #f8fafc;
        }
    </style>
</head>
<body>
    <h1>📋 HƯỚNG DẪN HỆ THỐNG YOUTUBE AUTO-PILOT & RENDER SHORTS</h1>
    <p style="text-align: center; font-style: italic; color: #64748b;">Tài liệu hướng dẫn vận hành chi tiết dành riêng cho Thảo Dương Media</p>
    
    <h2>📂 1. THƯ MỤC QUẢN LÝ DỰ ÁN</h2>
    <p>Toàn bộ mã nguồn và dữ liệu cấu hình hệ thống được lưu tại thư mục chính:</p>
    <pre>📂 Path: /Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management</pre>
    
    <h3>Cấu trúc các file quan trọng:</h3>
    <ul>
        <li><code>content_generator.py</code>: Bộ não sinh kịch bản. Tự động quét DB để chọn bài tiếp theo chưa đăng, chống trùng 100%.</li>
        <li><code>video_builder.py</code>: Bộ dựng video MP4 (lồng giọng nói AI Hoài Mỹ/Nam Minh và ghép nhạc nền 432Hz).</li>
        <li><code>run_auto_pilot_slot.py</code>: Lệnh chạy chính cho từng khung giờ + Tự động chạy bù (Backfill) khi máy bị tắt.</li>
        <li><code>auto_pilot_daemon.py</code>: Daemon chạy ngầm 24/7 kiểm soát giờ giấc để đăng bài tự động.</li>
        <li><code>dashboard_server.py</code>: Local web server hiển thị video xem trước tại cổng <code>8099</code>.</li>
    </ul>

    <h2>⏰ 2. LỊCH PHÁT SÓNG & ĐĂNG BÀI CHI TIẾT</h2>
    <table>
        <tr>
            <th>Khung Giờ</th>
            <th>Chủ Đề</th>
            <th>Loại Giọng Đọc</th>
            <th>Ghi Chú</th>
        </tr>
        <tr>
            <td>🌅 08:00 AM</td>
            <td>Tư Duy Deep Work & Kỷ Luật</td>
            <td>Southern Female (Hoài Mỹ)</td>
            <td>Lấy từ kho DEEP_WORK_SLOTS</td>
        </tr>
        <tr>
            <td>🌿 11:00 AM</td>
            <td>Sơ Cứu Tâm Lý & Giải Tỏa Lo Âu</td>
            <td>Southern Female (Hoài Mỹ)</td>
            <td>Lấy từ kho HEALING_SLOTS</td>
        </tr>
        <tr>
            <td>🌙 18:00 PM</td>
            <td>Triết Lý Kinh Nikaya Đêm (Bài 1/3)</td>
            <td>Southern Female (Hoài Mỹ)</td>
            <td>Lấy tự động từ file PDF Kinh Nikaya</td>
        </tr>
        <tr>
            <td>🌙 20:00 PM</td>
            <td>Triết Lý Kinh Nikaya Đêm (Bài 2/3)</td>
            <td>Southern Female (Hoài Mỹ)</td>
            <td>Lấy tự động từ file PDF Kinh Nikaya</td>
        </tr>
        <tr>
            <td>💤 21:30 PM</td>
            <td>Triết Lý Kinh Nikaya Đêm (Bài 3/3)</td>
            <td>Southern Female (Hoài Mỹ)</td>
            <td>Chánh niệm ngủ ngon, lấy từ PDF</td>
        </tr>
    </table>

    <h2>🛠️ 3. HƯỚNG DẪN ĐIỀU KHIỂN BẰNG TERMINAL</h2>

    <h3>A. Điều khiển Daemon Đăng Bài Tự Động (Cron 24/7)</h3>
    <p>Mỗi khi máy tính của bạn khởi động lại, bạn cần bật lại Daemon để lịch phát sóng chạy tự động:</p>
    
    <p><strong>Bật Daemon:</strong></p>
    <pre>nohup python3 "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management/auto_pilot_daemon.py" &gt; "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management/daemon_output.log" 2&gt;&amp;1 &</pre>
    
    <p><strong>Tắt Daemon:</strong></p>
    <pre>pkill -f auto_pilot_daemon.py</pre>

    <p><strong>Xem Nhật Ký Hoạt Động (Logs):</strong></p>
    <pre>tail -f "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management/daemon.log"</pre>

    <h3>B. Điều khiển Local Web Server (Cổng 8099)</h3>
    <p>Local Web dùng để xem trước các video của ngày mai (25/08...).</p>
    
    <p><strong>Bật Web Server:</strong></p>
    <pre>nohup python3 "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management/dashboard_server.py" &gt;/dev/null 2&gt;&amp;1 &</pre>
    
    <p><strong>Tắt Web Server:</strong></p>
    <pre>pkill -f dashboard_server.py</pre>

    <h2>📝 4. CÁCH CHỈNH SỬA KỊCH BẢN & NỘI DUNG</h2>
    <div class="note">
        <strong>Chỉnh sửa các bài học Kinh Nikaya:</strong> Mở file <code>/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management/nikaya_30_authentic_posts.json</code>. Bạn có thể sửa trực tiếp văn bản, tiêu đề hoặc nguồn trích dẫn của các bài viết từ 1 đến 30 tại đây.
    </div>
    
    <div class="warning">
        <strong>Mẹo nhỏ:</strong> Hệ thống tự động lưu các bài đã đăng vào <code>published_db.json</code>. Nếu bạn muốn hệ thống đăng lại một bài nào đó, chỉ cần xóa dòng của bài đó trong file <code>published_db.json</code>.
    </div>

    <h2>🎥 5. CÁCH DỰNG VIDEO SHORT HÀI HƯỚC MỚI</h2>
    <p>Nếu bạn muốn tự dựng một video đối thoại hài hước (ví dụ như Anh Hai Lúa):</p>
    <pre>python3 "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management/build_hailua_video.py"</pre>
    <p>File video kết quả <code>anh_hai_lua_hai_huoc.mp4</code> sẽ tự động xuất hiện tại thư mục <code>/Users/abc/Documents/Kenh_youtube/anh Hai lua - Hai Huoc/</code>.</p>
</body>
</html>
"""
    
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print("Converting HTML to PDF via headless Google Chrome...")
    subprocess.run([
        CHROME_PATH,
        "--headless",
        "--disable-gpu",
        f"--print-to-pdf={PDF_PATH}",
        HTML_PATH
    ], check=True)
    
    # Cleanup temp HTML
    if os.path.exists(HTML_PATH):
        os.remove(HTML_PATH)
        
    print(f"✅ Guideline PDF successfully created at: {PDF_PATH}")

if __name__ == "__main__":
    build_pdf_guide()
