#!/bin/bash
echo "🛑 Đang dừng trình upload short hàng giờ..."
pkill -f "sleep 3600"
pkill -f "upload_short_videos.py"
echo "✅ Đã dừng thành công!"
