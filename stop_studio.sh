#!/usr/bin/env bash
# stop_studio.sh — Dừng Manual Video Studio
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
PID_FILE="$PROJECT_DIR/studio.pid"
PORT=8098
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RESET='\033[0m'

echo -e "${YELLOW}Đang dừng Studio (port $PORT)...${RESET}"
if [ -f "$PID_FILE" ]; then
  PID=$(cat "$PID_FILE")
  kill "$PID" 2>/dev/null && echo -e "${GREEN}✅ Đã dừng PID $PID${RESET}" || echo -e "${YELLOW}PID $PID không còn chạy${RESET}"
  rm -f "$PID_FILE"
fi
# Kill bất kỳ process nào còn trên port
if lsof -ti:$PORT > /dev/null 2>&1; then
  kill $(lsof -ti:$PORT) 2>/dev/null
  echo -e "${GREEN}✅ Đã kill tất cả process trên port $PORT${RESET}"
fi
echo -e "${GREEN}✅ Studio đã dừng.${RESET}"
