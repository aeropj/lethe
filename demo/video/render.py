#!/usr/bin/env python3
"""Render lethe-video.html to MP4, frame by frame, with headless Chrome.

  python3 demo/video/render.py              full film -> demo/video/out/lethe-demo.mp4
  python3 demo/video/render.py --stills 3 25 40   PNG stills at those seconds -> demo/video/out/still-*.png
"""
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
FPS = 30


def main():
    OUT.mkdir(exist_ok=True)
    stills = [float(x) for x in sys.argv[sys.argv.index("--stills") + 1:]] if "--stills" in sys.argv else None
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome")
        page = browser.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
        page.goto((HERE / "lethe-video.html").as_uri())
        page.evaluate("window.ready")
        if stills:
            for t in stills:
                page.evaluate(f"render({t})")
                page.screenshot(path=str(OUT / f"still-{t:05.1f}.png"))
            browser.close()
            return
        duration = page.evaluate("window.DURATION")
        silent = OUT / "lethe-demo-silent.mp4"
        ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS),
                               "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p",
                               "-movflags", "+faststart", str(silent)], stdin=subprocess.PIPE)
        frames = int(duration * FPS)
        for i in range(frames):
            page.evaluate(f"render({i / FPS})")
            ff.stdin.write(page.screenshot(type="jpeg", quality=95))
            if i % (FPS * 10) == 0:
                print(f"{i / FPS:5.1f}s / {duration}s", flush=True)
        ff.stdin.close()
        ff.wait()
        browser.close()
    print("wrote", silent)


if __name__ == "__main__":
    main()
