#!/usr/bin/env python3
"""Make an upload-grade master from a recorded reel.

  master.py reels/<slug> [--platform instagram|youtube] [--in reel.mp4]

Two things this fixes:

1. Bitrate. The capture pass optimises for a small file. Smooth dark gradients are the
   worst case for H.264 and band badly at ~2 Mbps, and every platform re-encodes what
   you upload - so a thin source gets thinner. This targets a high, clean bitrate.

2. Audio. Reels ship mono 44.1k by default here; platforms expect 48k stereo AAC.

It does NOT fix transit. WhatsApp recompresses video in normal "photo/video" mode no
matter what you feed it - send as a Document instead.
"""
import argparse, json, os, subprocess, sys

SPEC = {
  # crf, maxrate, bufsize, audio kbps
  "instagram": (16, "14M", "28M", 192),
  "youtube":   (15, "20M", "40M", 192),
}

def probe(p):
    o = json.loads(subprocess.run(["ffprobe","-v","error","-print_format","json",
        "-show_format","-show_streams",p],capture_output=True,text=True).stdout)
    v = next(s for s in o["streams"] if s["codec_type"]=="video")
    return {"dur":float(o["format"]["duration"]), "size":int(o["format"]["size"]),
            "br":int(o["format"].get("bit_rate",0)), "w":v["width"], "h":v["height"]}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir"); ap.add_argument("--platform", default="instagram", choices=list(SPEC))
    ap.add_argument("--in", dest="src", default="reel.mp4")
    a = ap.parse_args()
    src = os.path.join(a.dir, a.src)
    if not os.path.exists(src): sys.exit("no " + src)
    crf, maxrate, bufsize, akbps = SPEC[a.platform]
    out = os.path.join(a.dir, f"reel_{a.platform}.mp4")

    before = probe(src)
    print(f"source : {before['size']/1e6:5.1f} MB  {before['br']/1e6:.2f} Mbps  {before['w']}x{before['h']}")

    subprocess.run(["ffmpeg","-v","error","-y","-i",src,
      "-c:v","libx264","-preset","slow","-crf",str(crf),
      "-maxrate",maxrate,"-bufsize",bufsize,
      "-profile:v","high","-level","4.2","-pix_fmt","yuv420p",
      # aq-mode 3 spends bits on the dark smooth areas that band; a touch of grain
      # dithers the gradients so they do not step
      "-x264-params","aq-mode=3:aq-strength=1.15:psy-rd=1.0,0.15:deblock=-1,-1:ref=5:bframes=3",
      "-vf","noise=alls=2:allf=t",
      "-c:a","aac","-b:a",f"{akbps}k","-ar","48000","-ac","2",
      "-movflags","+faststart", out], check=True)

    after = probe(out)
    print(f"master : {after['size']/1e6:5.1f} MB  {after['br']/1e6:.2f} Mbps  -> {out}")
    print()
    print("Getting it to the phone WITHOUT losing quality:")
    print("  WhatsApp  : attach > Document (not Photos/Videos). Normal send recompresses.")
    print("  Telegram  : send as File / uncheck 'compress'")
    print("  Drive     : upload, then download on the phone")
    print("  Cable     : Android File Transfer, or a USB-C stick")

if __name__ == "__main__":
    main()
