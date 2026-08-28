#!/bin/bash
cd /Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management

# Kiểm tra xem tiến trình đã chạy chưa
if pgrep -f "sleep 3600" | grep -q "upload_short_videos"; then
    echo "⚠️ Tiến trình upload hàng giờ đang chạy rồi!"
    exit 1
fi

echo "🚀 Đang khởi động trình chạy ngầm Upload Short mỗi 1 giờ (Thay thế Crontab)..."

nohup bash -c '
while true; do 
    echo "============================================================" >> upload_short_report.log
    echo "[$(date +"%Y-%m-%d %H:%M:%S")] ⏰ KÍCH HOẠT VÒNG LẶP HÀNG GIỜ..." >> upload_short_report.log
    
    H=$(date +%-H)
    if [ $H -ge 6 ] && [ $H -lt 24 ]; then
        echo "[$(date +"%Y-%m-%d %H:%M:%S")] ⏰ KÍCH HOẠT UPLOAD SHORT..." >> upload_short_report.log
        python3 upload_short_videos.py
    else
        echo "[$(date +"%Y-%m-%d %H:%M:%S")] 💤 Đang là $H giờ. Nằm ngoài khung giờ 06:00-23:59. Bỏ qua upload..." >> upload_short_report.log
    fi
    
    # Ngủ đúng 3600 giây (1 tiếng) rồi chạy lại
    sleep 3600
done
' > hourly_loop.log 2>&1 &

PID=$!
echo "✅ Đã chạy ngầm thành công! (PID: $PID)"
echo "🕒 Hệ thống sẽ tự động upload 1 video rồi nghỉ 1 tiếng."
echo "📊 Bạn có thể theo dõi log tại thư mục Dashweb (Tab Logs) hoặc lệnh:"
echo "   tail -f upload_short_report.log"
