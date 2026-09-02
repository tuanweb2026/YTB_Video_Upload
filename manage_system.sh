#!/usr/bin/env bash
# ==============================================================================
# 🛠️ Quản Lý Hệ Thống Tự Động Đăng Video YouTube (@1995lido - Thảo Dương TV)
# ==============================================================================

DIR="/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management"
cd "$DIR" || exit 1

ACTION="${1:-status}"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

function show_header() {
    echo -e "${CYAN}==============================================================${NC}"
    echo -e "${CYAN}  🎬 QUẢN LÝ AUTO-PILOT & CRONTAB YOUTUBE — @1995lido        ${NC}"
    echo -e "${CYAN}==============================================================${NC}"
}

function check_status() {
    show_header
    
    # 1. Check Daemon
    echo -e "\n${YELLOW}⏰ 1. KIỂM TRA TIẾN TRÌNH DAEMON (5 KHUNG GIỜ VÀNG):${NC}"
    DAEMON_PID=$(pgrep -f "auto_pilot_daemon.py" | head -n 1)
    if [ -n "$DAEMON_PID" ]; then
        echo -e "  ✅ Trạng thái: ${GREEN}ĐANG CHẠY (PID: $DAEMON_PID)${NC}"
    else
        echo -e "  ❌ Trạng thái: ${RED}ĐÃ DỪNG / CHƯA CHẠY${NC}"
    fi

    # 2. Check Crontab
    echo -e "\n${YELLOW}📡 2. KIỂM TRA LỊCH TRÌNH CRONTAB (30 PHÚT/LẦN):${NC}"
    CRON_CHECK=$(crontab -l 2>/dev/null | grep "upload_short_videos.py")
    if [ -n "$CRON_CHECK" ]; then
        echo -e "  ✅ Trạng thái: ${GREEN}ĐÃ CÀI ĐẶT TRONG HỆ THỐNG${NC}"
        echo -e "  📅 Lịch chạy:  ${CYAN}$CRON_CHECK${NC}"
    else
        echo -e "  ❌ Trạng thái: ${RED}CHƯA CÓ TRONG CRONTAB${NC}"
    fi

    # 3. Check Queue & Manual video count
    echo -e "\n${YELLOW}📦 3. KHO VIDEO CHỜ PHÁT SÓNG:${NC}"
    python3 -c "
from pathlib import Path
import json

scratch = Path('$DIR')
out_manual = scratch / 'output_manual'
out_queue = scratch / 'output_queue'
yt_log = scratch / 'yt_terminal_upload_log.json'

uploaded_set = set()
if yt_log.exists():
    with open(yt_log) as f:
        for x in json.load(f):
            if x.get('status') == 'uploaded':
                uploaded_set.add(x.get('file_name', ''))

manual_files = [f for f in out_manual.glob('*.mp4') if f.stat().st_size > 1024]
pending_manual = [f for f in manual_files if f.name not in uploaded_set]

print(f'  📁 output_manual/ (Crontab 30-phút): {len(manual_files)} video tổng | {len(pending_manual)} video chờ đăng')
queue_files = list(out_queue.glob('shorts_day_13_*.mp4'))
print(f'  📁 output_queue/  (Daemon 5 khung giờ): {len(queue_files)}/5 video Day 13 đã render sẵn')
"

    # 4. Recent Uploads
    echo -e "\n${YELLOW}📺 4. 5 VIDEO GẦN NHẤT ĐÃ LÊN SÓNG:${NC}"
    python3 -c "
import json
from pathlib import Path

yt_log = Path('$DIR') / 'yt_terminal_upload_log.json'
if yt_log.exists():
    with open(yt_log) as f:
        data = json.load(f)
    uploaded = [x for x in data if x.get('status') == 'uploaded']
    for item in uploaded[-5:]:
        ts = item.get('uploaded_at', '')[:16].replace('T', ' ')
        title = item.get('title', '')[:45]
        vid = item.get('youtube_video_id', '')
        print(f'  • [{ts}] {title}... -> https://youtu.be/{vid}')
"
    echo -e "\n${CYAN}==============================================================${NC}\n"
}

function start_daemon() {
    echo -e "${YELLOW}🔄 Đang khởi động lại Daemon...${NC}"
    # Kill old daemon if any
    pkill -f "auto_pilot_daemon.py" 2>/dev/null
    rm -f "$DIR/daemon.lock"
    sleep 1
    
    # Start new daemon
    nohup python3 "$DIR/auto_pilot_daemon.py" >> "$DIR/daemon.log" 2>&1 &
    NEW_PID=$!
    sleep 2
    
    if ps -p $NEW_PID > /dev/null; then
        echo -e "✅ ${GREEN}Daemon đã khởi động thành công với PID: $NEW_PID${NC}"
    else
        echo -e "❌ ${RED}Không thể khởi động Daemon, vui lòng xem log tại daemon.log${NC}"
    fi
}

function reinstall_crontab() {
    echo -e "${YELLOW}🔄 Đang cập nhật lại lịch Crontab 30 phút/lần...${NC}"
    CRON_LINE="0,30 8-23,0 * * * cd $DIR && /usr/bin/python3 $DIR/upload_short_videos.py >> $DIR/upload_short_report.log 2>&1"
    
    # Remove existing upload_short_videos crons and re-add
    (crontab -l 2>/dev/null | grep -v "upload_short_videos.py"; echo "$CRON_LINE") | crontab -
    echo -e "✅ ${GREEN}Đã cài đặt lịch Crontab (08:00 - 24:00 mỗi 30 phút):${NC}"
    echo -e "   $CRON_LINE"
}

function upload_now() {
    echo -e "${YELLOW}⚡ Đang kích hoạt đăng ngay 1 video từ output_manual/...${NC}"
    python3 "$DIR/upload_short_videos.py"
}

case "$ACTION" in
    status)
        check_status
        ;;
    start|restart)
        start_daemon
        reinstall_crontab
        echo ""
        check_status
        ;;
    cron)
        reinstall_crontab
        ;;
    daemon)
        start_daemon
        ;;
    upload-now)
        upload_now
        ;;
    logs)
        tail -n 25 "$DIR/daemon.log"
        ;;
    *)
        echo -e "Cách dùng: $0 {status|restart|daemon|cron|upload-now|logs}"
        ;;
esac
