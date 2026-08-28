import os
from PIL import Image, ImageDraw, ImageFont

SCRATCH_DIR = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management"
BRAIN_DIR = "/Users/abc/.gemini/antigravity/brain/f1b616c4-34df-4bce-8ba5-f93a710452fb"

img1_path = f"{BRAIN_DIR}/youtube_shorts_thumbnail_1787412760992.jpg"
img2_path = f"{BRAIN_DIR}/shorts_scene2_phone_1787412813911.jpg"
img3_path = f"{BRAIN_DIR}/shorts_scene3_headphones_1787412829319.jpg"

out1 = f"{SCRATCH_DIR}/scene1_captioned.jpg"
out2 = f"{SCRATCH_DIR}/scene2_captioned.jpg"
out3 = f"{SCRATCH_DIR}/scene3_captioned.jpg"

# Try loading system font or default PIL font
try:
    font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 65)
    font_sub = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 45)
except Exception:
    font_large = ImageFont.load_default()
    font_sub = ImageFont.load_default()

def add_captions(img_path, title, subtitle, cta, output_path):
    img = Image.open(img_path).convert("RGB")
    # Resize to exact 1080x1920
    img = img.resize((1080, 1920))
    draw = ImageDraw.Draw(img)
    
    # Add subtle dark gradient overlay at top & bottom for text contrast
    overlay = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rectangle([0, 0, 1080, 450], fill=(0, 0, 0, 140))
    overlay_draw.rectangle([0, 1450, 1080, 1920], fill=(0, 0, 0, 160))
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(img)
    
    # Draw Title (Yellow)
    if title:
        draw.text((540, 200), title, font=font_large, fill=(255, 220, 0), anchor="mm")
        
    # Draw Subtitle (White)
    if subtitle:
        draw.text((540, 310), subtitle, font=font_sub, fill=(255, 255, 255), anchor="mm")
        
    # Draw CTA (Bottom)
    if cta:
        draw.text((540, 1720), cta, font=font_sub, fill=(255, 230, 100), anchor="mm")
        
    img.convert("RGB").save(output_path, quality=95)

# Render Scene 1
add_captions(
    img1_path,
    "3 THÓI QUEN NÂNG CẤP NÃO BỘ 🧠",
    "Bước 1: Không dùng điện thoại 15 phút đầu",
    "Thảo Dương TV (@1995lido)",
    out1
)

# Render Scene 2
add_captions(
    img2_path,
    "BẮT ĐẦU NGÀY MỚI HIỆU QUẢ ✨",
    "Bước 2: Uống nước ấm & viết 3 việc ưu tiên",
    "Đừng để thông báo làm xao nhãng",
    out2
)

# Render Scene 3
add_captions(
    img3_path,
    "ĐƯA NÃO BỘ VÀO TRẠNG THÁI FLOW 🎧",
    "Bước 3: Dành 5 phút nghe nhạc chill tập trung",
    "🔔 ĐĂNG KÝ KÊNH @1995lido NGAY!",
    out3
)

print("✅ Captioned frames generated successfully!")
