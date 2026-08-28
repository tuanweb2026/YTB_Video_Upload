#!/usr/bin/env python3
"""
YouTube Channel Growth & Management CLI Tool
Target: @1995lido (Thảo Dương TV) - 1,000 Views Goal
"""

import sys
import json
from datetime import datetime, timedelta

CAMPAIGN_START = datetime(2026, 8, 22)
CAMPAIGN_END = CAMPAIGN_START + timedelta(days=30)

VIDEOS = [
    {
        "id": "shorts_01",
        "type": "Shorts",
        "title": "3 Thói Quen Nhỏ Giúp Nâng Cấp Brain Power Mỗi Sáng #Shorts",
        "alt_title": "Làm 3 Việc Này Mỗi Sáng Để Trí Não Tập Trung 200% #Shorts",
        "target_views": 150,
        "publish_date": "2026-08-23",
        "status": "Ready to Upload",
        "tags": [
            "Thảo Dương TV", "1995lido", "phát triển bản thân", "nâng cấp não bộ",
            "thói quen buổi sáng", "tập trung làm việc", "quản lý thời gian", "Shorts"
        ]
    },
    {
        "id": "shorts_02",
        "type": "Shorts",
        "title": "Đừng Quản Lý Thời Gian, Hãy Quản Lý Năng Lượng! #Shorts",
        "alt_title": "Vì Sao Bạn Càng Quản Lý Thời Gian Càng Kiệt Sức? #Shorts",
        "target_views": 150,
        "publish_date": "2026-08-25",
        "status": "Ready to Upload",
        "tags": [
            "Thảo Dương TV", "1995lido", "quản lý năng lượng", "phát triển bản thân",
            "tránh trì hoãn", "bí quyết thành công", "Shorts"
        ]
    },
    {
        "id": "longform_01",
        "type": "Long-Form",
        "title": "Giao Thức Nâng Cấp Bản Thân 2026 | Nhạc Tập Trung Học Tập & Làm Việc",
        "alt_title": "3 Bước Tối Ưu Não Bộ & Nhạc JazzHop Thư Giãn Đêm Muộn | Thảo Dương TV",
        "target_views": 250,
        "publish_date": "2026-08-29",
        "status": "Script & SEO Ready",
        "tags": [
            "Thảo Dương TV", "1995lido", "giao thức nâng cấp não bộ", "nhạc tập trung học tập",
            "nhạc chill đọc sách", "nhạc jazzhop không lời", "chánh kiến", "phát triển bản thân 2026"
        ]
    }
]

def show_campaign_status():
    today = datetime.now()
    days_left = (CAMPAIGN_END - today).days
    total_target = sum(v["target_views"] for v in VIDEOS)
    
    print("=" * 60)
    print("🚀 YOUTUBE CHANNEL MANAGEMENT DASHBOARD - @1995lido")
    print("=" * 60)
    print(f"📅 Ngày bắt đầu: {CAMPAIGN_START.strftime('%d/%m/%Y')}")
    print(f"🏁 Ngày kết thúc: {CAMPAIGN_END.strftime('%d/%m/%Y')}")
    print(f"⏳ Số ngày còn lại: {max(days_left, 0)} ngày")
    print(f"🎯 Mục tiêu tổng views: 1,000 Views")
    print("-" * 60)
    print("📋 DANH SÁCH VIDEO SẮP XUẤT BẢN:")
    for idx, v in enumerate(VIDEOS, 1):
        print(f"\n{idx}. [{v['type']}] {v['title']}")
        print(f"   - Ngày đăng đề xuất: {v['publish_date']}")
        print(f"   - Target views: {v['target_views']} views")
        print(f"   - Tiêu đề A/B Test: {v['alt_title']}")
        print(f"   - Tags (CSV): {', '.join(v['tags'])}")
    print("=" * 60)

if __name__ == "__main__":
    show_campaign_status()
