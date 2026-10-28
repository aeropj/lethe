"""Frame-by-frame screen recording for the Lethe demo film.

The real app runs in headless Chrome. Each frame is a fresh screenshot (or a reuse of the last one during a
hold), composed into a browser window on an ivory canvas at 2x, framed by a moving camera, with a synthetic
cursor and captions on top, then piped to ffmpeg. Long waits on the network are compressed and badged.
"""
import io
import math
import subprocess

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1920, 1080          # output
CW, CH = 3840, 2160        # composition canvas (2x)
BG = (240, 238, 230)
INK = (20, 20, 19)
CLAY = (181, 83, 47)
SERIF = "/System/Library/Fonts/Supplemental/Iowan Old Style.ttc"
SANS = "/System/Library/Fonts/SFNS.ttf"
MONO = "/System/Library/Fonts/SFNSMono.ttf"


def ease(x):
    x = max(0.0, min(1.0, x))
    return 4 * x * x * x if x < .5 else 1 - pow(-2 * x + 2, 3) / 2


# ---------------------------------------------------------------- the window frame
class Window:
    """A browser window on the ivory canvas. Content area receives the app screenshot."""

    def __init__(self, url="localhost:8787", content_px=(3200, 1668)):
        self.x, self.y, self.w = 200, 150, 3440
        self.bar = 92
        self.cw = self.w
        self.ch = round(content_px[1] * self.w / content_px[0])
        self.h = self.bar + self.ch
        self.scale = self.w / content_px[0]          # screenshot px -> canvas px
        base = Image.new("RGB", (CW, CH), BG)
        shadow = Image.new("L", (CW, CH), 0)
        ImageDraw.Draw(shadow).rounded_rectangle((self.x, self.y + 40, self.x + self.w, self.y + self.h + 40), 40, fill=110)
        shadow = shadow.filter(ImageFilter.GaussianBlur(60))
        base.paste(Image.new("RGB", (CW, CH), (150, 140, 120)), (0, 0), shadow)
        d = ImageDraw.Draw(base)
        d.rounded_rectangle((self.x, self.y, self.x + self.w, self.y + self.h), 40, fill=(250, 249, 245),
                            outline=(214, 210, 198), width=2)
        d.rounded_rectangle((self.x, self.y, self.x + self.w, self.y + self.bar + 40), 40, fill=(236, 234, 226))
        d.rectangle((self.x, self.y + self.bar, self.x + self.w, self.y + self.bar + 40), fill=(250, 249, 245))
        d.line((self.x, self.y + self.bar, self.x + self.w, self.y + self.bar), fill=(214, 210, 198), width=2)
        for i, c in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]):
            cx, cy = self.x + 50 + i * 44, self.y + self.bar // 2
            d.ellipse((cx - 13, cy - 13, cx + 13, cy + 13), fill=c)
        pill_w = 900
        px = self.x + (self.w - pill_w) // 2
        d.rounded_rectangle((px, self.y + 20, px + pill_w, self.y + self.bar - 20), 26, fill=(250, 249, 245))
        f = ImageFont.truetype(SANS, 30)
        d.text((px + pill_w // 2, self.y + self.bar // 2), "🔒  " + url if False else url, font=f, fill=(90, 90, 86),
               anchor="mm")
        self.base = base
        mask = Image.new("L", (self.cw, self.ch), 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, -40, self.cw, self.ch), 38, fill=255)
        self.mask = mask

    def compose(self, shot: Image.Image) -> Image.Image:
        img = self.base.copy()
        img.paste(shot.resize((self.cw, self.ch), Image.BICUBIC), (self.x, self.y + self.bar), self.mask)
        return img

    def to_canvas(self, px, py):
        """Page CSS px (viewport) -> canvas px, given screenshot device scale 2."""
        return self.x + px * 2 * self.scale, self.y + self.bar + py * 2 * self.scale


# ---------------------------------------------------------------- the reel
class Reel:
    def __init__(self, path, fps=30):
        self.fps = fps
        self.ff = subprocess.Popen(
            ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
             "-framerate", str(fps), "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "16",
             "-pix_fmt", "yuv420p", "-movflags", "+faststart", path], stdin=subprocess.PIPE)
        self.n = 0
        self.cam = (W / 2, H / 2, 1.0)      # centre x, centre y (output coords of the full canvas), zoom
        self.cursor = None                  # canvas px
        self.click_at = None                # (frame, x, y)
        self.caption = None                 # dict(text, eyebrow, start, end)
        self.badge = None                   # small corner badge text
        self.prev = None                    # last output frame, for crossfades
        self.fade_left, self.fade_total = 0, 0
        self.f_cap = ImageFont.truetype(SERIF, 44)
        self.f_eye = ImageFont.truetype(SANS, 21)
        self.f_badge = ImageFont.truetype(SANS, 24)

    # ---- camera
    def view(self, canvas: Image.Image) -> Image.Image:
        cx, cy, z = self.cam
        cw, ch = CW / z, CH / z
        x0 = min(max(cx * 2 - cw / 2, 0), CW - cw)
        y0 = min(max(cy * 2 - ch / 2, 0), CH - ch)
        return canvas.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch))

    def draw_cursor(self, canvas):
        if not self.cursor:
            return canvas
        x, y = self.cursor
        d = ImageDraw.Draw(canvas)
        if self.click_at and 0 <= self.n - self.click_at[0] < 14:
            k = (self.n - self.click_at[0]) / 14
            r = 20 + 70 * k
            d.ellipse((x - r, y - r, x + r, y + r), outline=(217, 119, 87), width=max(1, int(8 * (1 - k))))
        s = 2.2
        pts = [(0, 0), (0, 34), (9, 26), (15, 40), (21, 37), (15, 24), (27, 24)]
        poly = [(x + px * s, y + py * s) for px, py in pts]
        d.polygon([(px + 3, py + 4) for px, py in poly], fill=(0, 0, 0, 60))
        d.polygon(poly, fill=(20, 20, 19), outline=(255, 255, 255))
        d.line(poly + [poly[0]], fill=(255, 255, 255), width=4)
        return canvas

    # ---- overlays on the output frame
    def overlay(self, frame: Image.Image) -> Image.Image:
        cap = self.caption
        if cap:
            k = min(1, (self.n - cap["start"]) / 10)
            if cap.get("end") is not None:
                k = min(k, max(0, (cap["end"] - self.n) / 10))
            if k > 0:
                frame = frame.convert("RGBA")
                lay = Image.new("RGBA", frame.size, (0, 0, 0, 0))
                d = ImageDraw.Draw(lay)
                tw = d.textlength(cap["text"], font=self.f_cap)
                ew = d.textlength(cap.get("eyebrow", "").upper(), font=self.f_eye) * 1.1
                bw = max(tw, ew) + 96
                bh = 128 if cap.get("eyebrow") else 96
                x0, y1 = (W - bw) / 2, H - 56 + (1 - k) * 18
                y0 = y1 - bh
                d.rounded_rectangle((x0 + 4, y0 + 10, x0 + bw + 4, y1 + 14), 26, fill=(20, 20, 19, int(40 * k)))
                d.rounded_rectangle((x0, y0, x0 + bw, y1), 26, fill=(250, 249, 245, int(246 * k)),
                                    outline=(214, 210, 198, int(255 * k)), width=2)
                ty = y0 + 30
                if cap.get("eyebrow"):
                    ex = W / 2 - ew / 2
                    for ch in cap["eyebrow"].upper():
                        d.text((ex, ty), ch, font=self.f_eye, fill=(*CLAY, int(255 * k)))
                        ex += d.textlength(ch, font=self.f_eye) * 1.1
                    ty += 36
                d.text((W / 2, ty + (30 if not cap.get("eyebrow") else 0)), cap["text"], font=self.f_cap,
                       fill=(*INK, int(255 * k)), anchor="mt")
                frame = Image.alpha_composite(frame, lay).convert("RGB")
        if self.badge:
            d = ImageDraw.Draw(frame)
            tw = d.textlength(self.badge, font=self.f_badge)
            d.rounded_rectangle((W - tw - 90, 40, W - 40, 92), 26, fill=(20, 20, 19))
            d.text((W - 65 - tw / 2, 66), self.badge, font=self.f_badge, fill=(245, 244, 238), anchor="mm")
        return frame

    def emit(self, canvas: Image.Image | None = None, full: Image.Image | None = None):
        """Write one frame. Either a 2x canvas (camera + cursor apply) or a ready 1920x1080 image."""
        if full is None:
            full = self.view(self.draw_cursor(canvas.copy()))
        frame = self.overlay(full)
        if self.fade_left > 0:
            a = 1 - self.fade_left / self.fade_total
            frame = Image.blend(self.prev, frame, ease(a))
            self.fade_left -= 1
        self.ff.stdin.write(frame.tobytes())
        self.last_out = frame
        self.n += 1

    def crossfade(self, frames=14):
        self.prev = self.last_out
        self.fade_left = self.fade_total = frames

    def say(self, text, eyebrow=None, seconds=None):
        self.caption = {"text": text, "eyebrow": eyebrow, "start": self.n,
                        "end": None if seconds is None else self.n + int(seconds * self.fps)}

    def hush(self):
        if self.caption:
            self.caption["end"] = self.n + 10

    def close(self):
        self.ff.stdin.close()
        self.ff.wait()


# ---------------------------------------------------------------- driving the real app
class Director:
    def __init__(self, page, reel: Reel, window: Window):
        self.page, self.reel, self.win = page, reel, window
        self.canvas = None

    def shoot(self):
        png = self.page.screenshot(type="png")
        self.canvas = self.win.compose(Image.open(io.BytesIO(png)).convert("RGB"))
        return self.canvas

    def frame(self, fresh=True):
        if fresh or self.canvas is None:
            self.shoot()
        self.reel.emit(self.canvas)

    def hold(self, seconds, cam=None, fresh_every=0):
        """Hold on the page; optionally move the camera to cam=(cx, cy, zoom) with easing."""
        n = max(1, int(seconds * self.reel.fps))
        start = self.reel.cam
        for i in range(n):
            if cam:
                k = ease((i + 1) / n)
                self.reel.cam = tuple(a + (b - a) * k for a, b in zip(start, cam))
            self.frame(fresh=bool(fresh_every) and i % fresh_every == 0)

    def center_of(self, selector):
        box = self.page.locator(selector).first.bounding_box()
        return box["x"] + box["width"] / 2, box["y"] + box["height"] / 2

    def move_to(self, selector, seconds=0.7):
        tx, ty = self.win.to_canvas(*self.center_of(selector))
        sx, sy = self.reel.cursor or (tx + 400, ty + 300)
        n = max(1, int(seconds * self.reel.fps))
        for i in range(n):
            k = ease((i + 1) / n)
            arc = math.sin(k * math.pi) * 40
            self.reel.cursor = (sx + (tx - sx) * k, sy + (ty - sy) * k - arc)
            self.frame(fresh=False)

    def click(self, selector, seconds=0.7):
        self.page.locator(selector).first.scroll_into_view_if_needed()
        self.shoot()
        self.move_to(selector, seconds)
        self.reel.click_at = (self.reel.n, *self.reel.cursor)
        self.page.locator(selector).first.click()
        for _ in range(6):
            self.frame()

    def type(self, selector, text, cps=32):
        self.page.locator(selector).first.click()
        per = self.reel.fps / cps
        acc = 0.0
        for ch in text:
            self.page.keyboard.type(ch)
            acc += per
            while acc >= 1:
                self.frame(fresh=True)
                acc -= 1

    def scroll(self, y, seconds=1.2, selector=None):
        """Smoothly scroll the window (or a scrollable element) to y."""
        get = f"document.querySelector({selector!r}).scrollTop" if selector else "window.scrollY"
        start = self.page.evaluate(get)
        n = max(1, int(seconds * self.reel.fps))
        for i in range(n):
            v = start + (y - start) * ease((i + 1) / n)
            if selector:
                self.page.evaluate(f"document.querySelector({selector!r}).scrollTop = {v}")
            else:
                self.page.evaluate(f"window.scrollTo(0, {v})")
            self.frame()

    def scroll_to(self, selector, offset=120, seconds=1.2):
        y = self.page.evaluate(f"document.querySelector({selector!r}).getBoundingClientRect().top + window.scrollY")
        self.scroll(max(0, y - offset), seconds)

    def wait_for(self, js_condition, label="sped up", max_real=120, every=0.25):
        """Wait on the network, filming one frame per `every` real seconds (time compressed, badged)."""
        import time
        self.reel.badge = f"▸▸ {label}"
        t0 = time.time()
        while time.time() - t0 < max_real:
            self.frame()
            if self.page.evaluate(js_condition):
                break
            time.sleep(every)
        self.reel.badge = None
