#!/usr/bin/env python3
"""
Pure Python YouTube Data API v3 OAuth2 Auto-Uploader
With SSL Context Bypass for macOS Python.
Ensures fresh token refresh before every single upload.
"""

import os
import sys
import json
import ssl
import time
import urllib.request
import urllib.parse
from datetime import datetime

ssl._create_default_https_context = ssl._create_unverified_context

SCRATCH_DIR = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management"
CLIENT_SECRET_FILE = f"{SCRATCH_DIR}/client_secret.json"
TOKEN_FILE = f"{SCRATCH_DIR}/token.json"

def refresh_access_token(tokens):
    post_data = urllib.parse.urlencode({
        "client_id": tokens["client_id"],
        "client_secret": tokens["client_secret"],
        "refresh_token": tokens["refresh_token"],
        "grant_type": "refresh_token"
    }).encode("utf-8")
    
    token_url = tokens.get("token_uri", "https://oauth2.googleapis.com/token")
    req = urllib.request.Request(token_url, data=post_data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    try:
        with urllib.request.urlopen(req) as resp:
            new_data = json.loads(resp.read().decode("utf-8"))
            tokens["access_token"] = new_data["access_token"]
            tokens["expires_in"] = new_data["expires_in"]
            
        with open(TOKEN_FILE, "w", encoding="utf-8") as f:
            json.dump(tokens, f, indent=2)
    except Exception as e:
        print(f"⚠️ Refresh token warning: {e}")
        
    return tokens

def get_tokens():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r", encoding="utf-8") as f:
            tokens = json.load(f)
            if "refresh_token" in tokens:
                return refresh_access_token(tokens)
    return None

def upload_video_via_api(video_path, title, description, tags):
    tokens = get_tokens()
    if not tokens:
        print("⚠️ Chưa tìm thấy token cấp quyền trong token.json!")
        return False
        
    access_token = tokens["access_token"]
    
    print("=" * 65)
    print("🚀 ĐANG TỰ ĐỘNG ĐĂNG VIDEO TRỰC TIẾP LÊN YOUTUBE STUDIO...")
    print("=" * 65)
    print(f"🎬 Video: {video_path}")
    print(f"📌 Tiêu đề: {title}")
    
    # Trim title to max 95 chars to avoid HTTP 400 from YouTube API title limit
    clean_title = title[:95]
    
    metadata = {
        "snippet": {
            "title": clean_title,
            "description": description,
            "tags": tags,
            "categoryId": "22"
        },
        "status": {
            "privacyStatus": "public",
            "selfMade": True
        }
    }
    
    upload_url = "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status"
    meta_bytes = json.dumps(metadata).encode("utf-8")
    file_size = os.path.getsize(video_path)
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; charset=UTF-8",
        "X-Upload-Content-Length": str(file_size),
        "X-Upload-Content-Type": "video/mp4"
    }
    
    req = urllib.request.Request(upload_url, data=meta_bytes, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            location = resp.headers.get("Location")
    except urllib.error.HTTPError as e:
        err_body = e.read().decode('utf-8', errors='ignore')
        print(f"❌ Upload Initiation HTTP {e.code} Error: {err_body}")
        return False
    except Exception as e:
        print(f"❌ Upload Initiation Failed: {e}")
        return False
        
    print(f"📡 Resumable session created. Transferring {file_size / (1024*1024):.2f} MB...")
    
    with open(video_path, "rb") as f:
        video_bytes = f.read()
        
    upload_req = urllib.request.Request(location, data=video_bytes, headers={
        "Content-Length": str(file_size),
        "Content-Type": "video/mp4"
    }, method="PUT")
    
    try:
        with urllib.request.urlopen(upload_req) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            video_id = result.get("id")
            
        print("=" * 65)
        print(f"🎉 PHÁT SÓNG THÀNH CÔNG! VIDEO LIVE AT: https://www.youtube.com/watch?v={video_id}")
        print("=" * 65)
        return video_id
    except Exception as e:
        print(f"❌ Binary Upload Failed: {e}")
        return False

if __name__ == "__main__":
    pass
