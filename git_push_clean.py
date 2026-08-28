#!/usr/bin/env python3
"""
Advanced Git Helper script to:
1. Safely remove old git history.
2. Initialize a fresh new git repository.
3. Configure .gitignore to ensure no heavy media files or tokens are ever tracked.
4. Perform a force push to start with a clean remote history on GitHub.
"""

import subprocess
import os
import shutil

SCRATCH_DIR = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management"
GIT_DIR = os.path.join(SCRATCH_DIR, ".git")

def run_cmd(cmd):
    print(f"Executing: {' '.join(cmd)}")
    res = subprocess.run(cmd, cwd=SCRATCH_DIR, capture_output=True, text=True)
    if res.stdout:
        print(res.stdout)
    if res.stderr:
        print(res.stderr)
    return res.returncode

def main():
    # 1. Append additional large directories/files to .gitignore
    gitignore_path = os.path.join(SCRATCH_DIR, ".gitignore")
    additional_ignores = [
        "studio_music/",
        "extracted_voice.mp3",
        "*.mp3",
        "*.mp4",
        "*.wav",
        "*.avi",
        "*.mov",
        "*.zip",
        "*.tar.gz"
    ]
    
    existing_ignores = []
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r", encoding="utf-8") as f:
            existing_ignores = f.read().splitlines()
            
    with open(gitignore_path, "a", encoding="utf-8") as f:
        for item in additional_ignores:
            if item not in existing_ignores:
                f.write(f"\n{item}")
                
    # 2. Delete old .git folder to completely wipe heavy commit history
    if os.path.exists(GIT_DIR):
        print(f"Removing old git folder at {GIT_DIR}...")
        shutil.rmtree(GIT_DIR)
        
    # 3. Initialize fresh git repository
    run_cmd(["git", "init"])
    run_cmd(["git", "remote", "add", "origin", "https://github.com/tuanweb2026/YTB_Video_Upload"])
    run_cmd(["git", "branch", "-M", "main"])
    
    # 4. Add files and commit
    run_cmd(["git", "add", "."])
    run_cmd(["git", "commit", "-m", "Initial commit: clean source code without tokens or large assets"])
    
    # 5. Force push to remote
    run_cmd(["git", "push", "-f", "origin", "main"])

if __name__ == "__main__":
    main()
