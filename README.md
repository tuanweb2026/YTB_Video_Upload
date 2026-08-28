# 🎬 YTB Video Upload & Autopilot Studio (@1995lido)

Hệ thống tự động hóa toàn diện quản lý kênh YouTube, từ khâu tạo video hàng loạt (tổng hợp kịch bản, text-to-speech, ghép nhạc, render MP4) cho đến tự động đăng video theo lịch (auto-upload) và cứu view cho các video thấp.

## 🌟 Tính năng chính

1. **Studio Tạo Video Tự Động (`auto_create_daily_videos.py`)**
   Tạo hàng loạt video Shorts & Video dài tự động từ kho dữ liệu bài học/kịch bản định dạng JSON.
   - Tự động lấy ảnh nền ngẫu nhiên từ thư mục `studio_backgrounds/`.
   - Tạo giọng đọc AI siêu thực (sử dụng thư viện `edge-tts`).
   - Ghép nối audio, chèn nhạc nền thư giãn (`studio_music/`).
   - Tự động render thành file MP4 hoàn chỉnh bằng `FFmpeg` với tốc độ cao.

2. **Auto Upload Lên Lịch Hàng Giờ (`start_hourly_shorts.sh`)**
   Vòng lặp tiến trình ngầm (Daemon) tự động đăng 1 video chưa publish mỗi giờ.
   - Tích hợp tính năng nhận diện khung giờ vàng (chỉ hoạt động từ **06:00 đến 23:59**, dừng hoạt động ban đêm để tránh bị YouTube phạt spam).
   - Tự động lấy file từ thư mục `output_manual/`.
   
3. **Quản trị Kênh & Upload (Bypass giới hạn)**
   Công cụ `yt_upload.py` hỗ trợ kết nối trực tiếp với YouTube API v3 bằng giao thức OAuth2. Giúp việc đăng tải an toàn, chuẩn SEO và không bị chặn bởi các công cụ bắt Bot của YouTube.

4. **Re-upload Cứu View (`reupload_low_view_shorts.py`)**
   Tự động quét lịch sử toàn bộ video trên kênh và dùng API để kiểm tra lượt view thời gian thực.
   - Lọc ra các video Shorts có số lượt xem **dưới 200 view**.
   - Tự động chỉnh sửa mã nhị phân (hash bypass) vào file MP4 gốc để YouTube nhận diện là một video hoàn toàn mới (tránh lỗi Reused Content).
   - Tự động Re-upload các video này lên kênh với nhịp độ giãn cách **15 phút/video** để bảo vệ an toàn cho kênh.
   - Có công cụ trực quan theo dõi tiến độ Re-upload (`check_reupload_progress.py`).

5. **Local Web Dashboard (`dashboard_server.py`)**
   Giao diện web cục bộ siêu nhẹ chạy tại `localhost:8098` và `localhost:8099` để:
   - Preview (Xem thử) các video offline trước khi hệ thống đăng.
   - Kiểm tra log lỗi hệ thống trực tiếp trên trình duyệt.

## 🚀 Cài đặt (Setup)

### 1. Yêu Cầu Hệ Thống
- **OS**: macOS / Linux (Khuyến nghị macOS Apple Silicon hoặc Intel).
- **Python**: 3.9 trở lên.
- **FFmpeg**: Yêu cầu phải cài đặt sẵn trong máy (qua Homebrew: `brew install ffmpeg`).

### 2. Cài Đặt Thư Viện (Dependencies)
Chạy lệnh sau để cài đặt các gói Python cần thiết:
```bash
pip3 install edge-tts moviepy pillow opencv-python google-auth-oauthlib google-api-python-client
```

### 3. Xác thực YouTube API
- Cần có file `client_secret.json` tải về từ Google Cloud Console (Đã bật Youtube Data API v3).
- Chạy lệnh `python3 setup_token_direct.py` để tạo file xác thực `token.json` lần đầu tiên.

## 🛠 Cách sử dụng (Usage)

### 1. Tạo Video Hàng Loạt Tự Động
Hệ thống sẽ bốc nội dung từ kho kịch bản JSON và tạo thành file MP4.
```bash
# Tạo 5 video (4 short, 1 dài) cho hôm nay
python3 auto_create_daily_videos.py --today

# Tạo video hàng loạt cho ngày 31 đến ngày 60
python3 auto_create_daily_videos.py --range 31 60
```
*(Video xuất ra sẽ được lưu tại thư mục `output_manual/`)*

### 2. Đăng Video Tự Động (Hourly Daemon)
Kích hoạt tiến trình ngầm tự đăng 1 video mỗi giờ.
```bash
# Khởi động Auto Upload
bash start_hourly_shorts.sh

# Dừng Auto Upload
bash stop_hourly_shorts.sh
```

### 3. Cứu View (Quét & Re-upload video < 200 views)
Khởi động tiến trình cày view tự động (treo ngầm):
```bash
nohup python3 reupload_low_view_shorts.py > reupload_live_log.txt 2>&1 &
```
Bạn có thể xem báo cáo tiến trình cày view bất cứ lúc nào bằng lệnh:
```bash
python3 check_reupload_progress.py
```

### 4. Mở Web Dashboard Review
```bash
python3 dashboard_server.py
```
Sau đó truy cập: [http://localhost:8098](http://localhost:8098)

## 📁 Cấu trúc Thư mục Chính
- `studio_backgrounds/`: Nơi chứa ảnh nền gốc (JPG, PNG).
- `studio_music/`: Nơi chứa nhạc nền (ví dụ nhạc thiền 432Hz).
- `output_manual/`: Nơi chứa các video MP4 thành phẩm chờ hệ thống đăng.
- `auto_schedule_db.json`, `manual_upload_log.json`: Cơ sở dữ liệu ghi chú lịch sử tạo và lịch sử đăng.

---
**Tác giả**: @1995lido - Hỗ trợ phát triển bởi Antigravity AI
