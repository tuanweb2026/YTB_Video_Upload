#!/usr/bin/env python3
"""
Extract Nikaya Kinh PDF Content for @1995lido (Thảo Dương TV) Shorts Video Scripts
"""

import os
import sys

pdf_path = "/Users/abc/Documents/Kenh_youtube/Nikaya_kinh/Nikaya_Kinh_Tat_Ca_Bai_Viet.pdf"

def extract_pdf_text():
    print(f"Reading PDF from: {pdf_path}")
    text = ""
    # Try pypdf, fitz (PyMuPDF), pdfplumber or pdftotext CLI
    try:
        import pypdf
        reader = pypdf.PdfReader(pdf_path)
        print(f"Total pages: {len(reader.pages)}")
        for i, page in enumerate(reader.pages[:10]):
            text += f"\n--- PAGE {i+1} ---\n" + (page.extract_text() or "")
    except Exception as e:
        print(f"pypdf failed: {e}. Trying pdftotext CLI...")
        res = subprocess.run(["pdftotext", pdf_path, "-"], stdout=subprocess.PIPE, text=True)
        text = res.stdout
        
    print("=" * 65)
    print(f"EXTRACTED TEXT PREVIEW (First 2000 chars):\n{text[:2000]}")
    print("=" * 65)
    
    with open("/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management/nikaya_raw_extracted.txt", "w", encoding="utf-8") as f:
        f.write(text)

if __name__ == "__main__":
    import subprocess
    extract_pdf_text()
