#!/usr/bin/env python3
"""
Dynamic Title Card Overlay Generator using Python PIL (Pillow)
Renders high-impact vertical 9:16 title overlay cards matching each video topic.
"""

import os
import sys
sys.path.append("/Users/abc/Library/Python/3.9/lib/python/site-packages")
from PIL import Image, ImageDraw, ImageFont

BRAIN_DIR = "/Users/abc/.gemini/antigravity/brain/f1b616c4-34df-4bce-8ba5-f93a710452fb"
SCRATCH_DIR = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management"

def create_title_overlay_image(base_img_path, title_text, output_img_path, series_tag="THẢO DƯƠNG TV"):
    img = Image.open(base_img_path).convert("RGBA")
    W, H = img.size
    
    # Create overlay layer
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Draw dark semi-transparent banner in upper-middle area
    card_top = int(H * 0.18)
    card_bottom = int(H * 0.45)
    card_left = int(W * 0.08)
    card_right = int(W * 0.92)
    
    # Rounded rectangle dark card
    draw.rounded_rectangle([card_left, card_top, card_right, card_bottom], radius=24, fill=(15, 23, 42, 210), outline=(255, 215, 0, 180), width=3)
    
    # Load fonts
    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", index=1, size=46)
        font_sub = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", index=0, size=28)
        font_brand = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", index=1, size=24)
    except Exception:
        font_title = ImageFont.load_default()
        font_sub = font_title
        font_brand = font_title
        
    # Draw Brand Badge
    draw.rounded_rectangle([card_left + 20, card_top + 20, card_left + 260, card_top + 55], radius=12, fill=(139, 92, 246, 220))
    draw.text((card_left + 35, card_top + 25), f"🌸 {series_tag}", fill=(255, 255, 255), font=font_brand)
    
    # Wrap Title Text into lines
    words = title_text.split()
    lines = []
    curr_line = ""
    for w in words:
        test = f"{curr_line} {w}".strip()
        if len(test) <= 22:
            curr_line = test
        else:
            lines.append(curr_line)
            curr_line = w
    if curr_line:
        lines.append(curr_line)
        
    # Render Title Text
    y_text = card_top + 75
    for l in lines[:4]:
        draw.text((card_left + 30, y_text), l, fill=(255, 255, 255), font=font_title)
        y_text += 52
        
    # Combine image and overlay
    final_img = Image.alpha_composite(img, overlay).convert("RGB")
    final_img.save(output_img_path, quality=95)
    print(f"✅ Dynamic Title Card created: {output_img_path}")
    return output_img_path

if __name__ == "__main__":
    base = f"{BRAIN_DIR}/bg_zen_meditation_1787464848840.jpg"
    out = f"{SCRATCH_DIR}/test_title_card.jpg"
    create_title_overlay_image(base, "Lối Sống Biết Đủ (SANTUTTHI): Mở Khóa Bình An Cho Gia Đình", out)
