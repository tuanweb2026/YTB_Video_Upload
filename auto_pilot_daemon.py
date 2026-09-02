#!/usr/bin/env python3
"""
Standalone 24/7 Auto-Pilot Background Daemon for Thảo Dương TV (@1995lido)
WITH STRICT PID-LOCKING SYSTEM to prevent concurrent duplicate daemon instances.
"""

import os
import sys
import time
import subprocess
from datetime import datetime

SCRATCH_DIR = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management"
RUNNER_SCRIPT = f"{SCRATCH_DIR}/run_auto_pilot_slot.py"
LOCK_FILE = f"{SCRATCH_DIR}/daemon.lock"

# Schedule configuration
SCHEDULE = {
    "08:00": "slot_08am",
    "11:00": "slot_11am",
    "18:00": "slot_18pm",
    "20:00": "slot_20pm",
    "21:30": "slot_2130pm"
}

def log_message(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {msg}\n"
    print(log_line, end="")
    try:
        with open(f"{SCRATCH_DIR}/daemon.log", "a", encoding="utf-8") as f:
            f.write(log_line)
    except Exception:
        pass

def acquire_lock():
    pid = os.getpid()
    if os.path.exists(LOCK_FILE):
        try:
            with open(LOCK_FILE, "r") as f:
                old_pid = int(f.read().strip())
            # Check if old process is still active
            os.kill(old_pid, 0)
            print(f"⚠️ DAEMON ALREADY RUNNING (PID: {old_pid}). Exiting to prevent duplicates.")
            sys.exit(0)
        except (ValueError, OSError):
            # Old process is dead, we can overwrite the lock
            pass
            
    with open(LOCK_FILE, "w") as f:
        f.write(str(pid))
    log_message(f"🔒 Acquired lock file for PID {pid}.")

def release_lock():
    if os.path.exists(LOCK_FILE):
        try:
            os.remove(LOCK_FILE)
            log_message("🔓 Released lock file.")
        except Exception:
            pass

def run_slot(slot_key):
    log_message(f"🔔 Scheduled trigger for: {slot_key}. Executing runner script...")
    try:
        res = subprocess.run(
            [sys.executable, RUNNER_SCRIPT, slot_key],
            cwd=SCRATCH_DIR,
            capture_output=True,
            text=True
        )
        if res.returncode == 0:
            log_message(f"✅ Executed successfully for {slot_key}.")
        else:
            log_message(f"❌ Execution failed for {slot_key}. Error:\n{res.stderr}")
    except Exception as e:
        log_message(f"💥 Exception during execution of {slot_key}: {e}")

def run_short_upload():
    log_message("⚡ 30-min Short auto-upload trigger starting...")
    try:
        res = subprocess.run(
            [sys.executable, f"{SCRATCH_DIR}/upload_short_videos.py"],
            cwd=SCRATCH_DIR,
            capture_output=True,
            text=True
        )
        if res.returncode == 0:
            log_message("✅ 30-min Short auto-upload completed successfully.")
        else:
            log_message(f"⚠️ 30-min Short auto-upload finished with code {res.returncode}.")
    except Exception as e:
        log_message(f"💥 Exception during short auto-upload: {e}")

def daemon_loop():
    acquire_lock()
    log_message("🚀 Standalone Auto-Pilot Daemon started successfully!")
    log_message(f"📅 Active schedule slots: {list(SCHEDULE.keys())}")
    
    # Run backfill check immediately on startup
    log_message("🔄 Checking and backfilling missed slots on daemon startup...")
    run_slot("startup_check")
    
    last_triggered_date = ""
    last_triggered_time = ""
    last_short_slot = ""
    last_short_upload_time = time.time()
    
    try:
        while True:
            now = datetime.now()
            current_date = now.strftime("%Y-%m-%d")
            current_time_str = now.strftime("%H:%M")
            current_hour = now.hour
            current_minute = now.minute
            
            # 1. Check 5 golden hour slots
            if current_time_str in SCHEDULE:
                if last_triggered_date != current_date or last_triggered_time != current_time_str:
                    slot_key = SCHEDULE[current_time_str]
                    log_message(f"⏰ Time matches scheduled slot: {current_time_str} -> {slot_key}")
                    run_slot(slot_key)
                    last_triggered_date = current_date
                    last_triggered_time = current_time_str
            
            # 2. Check 30-minute Shorts upload (08:00 - 23:59) with sleep wake-up catch-up
            if 8 <= current_hour <= 23:
                is_exact_slot = (current_minute in [0, 30]) and (last_short_slot != f"{current_date}_{current_hour}_{current_minute}")
                is_overdue = (time.time() - last_short_upload_time >= 1920) # 32 mins overdue due to sleep
                
                if is_exact_slot or is_overdue:
                    last_short_slot = f"{current_date}_{current_hour}_{current_minute}"
                    last_short_upload_time = time.time()
                    run_short_upload()
                    
            time.sleep(10)
    except KeyboardInterrupt:
        log_message("🛑 Daemon stopped by user request.")
    except Exception as e:
        log_message(f"⚠️ Unexpected error in daemon loop: {e}")
    finally:
        release_lock()

if __name__ == "__main__":
    daemon_loop()

