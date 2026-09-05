# HƯỚNG DẪN TỰ CHẠY SCRIPT ĐĂNG 31 SHORTS CÁCH NHAU 15 PHÚT MỖI BÀI
### Kênh YouTube: Thảo Dương TV (@1995lido)

Hệ thống đã được thiết kế sẵn một script tự động hóa hoàn toàn:  
👉 Đường dẫn script: `/Users/abc/.gemini/antigravity/scratch/music_shorts/schedule_daemon.py`

Script này sẽ:
1. Duyệt tuần tự qua danh sách 31 bài hát.
2. Tự tải video nguồn -> Cắt đoạn cao trào vàng -> Chuyển đổi sang chuẩn dọc `9:16 (1080x1920)`.
3. Điền tiêu đề, gắn link video dài vào phần mô tả và đăng công khai (Public) lên kênh.
4. Tự động dọn dẹp file tạm và **chờ đúng 15 phút (900 giây)** mới đăng bài tiếp theo cho đến khi hoàn thành đủ 31 bài.

---

## 🚀 1. LỆNH CHẠY SCRIPT TRONG TERMINAL

Bạn chỉ cần mở ứng dụng **Terminal** trên Mac và chạy một trong 2 cách sau:

### Cách A: Chạy trực tiếp hiển thị tiến trình trên màn hình (Khuyên dùng khi muốn theo dõi)
```bash
python3 /Users/abc/.gemini/antigravity/scratch/music_shorts/schedule_daemon.py
```
*(Bạn sẽ thấy màn hình hiển thị từng bước tải, cắt và thông báo đếm ngược 15 phút).*

---

### Cách B: Chạy ngầm 24/7 (Có thể tắt cửa sổ Terminal máy vẫn tự chạy)
Nếu bạn muốn tắt cửa sổ Terminal hoặc làm việc khác mà tiến trình vẫn tự động đăng bài đều đặn mỗi 15 phút:
```bash
nohup python3 /Users/abc/.gemini/antigravity/scratch/music_shorts/schedule_daemon.py > /Users/abc/.gemini/antigravity/scratch/music_shorts/schedule_daemon.log 2>&1 &
```

---

## 📊 2. LỆNH THEO DÕI TIẾN TRÌNH & XEM LỊCH SỬ

### Xem màn hình log trực tiếp đang chạy:
```bash
tail -f /Users/abc/.gemini/antigravity/scratch/music_shorts/schedule_daemon.log
```
*(Bấm `Ctrl + C` để thoát màn hình xem log).*

### Xem danh sách các video đã đăng thành công (kèm link xem):
```bash
cat /Users/abc/.gemini/antigravity/scratch/music_shorts/schedule_15min_progress.json
```

---

## 🛑 3. CÁCH DỪNG TIẾN TRÌNH KHI CẦN
Nếu bạn muốn tạm ngưng việc tự động đăng bài, mở Terminal và chạy lệnh:
```bash
pkill -f schedule_daemon.py
```

---

## ⚙️ 4. TÙY CHỈNH THỜI GIAN GIỮA CÁC LẦN ĐĂNG (NẾU MUỐN THAY ĐỔI)
Mặc định thời gian giãn cách là **15 phút**. Nếu sau này bạn muốn đổi sang **30 phút** hoặc **1 tiếng**, bạn chỉ cần mở file:  
`/Users/abc/.gemini/antigravity/scratch/music_shorts/schedule_daemon.py`

Và sửa dòng số 26:
```python
INTERVAL_SECONDS = 15 * 60  # 15 phút (900 giây)
# Đổi thành 30 phút: INTERVAL_SECONDS = 30 * 60
# Đổi thành 1 tiếng: INTERVAL_SECONDS = 60 * 60
```
