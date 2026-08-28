#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tạo 3 file nhạc thiền WAV thật sự có âm thanh nghe được.
Dùng Python thuần (wave + math, không cần numpy).
"""
import wave, math, struct, os
from pathlib import Path

SAMPLE_RATE = 44100  # Hz — chất lượng CD
DURATION    = 180    # 3 phút mỗi bài
OUT_DIR     = Path(__file__).parent / "studio_music"
OUT_DIR.mkdir(exist_ok=True)

def write_wav(filename, samples, sample_rate=SAMPLE_RATE):
    path = OUT_DIR / filename
    with wave.open(str(path), "w") as f:
        f.setnchannels(2)        # Stereo
        f.setsampwidth(2)        # 16-bit
        f.setframerate(sample_rate)
        f.writeframes(samples)
    size = path.stat().st_size / 1024 / 1024
    print(f"  ✅ {filename}  ({size:.1f} MB, {DURATION}s)")

def to_frames(left_samples, right_samples):
    """Ghép left + right thành bytes stereo interleaved."""
    frames = bytearray()
    for l, r in zip(left_samples, right_samples):
        # Clamp [-1, 1] → int16
        li = max(-32767, min(32767, int(l * 32767)))
        ri = max(-32767, min(32767, int(r * 32767)))
        frames += struct.pack("<hh", li, ri)
    return bytes(frames)

def sine(freq, t, phase=0.0):
    return math.sin(2 * math.pi * freq * t + phase)

def fade(i, total, fade_samples):
    """Fade in / fade out."""
    if i < fade_samples:
        return i / fade_samples
    if i > total - fade_samples:
        return (total - i) / fade_samples
    return 1.0

print("\n🎵 Đang tạo nhạc thiền WAV thật sự...\n")

N          = SAMPLE_RATE * DURATION
FADE_SECS  = 5  # 5 giây fade in/out
FADE_N     = SAMPLE_RATE * FADE_SECS

# ──────────────────────────────────────────────────────
# 1. nhac_thien_432hz.wav
# Nhạc thiền 432 Hz — tần số chữa lành cổ điển
# Layer: 432Hz base + 216Hz (sub) + 864Hz (harmonic) + nhịp điệu alpha 10Hz
# ──────────────────────────────────────────────────────
print("🌙 [1/3] nhac_thien_432hz.wav — Tần Số 432Hz Chữa Lành")
left_buf  = []
right_buf = []

for i in range(N):
    t  = i / SAMPLE_RATE
    fd = fade(i, N, FADE_N)

    # Base 432Hz — âm chính, stereo nhẹ
    base = sine(432, t) * 0.30

    # Sub 216Hz = 432/2 — âm trầm ấm
    sub  = sine(216, t) * 0.18

    # Harmonic 864Hz = 432×2 — âm cao nhẹ
    harm = sine(864, t) * 0.08

    # 3rd harmonic 1296Hz — rất nhẹ
    h3   = sine(1296, t) * 0.04

    # Binaural beat 10Hz (alpha) — left 432Hz, right 442Hz
    # Tạo cảm giác thiền định
    beat_l = sine(432, t) * 0.15
    beat_r = sine(442, t) * 0.15   # lệch 10Hz → binaural 10Hz

    # Nhịp thở nhẹ 0.1Hz (cứ ~10 giây 1 nhịp)
    breath = (math.sin(2 * math.pi * 0.1 * t) * 0.5 + 0.5) * 0.12 + 0.88

    total = (base + sub + harm + h3) * breath * fd
    left_buf.append(total + beat_l * fd)
    right_buf.append(total + beat_r * fd)

write_wav("nhac_thien_432hz.wav", to_frames(left_buf, right_buf))

# ──────────────────────────────────────────────────────
# 2. nhac_thien_pure.wav
# Nhạc thiền thuần khiết — Solfeggio 528Hz (DNA repair)
# Layer: 528Hz + 264Hz + 1056Hz + OM 136Hz + binaural 7Hz theta
# ──────────────────────────────────────────────────────
print("✨ [2/3] nhac_thien_pure.wav — Solfeggio 528Hz Thuần Khiết")
left_buf  = []
right_buf = []

for i in range(N):
    t  = i / SAMPLE_RATE
    fd = fade(i, N, FADE_N)

    # 528Hz — Solfeggio "Mi" frequency
    base = sine(528, t) * 0.28

    # Sub 264Hz
    sub  = sine(264, t) * 0.15

    # OM / Schumann 136.1Hz — âm đất mẹ
    om   = sine(136.1, t) * 0.12

    # Harmonic 1056Hz
    harm = sine(1056, t) * 0.06

    # Binaural 7Hz Theta (sáng tạo, thiền sâu)
    # Left 528Hz, Right 535Hz → binaural 7Hz
    beat_l = sine(528, t, 0.0) * 0.14
    beat_r = sine(535, t, 0.0) * 0.14

    # Pulse chậm 0.07Hz (~14 giây) — sóng thiền
    pulse = (math.sin(2 * math.pi * 0.07 * t) * 0.15 + 0.85)

    total = (base + sub + om + harm) * pulse * fd
    left_buf.append(total + beat_l * fd)
    right_buf.append(total + beat_r * fd)

write_wav("nhac_thien_pure.wav", to_frames(left_buf, right_buf))

# ──────────────────────────────────────────────────────
# 3. nhac_chill_zen.wav
# Nhạc chill zen — nhẹ nhàng, động hơn, 3 tầng melody
# Base 396Hz (Solfeggio FA) + arpeggios + nhịp 4/4 nhẹ
# ──────────────────────────────────────────────────────
print("🌿 [3/3] nhac_chill_zen.wav — Chill Zen Đa Tầng")
left_buf  = []
right_buf = []

# Arpeggio sequence — lặp mỗi 4 giây
# Pentatonic: C D E G A = 261.6 293.7 329.6 392.0 440.0
ARP_NOTES = [261.6, 329.6, 392.0, 329.6, 440.0, 392.0, 329.6, 261.6]
ARP_STEP  = SAMPLE_RATE  # mỗi note 1 giây

for i in range(N):
    t  = i / SAMPLE_RATE
    fd = fade(i, N, FADE_N)

    # Base drone 396Hz Solfeggio (FA)
    drone = sine(396, t) * 0.20

    # Sub 198Hz
    sub   = sine(198, t) * 0.12

    # Arpeggio melody — chuyển note mỗi giây
    note_idx  = (i // ARP_STEP) % len(ARP_NOTES)
    note_freq = ARP_NOTES[note_idx]
    # Giảm click khi chuyển note bằng micro-fade
    note_pos  = i % ARP_STEP
    note_fade = min(1.0, note_pos / 2000) * min(1.0, (ARP_STEP - note_pos) / 2000)
    arp  = sine(note_freq, t) * 0.18 * note_fade

    # Octave cao hơn — nhẹ hơn
    arp_high = sine(note_freq * 2, t) * 0.07 * note_fade

    # Nhịp thở 0.05Hz (~20 giây) — sóng zen
    breath = (math.sin(2 * math.pi * 0.05 * t) * 0.20 + 0.80)

    # Stereo spread — arp lệch trái/phải
    center = (drone + sub) * breath * fd
    left_buf.append(center + (arp + arp_high) * fd * 0.8)
    right_buf.append(center + (arp + arp_high) * fd * 1.2)

write_wav("nhac_chill_zen.wav", to_frames(left_buf, right_buf))

print()
print("=" * 55)
print("  ✅ Tạo xong 3 file nhạc thiền WAV thật sự!")
print(f"  📂 Thư mục: {OUT_DIR}")
print()
print("  🌙 432hz  — Tần số chữa lành, binaural 10Hz alpha")
print("  ✨ Pure   — Solfeggio 528Hz, binaural 7Hz theta")
print("  🌿 Chill  — Pentatonic arpeggios, drone 396Hz")
print()
print("  Cả 3 bài đều: Stereo · 44100Hz · 16-bit · 3 phút")
print("  Có fade in/out 5 giây, không bị click/pop")
print("=" * 55)
