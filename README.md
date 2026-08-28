# 🚀 HỆ THỐNG TỰ ĐỘNG HÓA KÊNH YOUTUBE & RENDER SHORTS

Hệ thống hỗ trợ tự động dựng video Shorts chuyên đề Chánh Niệm/Tâm Lý/Kinh Nikaya và đăng tải tự động lên YouTube Studio theo khung giờ cố định.

---

## 📂 1. Cấu Trúc Các File Quan Trọng

* **`auto_pilot_daemon.py`**: Bộ điều khiển (Daemon) chạy ngầm 24/7. Kiểm soát thời gian để kích hoạt đúng giờ.
* **`run_auto_pilot_slot.py`**: Trình thực thi chính cho từng slot. Tự động kiểm tra bù (Backfill) nếu bị lỡ giờ do sập nguồn/mạng.
* **`content_generator.py`**: Bộ tạo nội dung, chọn bài tiếp theo chưa đăng từ cơ sở dữ liệu để chống trùng 100%.
* **`video_builder.py`**: Bộ biên tập video (lồng giọng AI Hoài Mỹ/Nam Minh, chèn nhạc nền tần số 432Hz).
* **`dashboard_server.py`**: Local web server hiển thị video xem trước tại cổng `8099`.
* **`published_db.json`**: Cơ sở dữ liệu ghi nhận các bài viết đã được đăng thành công.

---

## ⏰ 2. Khung Giờ Đăng Bài Mặc Định

| Slot | Giờ Phát Sóng | Chuyên Đề | Giọng Đọc AI |
| :--- | :--- | :--- | :--- |
| **slot_08am** | 🌅 08:00 AM | Tư Duy Deep Work & Kỷ Luật Sáng | Southern Female (Hoài Mỹ) |
| **slot_11am** | 🌿 11:00 AM | Giải Tỏa Lo Âu & Sơ Cứu Tâm Lý | Southern Female (Hoài Mỹ) |
| **slot_18pm** | 🌙 18:00 PM | Triết Lý Kinh Nikaya Đêm (Bài 1/3) | Southern Female (Hoài Mỹ) |
| **slot_20pm** | 🌙 20:00 PM | Triết Lý Kinh Nikaya Đêm (Bài 2/3) | Southern Female (Hoài Mỹ) |
| **slot_2130pm**| 💤 21:30 PM | Triết Lý Kinh Nikaya Đêm (Bài 3/3) | Southern Female (Hoài Mỹ) |

---

## 🛠️ 3. Hướng Dẫn Vận Hành Hệ Thống

### A. Quản Lý Tiến Trình Chạy Ngầm (Daemon 24/7)

Để hệ thống tự động đăng bài theo khung giờ mà không cần mở Terminal thủ công, bạn chạy lệnh sau:

* **Bật Daemon chạy ngầm:**
  ```bash
  nohup python3 auto_pilot_daemon.py > daemon_output.log 2>&1 &
  ```

* **Kiểm tra Daemon có đang chạy hay không:**
  ```bash
  ps aux | grep auto_pilot_daemon.py
  ```

* **Xem log lịch sử chạy của Daemon theo thời gian thực:**
  ```bash
  tail -f daemon.log
  ```

* **Dừng Daemon (Tắt chế độ tự động):**
  ```bash
  pkill -f auto_pilot_daemon.py
  ```

---

### B. Quản Lý Local Web Server (Cổng 8099)

Web cục bộ dùng để xem trước các video dự kiến sẽ đăng ngày mai:

* **Bật Web Server:**
  ```bash
  nohup python3 dashboard_server.py > /dev/null 2>&1 &
  ```

* **Địa chỉ truy cập trình duyệt:**
  👉 **`http://localhost:8099`**

* **Tắt Web Server:**
  ```bash
  pkill -f dashboard_server.py
  ```

---

## 📝 4. Cấu Hình Kho Kịch Bản & Cấp Quyền

1. **Cấp quyền YouTube API**: Bạn cần đặt file credentials `client_secret.json` vào thư mục này, sau đó chạy `setup_token_direct.py` để sinh ra file `token.json` cấp quyền.
2. **Sửa danh sách bài viết**:
   * Chuyên đề Nikaya: Sửa trực tiếp nội dung trong file `nikaya_30_authentic_posts.json`.
   * Chuyên đề Deep Work: Sửa trong `content_generator.py`.
