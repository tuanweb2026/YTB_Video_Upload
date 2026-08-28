#!/usr/bin/env bash
# =============================================================
#  🎬 start_studio.sh — Khởi động Manual Video Studio
#  Chạy: bash start_studio.sh
# =============================================================

# ── Màu sắc ──────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; PURPLE='\033[0;35m'; CYAN='\033[0;36m'
BOLD='\033[1m'; RESET='\033[0m'

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
STUDIO_FILE="$PROJECT_DIR/manual_video_studio.py"
LOG_FILE="$PROJECT_DIR/studio_server.log"
PID_FILE="$PROJECT_DIR/studio.pid"
PORT=8098

# ── Banner ────────────────────────────────────────────────────
echo ""
echo -e "${PURPLE}${BOLD}╔══════════════════════════════════════════════════════════╗${RESET}"
echo -e "${PURPLE}${BOLD}║     🎬 Manual Video Studio — @1995lido · Port $PORT      ║${RESET}"
echo -e "${PURPLE}${BOLD}╚══════════════════════════════════════════════════════════╝${RESET}"
echo ""

# ── Kiểm tra nếu đang chạy ───────────────────────────────────
if lsof -ti:$PORT > /dev/null 2>&1; then
  PID_RUNNING=$(lsof -ti:$PORT)
  echo -e "${YELLOW}⚠️  Port $PORT đang được dùng bởi PID: $PID_RUNNING${RESET}"
  echo -e "${YELLOW}   Studio có thể đang chạy rồi!${RESET}"
  echo ""
  echo -e "   ${CYAN}→ Mở trình duyệt: http://localhost:$PORT${RESET}"
  echo -e "   ${CYAN}→ Dừng studio: ${BOLD}bash stop_studio.sh${RESET}"
  echo ""
  read -p "   Bạn muốn KHỞI ĐỘNG LẠI không? (y/n): " RESTART
  if [[ "$RESTART" != "y" && "$RESTART" != "Y" ]]; then
    echo -e "${GREEN}OK — Studio vẫn đang chạy bình thường.${RESET}"
    open http://localhost:$PORT 2>/dev/null
    exit 0
  fi
  echo -e "${YELLOW}   Đang dừng server cũ...${RESET}"
  kill $(lsof -ti:$PORT) 2>/dev/null
  sleep 1
fi

# ── Kiểm tra prerequisites ────────────────────────────────────
echo -e "${BLUE}${BOLD}[1/5] Kiểm tra môi trường...${RESET}"

# Python
PYTHON=$(which python3 2>/dev/null)
if [ -z "$PYTHON" ]; then
  echo -e "${RED}❌ Không tìm thấy python3!${RESET}"
  echo -e "${YELLOW}   Fix: Cài Python từ https://www.python.org/downloads/${RESET}"
  exit 1
fi
echo -e "${GREEN}  ✅ Python: $PYTHON${RESET}"

# Flask
if ! $PYTHON -c "import flask" 2>/dev/null; then
  echo -e "${YELLOW}  ⚠️  Flask chưa cài — đang cài...${RESET}"
  $PYTHON -m pip install flask --user -q
  if ! $PYTHON -c "import flask" 2>/dev/null; then
    echo -e "${RED}  ❌ Cài Flask thất bại!${RESET}"
    echo -e "${YELLOW}  Fix: chạy lệnh: python3 -m pip install flask --user${RESET}"
    exit 1
  fi
fi
echo -e "${GREEN}  ✅ Flask: OK${RESET}"

# edge-tts
if ! $PYTHON -m edge_tts --version 2>/dev/null | grep -q "edge"; then
  echo -e "${YELLOW}  ⚠️  edge-tts chưa cài — đang cài...${RESET}"
  $PYTHON -m pip install edge-tts --user -q
fi
echo -e "${GREEN}  ✅ edge-tts: OK${RESET}"

# FFmpeg
FFMPEG="/Users/abc/bin/ffmpeg"
if [ ! -f "$FFMPEG" ]; then
  echo -e "${RED}  ❌ FFmpeg không tìm thấy tại: $FFMPEG${RESET}"
  echo -e "${YELLOW}  Fix: Tải ffmpeg từ https://evermeet.cx/ffmpeg/ → bỏ vào ~/bin/${RESET}"
  exit 1
fi
echo -e "${GREEN}  ✅ FFmpeg: $FFMPEG${RESET}"

# PIL (optional)
if $PYTHON -c "from PIL import Image" 2>/dev/null; then
  echo -e "${GREEN}  ✅ Pillow (PIL): OK — title card overlay bật${RESET}"
else
  echo -e "${YELLOW}  ⚠️  Pillow chưa cài — title card sẽ dùng ảnh gốc${RESET}"
  echo -e "${YELLOW}     (Optional) Cài: python3 -m pip install Pillow --user${RESET}"
fi

# ── Kiểm tra file studio ──────────────────────────────────────
echo ""
echo -e "${BLUE}${BOLD}[2/5] Kiểm tra file studio...${RESET}"
if [ ! -f "$STUDIO_FILE" ]; then
  echo -e "${RED}❌ Không tìm thấy file: $STUDIO_FILE${RESET}"
  exit 1
fi
echo -e "${GREEN}  ✅ $STUDIO_FILE${RESET}"

# Syntax check
$PYTHON -m py_compile "$STUDIO_FILE" 2>/dev/null
if [ $? -ne 0 ]; then
  echo -e "${RED}  ❌ File Python có lỗi cú pháp!${RESET}"
  $PYTHON -m py_compile "$STUDIO_FILE"
  exit 1
fi
echo -e "${GREEN}  ✅ Python syntax OK${RESET}"

# ── Kiểm tra folder assets ────────────────────────────────────
echo ""
echo -e "${BLUE}${BOLD}[3/5] Kiểm tra thư mục...${RESET}"
BG_DIR="$PROJECT_DIR/studio_backgrounds"
MUSIC_DIR="$PROJECT_DIR/studio_music"
OUTPUT_DIR="$PROJECT_DIR/output_manual"
mkdir -p "$BG_DIR" "$MUSIC_DIR" "$OUTPUT_DIR"

BG_COUNT=$(ls "$BG_DIR"/*.{jpg,jpeg,png,webp} 2>/dev/null | wc -l | tr -d ' ')
MUSIC_COUNT=$(ls "$MUSIC_DIR"/*.{wav,mp3,aiff,m4a} 2>/dev/null | wc -l | tr -d ' ')

echo -e "${GREEN}  ✅ studio_backgrounds/ : $BG_COUNT file ảnh${RESET}"
echo -e "${GREEN}  ✅ studio_music/       : $MUSIC_COUNT file nhạc${RESET}"
echo -e "${GREEN}  ✅ output_manual/      : sẵn sàng${RESET}"

if [ "$BG_COUNT" -eq 0 ]; then
  echo -e "${YELLOW}  ⚠️  Chưa có hình nền! Bỏ file JPG/PNG vào: $BG_DIR${RESET}"
fi
if [ "$MUSIC_COUNT" -eq 0 ]; then
  echo -e "${YELLOW}  ⚠️  Chưa có nhạc nền. Bỏ file WAV/MP3 vào: $MUSIC_DIR${RESET}"
fi

# ── Khởi động server ─────────────────────────────────────────
echo ""
echo -e "${BLUE}${BOLD}[4/5] Khởi động server...${RESET}"
cd "$PROJECT_DIR"

# Xóa log cũ và tạo log mới
> "$LOG_FILE"
echo "=== Studio started at $(date) ===" >> "$LOG_FILE"

# Chạy ngầm với nohup
nohup $PYTHON "$STUDIO_FILE" >> "$LOG_FILE" 2>&1 &
SERVER_PID=$!
echo $SERVER_PID > "$PID_FILE"

# Đợi server boot
echo -e "${YELLOW}  ⏳ Đang boot (tối đa 8 giây)...${RESET}"
for i in {1..8}; do
  sleep 1
  if curl -s "http://localhost:$PORT/" > /dev/null 2>&1; then
    echo -e "${GREEN}  ✅ Server sẵn sàng sau ${i}s (PID: $SERVER_PID)${RESET}"
    break
  fi
  if [ $i -eq 8 ]; then
    echo -e "${RED}  ❌ Server không khởi động được sau 8 giây!${RESET}"
    echo -e "${YELLOW}  Xem log lỗi:${RESET}"
    tail -20 "$LOG_FILE"
    exit 1
  fi
done

# ── Mở trình duyệt ───────────────────────────────────────────
echo ""
echo -e "${BLUE}${BOLD}[5/5] Mở trình duyệt...${RESET}"
open "http://localhost:$PORT" 2>/dev/null || true

# ── Thông tin cuối ────────────────────────────────────────────
echo ""
echo -e "${GREEN}${BOLD}╔══════════════════════════════════════════════════════════╗${RESET}"
echo -e "${GREEN}${BOLD}║  ✅ Studio đang chạy!                                    ║${RESET}"
echo -e "${GREEN}${BOLD}╚══════════════════════════════════════════════════════════╝${RESET}"
echo ""
echo -e "  🌐  URL      : ${CYAN}${BOLD}http://localhost:$PORT${RESET}"
echo -e "  🔧  PID      : ${CYAN}$SERVER_PID${RESET}"
echo -e "  📋  Log file : ${CYAN}$LOG_FILE${RESET}"
echo ""
echo -e "${BOLD}Lệnh hữu ích:${RESET}"
echo -e "  ${YELLOW}bash stop_studio.sh${RESET}          ← Dừng server"
echo -e "  ${YELLOW}tail -f $LOG_FILE${RESET}  ← Xem log realtime"
echo -e "  ${YELLOW}bash start_studio.sh${RESET}         ← Khởi động lại"
echo ""

# ── Crontab cho Auto Short Upload ─────────────────────────────
echo ""
echo -e "${BLUE}${BOLD}[CRON] Thiết lập crontab auto-short upload...${RESET}"

UPLOAD_SHORT_SCRIPT="$PROJECT_DIR/upload_short_videos.py"
UPLOAD_SHORT_REPORT="$PROJECT_DIR/upload_short_report.log"
CRON_LINE="0 * * * * cd $PROJECT_DIR && $PYTHON $UPLOAD_SHORT_SCRIPT >> $UPLOAD_SHORT_REPORT 2>&1"

if [ -f "$UPLOAD_SHORT_SCRIPT" ]; then
  # Kiểm tra xem crontab đã có entry chưa
  if crontab -l 2>/dev/null | grep -F "upload_short_videos.py" > /dev/null 2>&1; then
    echo -e "${GREEN}  ✅ Crontab entry đã tồn tại — không thêm lại.${RESET}"
  else
    # Thử thêm crontab
    (crontab -l 2>/dev/null; echo "$CRON_LINE") | crontab - 2>/dev/null
    if [ $? -eq 0 ]; then
      echo -e "${GREEN}  ✅ Crontab auto-short upload đã được cài đặt! (mỗi giờ upload 1 video)${RESET}"
    else
      echo -e "${YELLOW}  ⚠️  Không thể cài crontab tự động (permission denied).${RESET}"
      echo -e "${CYAN}  📋 Hướng dẫn cài thủ công:${RESET}"
      echo ""
      echo -e "${BOLD}     Bước 1: Mở crontab editor:${RESET}"
      echo -e "       ${YELLOW}crontab -e${RESET}"
      echo ""
      echo -e "${BOLD}     Bước 2: Dán dòng này vào cuối file:${RESET}"
      echo -e "       ${CYAN}$CRON_LINE${RESET}"
      echo ""
      echo -e "${BOLD}     Bước 3: Lưu và thoát (trong vi: :wq)${RESET}"
      echo ""
      echo -e "  ${GRAY}Tip: Nếu macOS chặn crontab, vào:${RESET}"
      echo -e "  ${GRAY}System Preferences → Privacy & Security → Full Disk Access${RESET}"
      echo -e "  ${GRAY}→ Thêm /usr/sbin/cron${RESET}"
    fi
  fi
else
  echo -e "${YELLOW}  ⚠️  File $UPLOAD_SHORT_SCRIPT chưa tồn tại.${RESET}"
fi

# ── Hướng dẫn Upload Manual ──────────────────────────────────
echo ""
echo -e "${BOLD}📋 UPLOAD MANUAL (nếu crontab không chạy):${RESET}"
echo ""
echo -e "  ${CYAN}# Upload 1 short video (tự động chọn video chưa upload):${RESET}"
echo -e "  ${YELLOW}python3 yt_upload.py --auto-short${RESET}"
echo ""
echo -e "  ${CYAN}# Hoặc dùng wrapper script:${RESET}"
echo -e "  ${YELLOW}python3 upload_short_videos.py${RESET}"
echo ""
echo -e "  ${CYAN}# Upload toàn bộ folder output_manual/:${RESET}"
echo -e "  ${YELLOW}python3 yt_upload.py --folder output_manual/ --skip-uploaded${RESET}"
echo ""
echo -e "  ${CYAN}# Xem log báo cáo upload:${RESET}"
echo -e "  ${YELLOW}cat upload_short_report.log${RESET}"
echo ""
echo -e "  ${CYAN}# Xem lịch sử upload:${RESET}"
echo -e "  ${YELLOW}python3 yt_upload.py --history${RESET}"
echo ""

# ── Live log theo dõi ────────────────────────────────────────
echo -e "${PURPLE}${BOLD}══ LOG REALTIME (Ctrl+C để dừng theo dõi — server vẫn chạy) ══${RESET}"
echo ""
tail -f "$LOG_FILE"
