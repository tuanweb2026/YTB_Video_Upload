#!/usr/bin/env python3
"""
Official macOS Launchd Background Daemon Installer for @1995lido (Thảo Dương TV)
Registers native LaunchAgents in ~/Library/LaunchAgents/com.lido1995.youtube.autopilot.plist
Runs 100% automatically in the background at 08:00 AM, 11:00 AM, and 18:00 PM daily.
"""

import os
import sys
import subprocess

SCRATCH_DIR = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management"
PYTHON_BIN = sys.executable
LAUNCH_AGENTS_DIR = os.path.expanduser("~/Library/LaunchAgents")

def install_launchd_services():
    os.makedirs(LAUNCH_AGENTS_DIR, exist_ok=True)
    
    slots = [
        ("slot_08am", 8, 0, "com.lido1995.youtube.slot08am.plist"),
        ("slot_11am", 11, 0, "com.lido1995.youtube.slot11am.plist"),
        ("slot_18pm", 18, 0, "com.lido1995.youtube.slot18pm.plist"),
    ]
    
    for slot_key, hour, minute, plist_name in slots:
        plist_path = os.path.join(LAUNCH_AGENTS_DIR, plist_name)
        plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.lido1995.youtube.{slot_key}</string>
    <key>ProgramArguments</key>
    <array>
        <string>{PYTHON_BIN}</string>
        <string>{SCRATCH_DIR}/auto_pilot_daemon.py</string>
        <string>{slot_key}</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>{hour}</integer>
        <key>Minute</key>
        <integer>{minute}</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>{SCRATCH_DIR}/launchd_{slot_key}.log</string>
    <key>StandardErrorPath</key>
    <string>{SCRATCH_DIR}/launchd_{slot_key}_err.log</string>
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
"""
        with open(plist_path, "w", encoding="utf-8") as f:
            f.write(plist_content)
            
        print(f"1. Created LaunchAgent plist: {plist_path}")
        subprocess.run(["launchctl", "unload", plist_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(["launchctl", "load", "-w", plist_path], check=True)
        print(f"✅ Active in macOS Launchd: com.lido1995.youtube.{slot_key}")

if __name__ == "__main__":
    install_launchd_services()
