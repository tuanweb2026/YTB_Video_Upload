#!/usr/bin/env python3
"""
Pure Python Diagnostic script to check what videos are actually live on the YouTube channel
using only standard libraries.
"""

import os
import json
import ssl
import urllib.request
import urllib.parse

ssl._create_default_https_context = ssl._create_unverified_context

SCRATCH_DIR = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management"
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

def diag_channel():
    tokens = get_tokens()
    if not tokens:
        print("❌ token.json not found or missing credentials.")
        return
        
    access_token = tokens["access_token"]
    
    # 1. Get Channel ID and Uploads Playlist ID
    channel_url = "https://www.googleapis.com/youtube/v3/channels?part=snippet,contentDetails,statistics&mine=true"
    req_ch = urllib.request.Request(channel_url, headers={"Authorization": f"Bearer {access_token}"})
    
    try:
        with urllib.request.urlopen(req_ch) as resp:
            ch_data = json.loads(resp.read().decode("utf-8"))
            
        if not ch_data.get("items"):
            print("❌ No channel items returned.")
            return
            
        channel = ch_data["items"][0]
        ch_title = channel["snippet"]["title"]
        ch_id = channel["id"]
        uploads_playlist_id = channel["contentDetails"]["relatedPlaylists"]["uploads"]
        
        print(f"🟢 Authenticated Channel: {ch_title} (ID: {ch_id})")
        print(f"📊 Statistics: Subscriber Count={channel['statistics'].get('subscriberCount')}, Video Count={channel['statistics'].get('videoCount')}")
        
        # 2. Get playlist items from Uploads Playlist
        playlist_url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet,status&playlistId={uploads_playlist_id}&maxResults=50"
        req_pl = urllib.request.Request(playlist_url, headers={"Authorization": f"Bearer {access_token}"})
        
        with urllib.request.urlopen(req_pl) as resp:
            pl_data = json.loads(resp.read().decode("utf-8"))
            
        items = pl_data.get("items", [])
        print("\n📺 ACTUAL VIDEOS ON YOUTUBE CHANNEL:")
        if not items:
            print("ℹ️ No videos found in the Uploads playlist.")
        for idx, item in enumerate(items):
            title = item["snippet"]["title"]
            video_id = item["snippet"]["resourceId"]["videoId"]
            privacy = item["status"]["privacyStatus"]
            published_at = item["snippet"]["publishedAt"]
            print(f"  {idx+1}. [{privacy.upper()}] {title} (ID: {video_id}) - Uploaded at: {published_at}")
            
    except Exception as e:
        print(f"❌ Error during diagnosis: {e}")

if __name__ == "__main__":
    diag_channel()
