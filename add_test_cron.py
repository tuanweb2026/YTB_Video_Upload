#!/usr/bin/env python3
"""
Adds a 1-minute test cron job at 09:48 AM to demonstrate 100% background system auto-execution.
"""

import os
import sys
import subprocess

SCRATCH_DIR = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management"
PYTHON_BIN = sys.executable

test_cron_job = f"48 9 * * * {PYTHON_BIN} {SCRATCH_DIR}/auto_pilot_daemon.py slot_11am >> {SCRATCH_DIR}/cron_test.log 2>&1"

def add_test_cron():
    res = subprocess.run(["crontab", "-l"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    existing_cron = res.stdout if res.returncode == 0 else ""
    
    clean_cron = existing_cron.strip() + "\n" + test_cron_job + "\n"
    
    tmp_cron_file = f"{SCRATCH_DIR}/tmp_test_crontab.txt"
    with open(tmp_cron_file, "w", encoding="utf-8") as f:
        f.write(clean_cron)
        
    subprocess.run(["crontab", tmp_cron_file], check=True)
    os.remove(tmp_cron_file)
    print("✅ Added 09:48 AM test job to macOS system crontab!")

if __name__ == "__main__":
    add_test_cron()
