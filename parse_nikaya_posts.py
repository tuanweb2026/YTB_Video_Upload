#!/usr/bin/env python3
"""
Parse Nikaya Kinh PDF Posts and Convert to 10 High-Impact YouTube Shorts Scripts
Source: /Users/abc/Documents/Kenh_youtube/Nikaya_kinh/Nikaya_Kinh_Tat_Ca_Bai_Viet.pdf
"""

import os
import sys
import json
import re

sys.path.append("/Users/abc/Library/Python/3.9/lib/python/site-packages")
import pypdf

pdf_path = "/Users/abc/Documents/Kenh_youtube/Nikaya_kinh/Nikaya_Kinh_Tat_Ca_Bai_Viet.pdf"
scratch_dir = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management"

def parse_posts():
    reader = pypdf.PdfReader(pdf_path)
    full_text = ""
    print(f"Total pages in PDF: {len(reader.pages)}")
    
    # Read first 80 pages to extract meaningful Nikaya articles
    for i, page in enumerate(reader.pages[3:80]):
        txt = page.extract_text() or ""
        full_text += f"\n--- PAGE {i+4} ---\n" + txt
        
    with open(f"{scratch_dir}/nikaya_extracted_pages.txt", "w", encoding="utf-8") as f:
        f.write(full_text)
        
    print(f"Extracted {len(full_text)} chars from pages 4-80.")
    return full_text

if __name__ == "__main__":
    parse_posts()
