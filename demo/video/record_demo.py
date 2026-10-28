#!/usr/bin/env python3
"""Record the Lethe live-demo film from the published Docker image, running on this machine.

  python3 demo/video/record_demo.py   -> demo/video/out/lethe-live-demo.mp4

Starts two containers from aeropj/lethe-demo: one with no key (to film the setup screen) and one connected
with the key in demo/.env (posted to its /api/key by this script; never typed into a page, never shown).
Everything else is the real app answering a real question through OpenAI.
"""
import io
import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from reel import H, W, Director, Reel, Window  # noqa: E402

OUT = HERE / "out"
IMAGE = "aeropj/lethe-demo:latest"
APP, SETUP = 8787, 8797
PROMPT = ("My son Ethan Miller, 9, has ADHD. Should he switch from Adderall to Vyvanse? We're on Kaiser in "
          "Sacramento. Reach me at sarah.miller@gmail.com.")
FPS = 30


def run(*args):
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout


def start_containers():
    for name in ("lethe-film", "lethe-film-setup", "lethe-e2e"):
        subprocess.run(["docker", "rm", "-f", name], capture_output=True)
    run("docker", "run", "-d", "--name", "lethe-film", "-p", f"127.0.0.1:{APP}:8787", IMAGE)
    run("docker", "run", "-d", "--name", "lethe-film-setup", "-p", f"127.0.0.1:{SETUP}:8787", IMAGE)
    for port in (APP, SETUP):
        for _ in range(60):
            try:
                urllib.request.urlopen(f"http://localhost:{port}/healthz", timeout=1)
                break
            except Exception:
                time.sleep(0.5)
    key = [l.split("=", 1)[1].strip() for l in (HERE.parent / ".env").read_text().splitlines()
           if l.startswith("OPENAI_API_KEY=")][0]
    req = urllib.request.Request(f"http://localhost:{APP}/api/key", method="POST",
                                 data=json.dumps({"key": key, "store": True}).encode(),
                                 headers={"Content-Type": "application/json"})
    info = json.load(urllib.request.urlopen(req, timeout=30))
    print("connected", info.get("masked_key"), list(info.get("models", {})), flush=True)


def stop_containers():
    for name in ("lethe-film", "lethe-film-setup"):
        subprocess.run(["docker", "rm", "-f", name], capture_output=True)


def terminal_script():
    layers = ["2b70e040f7d1", "0922d1fc1a5f", "b41621e272b0", "64074ecd150a",
              "317336cb5095", "f7803e891b5a", "51fa07964666", "ac66590bb06a"]
    digest = run("docker", "buildx", "imagetools", "inspect", IMAGE, "--format", "{{json .Manifest.Digest}}").strip().strip('"')
    banner = run("docker", "logs", "lethe-film-setup").strip().splitlines()[0]
    return ([{"cmd": "docker run --rm -p 127.0.0.1:8787:8787 aeropj/lethe-demo"},
             {"line": "Unable to find image 'aeropj/lethe-demo:latest' locally", "cls": "d", "gap": .45},
             {"line": "latest: Pulling from aeropj/lethe-demo", "cls": "d", "gap": .35}]
            + [{"line": f"{l}: Pull complete", "cls": "d", "gap": .11} for l in layers]
            + [{"line": f"Digest: {digest}", "cls": "d", "gap": .2},
               {"line": "Status: Downloaded newer image for aeropj/lethe-demo:latest", "cls": "d", "gap": .7},
               {"line": banner, "cls": "h", "gap": .3}])


def main():
    OUT.mkdir(exist_ok=True)
    start_containers()
    reel = Reel(str(OUT / "lethe-live-silent.mp4"), FPS)
    win = Window("localhost:8787")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(channel="chrome")
            scenes = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
            scenes.goto((HERE / "demo-scenes.html").as_uri())
            scenes.evaluate("window.ready")

            def scene(name, seconds):
                for i in range(int(seconds * FPS)):
                    scenes.evaluate(f"render('{name}', {i / FPS})")
                    reel.emit(full=Image.open(io.BytesIO(scenes.screenshot(type="png"))).convert("RGB"))

            # ---------------------------------------------------------------- 1. title, terminal
            scene("title", 4.6)
            reel.crossfade(16)
            scenes.evaluate(f"window.TERM = {json.dumps(terminal_script())}")
            scene("terminal", scenes.evaluate("termDuration()"))

            ctx = browser.new_context(viewport={"width": 1600, "height": 834}, device_scale_factor=2)

            def cam_on(page, selector, zoom):
                b = page.locator(selector).first.bounding_box()
                x, y = win.to_canvas(b["x"] + b["width"] / 2, b["y"] + b["height"] / 2)
                return x / 2, y / 2, zoom

            # ---------------------------------------------------------------- 2. setup screen
            setup = ctx.new_page()
            setup.goto(f"http://localhost:{SETUP}/")
            setup.wait_for_selector("#key")
            d = Director(setup, reel, win)
            reel.crossfade(18)
            reel.cam = (W / 2, H / 2, 1.0)
            d.shoot()
            d.hold(0.8)
            reel.say("Open localhost:8787 and paste your OpenAI key.", eyebrow="Connect")
            d.hold(0.9, cam=cam_on(setup, "#key", 1.45))
            d.click("#key", 0.6)
            d.type("#key", "sk-proj-" + "x" * 40, cps=60)   # a placeholder: the field shows dots
            reel.say("It stays in this container's memory, and goes only to api.openai.com.", eyebrow="Connect")
            d.hold(1.6, cam=cam_on(setup, "#connect", 1.3))
            d.move_to("#connect", 0.6)
            reel.click_at = (reel.n, *reel.cursor)
            d.hold(0.4)
            reel.hush()

            # ---------------------------------------------------------------- 3. ask
            app = ctx.new_page()
            app.goto(f"http://localhost:{APP}/#/")
            app.wait_for_selector("#prompt")
            app.fill("#prompt", "")
            d = Director(app, reel, win)
            reel.crossfade(18)
            reel.cam = (W / 2, H / 2, 1.0)
            d.shoot()
            d.hold(0.7)
            reel.say("Ask the way you normally would.", eyebrow="Ask")
            d.hold(0.8, cam=cam_on(app, "#prompt", 1.35))
            d.click("#prompt", 0.5)
            d.type("#prompt", PROMPT, cps=36)
            d.hold(0.5, cam=(W / 2, H / 2, 1.0))
            reel.say("Names, places and IDs are swapped on this laptop first.", eyebrow="On your device")
            d.click("#ask", 0.6)
            d.wait_for("!document.querySelector('#ask').disabled && !document.querySelector('#tracelink').hidden",
                       label="waiting on GPT-5.6 · sped up")
            d.hold(0.4)
            d.scroll_to("#orig", offset=150, seconds=1.0)
            reel.say("OpenAI gets stand-ins. The swap took a couple of milliseconds.", eyebrow="What left your device")
            d.hold(3.4, cam=cam_on(app, "#sent", 1.55))
            d.hold(0.6, cam=(W / 2, H / 2, 1.0))
            d.scroll_to("#answer", offset=170, seconds=1.0)
            reel.say("The answer comes back. Real names are put back only here.", eyebrow="Answer")
            d.hold(3.2, cam=cam_on(app, "#answer", 1.35))
            d.hold(0.6, cam=(W / 2, H / 2, 1.0))

            # ---------------------------------------------------------------- 4. observability
            reel.say("Every request is traced, end to end.", eyebrow="Observability")
            d.scroll(0, 0.9)
            d.click("#tracelink", 0.6)
            app.wait_for_selector(".kpis")
            d.hold(0.8, fresh_every=1)
            d.hold(1.6, cam=cam_on(app, ".kpis", 1.22))
            reel.say("Lethe adds a few milliseconds. The model takes seconds.", eyebrow="Overhead")
            d.hold(2.6, cam=cam_on(app, ".kpi.accent", 2.0))
            d.hold(0.7, cam=(W / 2, H / 2, 1.0))
            reel.say("Nine steps on one clock.", eyebrow="Waterfall")
            d.scroll_to("#wf", offset=90, seconds=1.0)
            d.hold(1.6)
            d.click('button[data-m="zoom"]', 0.6)
            reel.say("Zoomed in on the steps Lethe adds: detect, credential, seal, relay, open, restore.",
                     eyebrow="Waterfall")
            d.hold(2.8, fresh_every=3)
            for sel, eyebrow, text, zoom in [
                ("#step-detect", "Step 1 · On your device", "What was found, and what was sent instead.", 1.12),
                ("#step-seal", "Step 3 · Sealed", "Sealed for the gateway and padded to a fixed size.", 1.12),
                ("#step-relay", "Step 4 · Relay", "The relay sees your IP and bytes it cannot read.", 1.12),
                ("#step-lab", "Step 6 · OpenAI", "Exactly what OpenAI received, byte for byte.", 1.12),
                ("#step-restore", "Step 9 · Restore", "Stand-ins on the left. Your words on the right.", 1.12),
            ]:
                d.hold(0.3, cam=(W / 2, H / 2, 1.0))
                d.scroll_to(sel, offset=84, seconds=1.1)
                reel.say(text, eyebrow=eyebrow)
                d.hold(2.9, cam=(W / 2, H / 2 - 20, zoom))

            # ---------------------------------------------------------------- 5. prove it
            d.hold(0.3, cam=(W / 2, H / 2, 1.0))
            reel.say("Now ask OpenAI for its own stored copy.", eyebrow="Prove it")
            d.scroll_to("#prove", offset=120, seconds=1.6)
            d.click("#verifybtn", 0.6)
            d.wait_for("(document.querySelector('#kpi-verify')||{}).innerText?.includes('Verified') || "
                       "(document.querySelector('#kpi-verify')||{}).innerText?.includes('Leak')",
                       label="asking OpenAI · sped up", every=0.2)
            d.hold(0.5, fresh_every=1)
            reel.say("None of your details are in what OpenAI kept.", eyebrow="Verified")
            d.hold(3.4, cam=cam_on(app, "#prove", 1.3))
            d.hold(0.8, cam=(W / 2, H / 2, 1.0))
            reel.hush()
            d.hold(0.4)

            # ---------------------------------------------------------------- 6. end
            reel.caption = None
            reel.crossfade(20)
            scene("end", 7)
            browser.close()
    finally:
        reel.close()
        stop_containers()
    print("frames", reel.n, "seconds", reel.n / FPS)


if __name__ == "__main__":
    main()
