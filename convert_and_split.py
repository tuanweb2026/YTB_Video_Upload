#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""convert_and_split.py

Utility to convert a video/audio file (MP4) to WAV or MP3 and optionally split the
result into equal‑duration chunks (e.g. 20 seconds each).

Features
--------
* Input: any file ffmpeg can read – MP4 is the common case.
* Output format: wav or mp3 (chosen via ``--to``).
* Optional ``--segment`` to cut the output into pieces of *N* seconds.
* Automatic naming: ``<orig_basename>_part001.wav`` … ``_partNN.wav``.
* Uses the system ffmpeg binary at ``/Users/abc/bin/ffmpeg`` (full path – no
  reliance on PATH).
* Simple CLI via ``argparse`` – works on macOS without extra Python deps.

Example usage
-------------
    # Convert to wav without splitting
    python3 convert_and_split.py input.mp4 --to wav

    # Convert to mp3 and split every 20 s
    python3 convert_and_split.py video.mp4 --to mp3 --segment 20

    # Save all parts into a custom folder
    python3 convert_and_split.py movie.mp4 --to wav --segment 15 --out-dir ./segments
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration – path to ffmpeg on the user machine
# ---------------------------------------------------------------------------
FFMPEG = "/Users/abc/bin/ffmpeg"

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------
def run_ffmpeg(cmd: list[str]):
    """Run an ffmpeg command, printing the command line and raising on error."""
    print(f"[ffmpeg] {' ".join(cmd)}")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if result.returncode != 0:
        sys.stderr.write(result.stdout)
        raise RuntimeError(f"ffmpeg exited with code {result.returncode}")
    return result.stdout

def get_duration(input_path: Path) -> float:
    """Return the duration (seconds) of *input_path* using ffprobe (via ffmpeg)."""
    cmd = [
        FFMPEG,
        "-i", str(input_path),
        "-hide_banner",
        "-show_entries", "format=duration",
        "-print_format", "default=noprint_wrappers=1:nokey=1",
    ]
    # ffmpeg prints the info to stderr, so capture both streams
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    out = result.stdout.strip()
    # The last line is the duration (float). If parsing fails, fallback to 0.
    try:
        return float(out.splitlines()[-1])
    except Exception:
        return 0.0

def convert(input_path: Path, out_path: Path, out_format: str):
    """Convert *input_path* to *out_path* with the desired container/codec.

    ``out_format`` must be either ``wav`` or ``mp3``.  The function builds the
    appropriate ffmpeg arguments (pcm_s16le for wav, libmp3lame for mp3).
    """
    if out_format == "wav":
        codec_args = ["-c:a", "pcm_s16le"]
    elif out_format == "mp3":
        codec_args = ["-c:a", "libmp3lame", "-q:a", "2"]  # quality 2 ≈ 190‑200 kbps
    else:
        raise ValueError("Unsupported format: {}".format(out_format))

    cmd = [
        FFMPEG,
        "-y",  # overwrite without asking
        "-i", str(input_path),
        *codec_args,
        str(out_path),
    ]
    run_ffmpeg(cmd)

def split_file(input_path: Path, segment_len: int, out_dir: Path, out_format: str):
    """Split *input_path* into *segment_len*‑second pieces.

    Files are named ``<base>_part001.<ext>``, ``<base>_part002.<ext>`` … and are
    written into *out_dir* (which is created if it does not exist).
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    base_name = input_path.stem
    # ffmpeg option: -f segment -segment_time <seconds>
    # Use -reset_timestamps 1 to start timestamps at zero for each segment.
    segment_pattern = out_dir / f"{base_name}_part%03d.{out_format}"
    cmd = [
        FFMPEG,
        "-y",
        "-i", str(input_path),
        "-f", "segment",
        "-segment_time", str(segment_len),
        "-reset_timestamps", "1",
        str(segment_pattern),
    ]
    run_ffmpeg(cmd)

# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Convert MP4 → WAV/MP3 and optionally split into fixed‑length chunks.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("input", type=str, help="Path to the source MP4 (or any ffmpeg‑readable) file")
    parser.add_argument("--to", choices=["wav", "mp3"], default="wav", help="Target container/codec (default: wav)")
    parser.add_argument("--segment", type=int, default=0,
                        help="If >0, split the output into pieces of this many seconds (e.g. 20).")
    parser.add_argument("--out-dir", type=str, default=".",
                        help="Directory where converted (and split) files will be placed. Default: current folder.")
    parser.add_argument("--prefix", type=str, default="",
                        help="Optional prefix added before the generated filename(s).")
    args = parser.parse_args()

    inp_path = Path(args.input).expanduser().resolve()
    if not inp_path.is_file():
        sys.exit(f"❌ Input file not found: {inp_path}")

    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    # Determine final base name (prefix + original stem)
    base = f"{args.prefix}{inp_path.stem}" if args.prefix else inp_path.stem
    out_ext = args.to
    out_file = out_dir / f"{base}.{out_ext}"

    # -------------------------------------------------------------------
    # Step 1 – conversion
    # -------------------------------------------------------------------
    print(f"📂 Converting {inp_path.name} → {out_file.name} ({out_ext})")
    try:
        convert(inp_path, out_file, args.to)
        print("✅ Conversion done")
    except Exception as e:
        sys.exit(f"❌ Conversion failed: {e}")

    # -------------------------------------------------------------------
    # Step 2 – optional splitting
    # -------------------------------------------------------------------
    if args.segment and args.segment > 0:
        print(f"✂️  Splitting {out_file.name} into {args.segment}s chunks…")
        try:
            split_file(out_file, args.segment, out_dir, out_ext)
            # Remove the single combined file – the user usually only wants the parts.
            out_file.unlink(missing_ok=True)
            print("✅ Splitting completed. Files written to:")
            for p in sorted(out_dir.glob(f"{base}_part*.{out_ext}")):
                print(f"   • {p.name}")
        except Exception as e:
            sys.exit(f"❌ Splitting failed: {e}")
    else:
        print("📁 No splitting requested – single file created.")

    # Summary
    total = sum(p.stat().st_size for p in out_dir.glob(f"*{out_ext}"))
    print(f"🗂️  Output directory: {out_dir}")
    print(f"📏 Total size of generated files: {total/1024/1024:.2f} MiB")

if __name__ == "__main__":
    main()
