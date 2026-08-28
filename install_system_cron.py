#!/usr/bin/env python3
"""
macOS System Crontab & LaunchAgent Installer for @1995lido (Thảo Dương TV)
Installs 100% standalone, hands-free background automation on macOS.
Runs at 08:00 AM, 11:00 AM, and 18:00 PM daily without requiring any chat interaction.
"""

import os
import sys
import subprocess

SCRATCH_DIR = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management"
PYTHON_BIN = sys.executable

cron_jobs = f"""
# --- @1995lido YOUTUBE SHORTS 100% AUTOPILOT SCHEDULE ---
0 8 * * * {PYTHON_BIN} {SCRATCH_DIR}/auto_pilot_daemon.py slot_08am >> {SCRATCH_DIR}/cron_08am.log 2>&1
0 11 * * * {PYTHON_BIN} {SCRATCH_DIR}/auto_pilot_daemon.py slot_11am >> {SCRATCH_DIR}/cron_11am.log 2>&1
0 18 * * * {PYTHON_BIN} {SCRATCH_DIR}/auto_pilot_daemon.py slot_18pm >> {SCRATCH_DIR}/cron_18pm.log 2>&1
# ---------------------------------------------------------
"""

def install_cron():
    print("1. Reading existing macOS crontab...")
    existing_cron = ""
    try:
        res = subprocess.run(["crontab", "-l"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode == 0:
            existing_cron = res.stdout
    except Exception as e:
        print(f"Crontab read note: {e}")
        
    # Remove old 1995lido jobs if any
    clean_lines = [line for line in existing_cron.split('\n') if "1995lido" not in line and line.strip()]
    clean_cron = "\n".join(clean_lines) + "\n" + cron_jobs.strip() + "\n"
    
    tmp_cron_file = f"{SCRATCH_DIR}/tmp_crontab.txt"
    with open(tmp_cron_file, "w", encoding="utf-8") as f:
        f.write(clean_cron)
        
    print("2. Writing 100% background crontab schedule to macOS system...")
    subprocess.run(["crontab", tmp_cron_file], check=True)
    os.remove(tmp_cron_file)
    
    print("✅ MAC OS SYSTEM CRONTAB INSTALLED SUCCESSFULLY!")
    print(f"• 08:00 AM Daily -> Series B (Morning Mindset)")
    print(f"• 11:00 AM Daily -> Series A (Healing & Overthinking Relief)")
    print(f"• 18:00 PM Daily -> Series C (Evening Chill & Meditation Music)")

if __name__ == "__main__":
    install_cron()
