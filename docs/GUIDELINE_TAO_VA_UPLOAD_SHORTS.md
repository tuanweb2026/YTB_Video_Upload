# CẨM NANG HƯỚNG DẪN TỰ TẠO & UPLOAD SHORTS TỪ TERMINAL
### Kênh YouTube: Thảo Dương TV (@1995lido)

Tài liệu này hướng dẫn bạn 2 nội dung chính:
1. **Phương pháp chọn đoạn cao trào vàng (30 - 60s) & cách dựng video Shorts hút người xem**.
2. **Hướng dẫn từng bước cách tự chạy lệnh Terminal để cắt video và upload tự động lên YouTube**.

---

## PHẦN 1: KỸ THUẬT CHỌN ĐOẠN CAO TRÀO & DỰNG SHORTS HÚT TRIỆU VIEW

### 1. Công thức nhận diện "Đoạn Cao Trào Vàng" (The Golden Hook)
Đối với video Shorts, 3 giây đầu tiên quyết định người xem có lướt qua hay ở lại. Do đó:
- **Dòng EDM / Deep House / Melodic House**:
  - Hãy bắt đầu Shorts ngay từ đoạn **Build-up (dồn trống)** kéo dài 3-5 giây rồi nổ vào **Drop** (điệp khúc có bass mạnh nhất). 
  - *Ví dụ mẫu:* Trong bài *Trả Lại Tự Do*, đoạn `01:15 - 01:55` là lúc giai điệu dâng trào và tiếng bass đánh tròn nhất.
- **Dòng Nhạc Thiền / Khí Nhạc / Tây Tạng (Chú Đại Bi, Himalaya)**:
  - Chọn đoạn có tiếng chuông ngân, tiếng sáo vút cao hoặc đoạn tụng trầm hùng nhất (`01:45 - 02:40`).
- **Dòng Ballad / Pop / Rap**:
  - Chọn ngay câu hát đắt giá nhất của điệp khúc (Chorus) hoặc câu punchline ý nghĩa nhất của bài rap (`01:10 - 01:50`).

### 2. Tiêu chuẩn dựng video Shorts đạt chuẩn YouTube
- **Tỉ lệ khung hình (Aspect Ratio)**: Dọc `9:16` (Độ phân giải chuẩn: `1080x1920` px).
- **Thời lượng tối ưu**: Từ **30 đến 45 giây** (đây là thời lượng giữ chân khán giả đạt 90-100% tỷ lệ hoàn thành tốt nhất).
- **Mẫu nội dung mô tả chuẩn chuyển đổi**:
```text
🎵 Nếu bạn nghe hay thì hãy nghe video dài đầy đủ tại link: [DÁN_LINK_VIDEO_DAI]
👉 Đăng ký kênh Thảo Dương TV để thưởng thức thêm nhiều ca khúc & bản phối tuyệt vời: https://www.youtube.com/@1995lido

Cảm ơn các bạn đã lắng nghe và ủng hộ kênh! Chúc bạn có những phút giây thư giãn tuyệt vời. ✨🎶
#ThaoDuongTV #Shorts #Music #AmNhacMoiNgay #[TheLoai]
```
- **Bình luận ghim (Pinned Comment)**:
> *"Bản Full nghe trọn vẹn tại link này cả nhà ơi: [LINK_VIDEO_DAI] ❤️ Đừng quên bấm Đăng Ký kênh Thảo Dương TV nhé!"*

---

## PHẦN 2: HƯỚNG DẪN TỰ DÙNG TERMINAL ĐỂ CẮT & UPLOAD VIDEO LÊN KÊNH

Hệ thống token xác thực của kênh bạn đã được lưu sẵn tại thư mục:  
`/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management/token.json`

Các công cụ sẵn có trên máy:
- **Cắt video & format 9:16**: `/Users/abc/bin/ffmpeg`
- **Tải video YouTube**: `/Users/abc/Library/Python/3.9/bin/yt-dlp`
- **Bộ công cụ upload YouTube**: `/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management/yt_upload.py`

---

### BƯỚC 1: Tải video từ YouTube về máy (Nếu bạn chưa có sẵn file gốc)

Mở Terminal và chạy lệnh sau để tải video gốc:
```bash
/Users/abc/Library/Python/3.9/bin/yt-dlp --extractor-args "youtube:player_client=android" -f "18/best" -o "video_goc.mp4" "https://www.youtube.com/watch?v=k4zDyKYmV14"
```
*(Thay link youtube của video bạn muốn tải).*

---

### BƯỚC 2: Dùng FFmpeg cắt đoạn cao trào & đổi sang chuẩn dọc 9:16

Ví dụ bạn muốn cắt từ phút **01:28** đến phút **02:08** của bài *Chạm Vào Hoàng Hôn*:
```bash
/Users/abc/bin/ffmpeg -y -ss 01:28 -to 02:08 -i "video_goc.mp4" -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" -c:v libx264 -preset fast -crf 22 -c:a aac -b:a 192k "short_video_hoan_thien.mp4"
```
> **Giải thích lệnh**:
> - `-ss 01:28 -to 02:08`: Thời gian bắt đầu và kết thúc đoạn cao trào.
> - `-vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"`: Tự động zoom và cắt hình ảnh sang khung dọc 9:16 (1080x1920) mà không bị méo hình.

---

### BƯỚC 3: Chạy lệnh Upload trực tiếp lên YouTube

Chuyển vào thư mục quản lý:
```bash
cd /Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management
```

#### Cách 3.1: Dùng lệnh `yt_upload.py` có sẵn (Rất đơn giản)
```bash
python3 yt_upload.py /duong_dan_toi/short_video_hoan_thien.mp4 \
  --title "[Shorts] Chạm Vào Hoàng Hôn - Giai điệu Deep House cực đỉnh | Thảo Dương TV #Shorts" \
  --privacy public
```

#### Cách 3.2: Upload với đầy đủ Mô tả & Link video dài (Dùng 1 dòng lệnh Python)
```bash
python3 -c '
import sys
sys.path.insert(0, "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management")
import yt_upload

tokens = yt_upload.get_tokens()
file_path = "/Users/abc/.gemini/antigravity/scratch/music_shorts/short_ChamVaoHoangHon.mp4"
title = "[Shorts] Chạm Vào Hoàng Hôn - Deep House cực chill | Thảo Dương TV #Shorts"
desc = """🎵 Nếu bạn nghe hay thì hãy nghe video dài đầy đủ tại link: https://www.youtube.com/watch?v=k4zDyKYmV14
👉 Đăng ký kênh Thảo Dương TV để thưởng thức thêm nhiều ca khúc & bản phối tuyệt vời: https://www.youtube.com/@1995lido

Cảm ơn các bạn đã lắng nghe và ủng hộ kênh! Chúc bạn có những phút giây thư giãn tuyệt vời. ✨🎶
#ThaoDuongTV #Shorts #Music #DeepHouse"""

tags = ["Shorts", "ThaoDuongTV", "Cham Vao Hoang Hon", "Deep House", "Music"]

vid_id, err = yt_upload.upload_one(file_path, title, desc, tags, privacy="public", tokens=tokens)
if vid_id:
    print(f"🎉 Tải lên thành công: https://www.youtube.com/watch?v={vid_id}")
else:
    print(f"Lỗi: {err}")
'
```

---

## PHẦN 3: SCRIPT TỰ ĐỘNG HÓA 1-CLICK CHO TOÀN BỘ DANH SÁCH

Để bạn không phải gõ từng lệnh thủ công, tôi đã tạo sẵn cho bạn file script tự động hóa hoàn toàn:
👉 **[auto_music_shorts_uploader.py](file:///Users/abc/.gemini/antigravity/brain/2abad14a-9357-444b-9c6b-518de7c823b3/auto_music_shorts_uploader.py)**

Khi cần chạy tự động, bạn chỉ cần mở Terminal và gõ:
```bash
python3 /Users/abc/.gemini/antigravity/brain/2abad14a-9357-444b-9c6b-518de7c823b3/auto_music_shorts_uploader.py
```
Script sẽ:
1. Tự động tải video bài hát từ danh sách.
2. Tự động cắt đúng mốc thời gian vàng (30 - 45 giây).
3. Đổi định dạng thành video đứng `1080x1920`.
4. Điền tiêu đề, gắn link video dài vào mô tả, gắn hashtag và upload trực tiếp lên kênh YouTube của bạn ở chế độ Công khai (Public).
