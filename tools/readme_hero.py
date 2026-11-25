"""Records the README's animated hero from the website's live replica.

  python tools/readme_hero.py [url]        (default http://localhost:8787/)

Run the website first (wrangler dev on :8787). It takes over the hero replica
("Try it yourself", so no tour cursor), records the download simulation for
about 5 s in Light, switches to Dark and records about 5 s more. The switch and
the loop back to Light are smooth crossfades. Output: .github/assets/hero/main.webp,
lossless and looping. Everything behind the window is made transparent before
capturing, so the rounded corners are clean on any page colour.

Needs Pillow and Playwright (python -m playwright install chromium).
"""
import sys
import tempfile
import time
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parent))
from readme_assets import ASSETS  # noqa: E402

URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8787/"
HOLD = 5.2          # seconds per scheme
SCALE = 1.25        # 1510 px replica -> 1888 px frames
FADE_STEPS = 4      # frames per crossfade
FADE_MS = 110       # per crossfade frame

# Make every ancestor of the window transparent so only the window is captured.
CLEAR_BEHIND = """() => {
  const q = document.querySelector('#heroLive .qbt');
  for (let e = q.parentElement; e; e = e.parentElement) {
    e.style.setProperty('background', 'transparent', 'important');
    e.style.setProperty('box-shadow', 'none', 'important');
    e.style.setProperty('border-color', 'transparent', 'important');
  }
  document.documentElement.style.setProperty('background', 'transparent', 'important');
}"""


def shoot(win, folder, frames):
    path = folder / f"{len(frames):03d}.png"
    win.screenshot(path=path, omit_background=True, animations="allow")
    frames.append(path)


def hold(win, folder, frames, stamps, seconds):
    t0 = time.time()
    while time.time() - t0 < seconds:
        shoot(win, folder, frames)
        stamps.append(time.time())


def record(browser, folder):
    pg = browser.new_page(viewport={"width": 2560, "height": 1310}, device_scale_factor=SCALE)
    pg.goto(URL, wait_until="networkidle")
    pg.wait_for_timeout(1500)
    pg.get_by_role("button", name="Light", exact=True).first.click()
    pg.get_by_role("button", name="Try it yourself").click()
    pg.mouse.move(5, 5)
    pg.wait_for_timeout(5000)  # let speeds settle after the takeover
    pg.evaluate(CLEAR_BEHIND)
    win = pg.locator("#heroLive .qbt").first
    frames, stamps = [], []
    hold(win, folder, frames, stamps, HOLD)
    switch_at = len(frames)
    pg.get_by_role("button", name="Dark", exact=True).first.click()
    pg.mouse.move(5, 5)
    pg.evaluate(CLEAR_BEHIND)
    pg.wait_for_timeout(250)
    hold(win, folder, frames, stamps, HOLD)
    pg.close()
    return frames, stamps, switch_at


def fade(a, b):
    return [Image.blend(a, b, k / (FADE_STEPS + 1)) for k in range(1, FADE_STEPS + 1)]


def encode(frames, stamps, switch_at, out):
    images = [Image.open(f).convert("RGBA") for f in frames]
    gaps = [int((b - a) * 1000) for a, b in zip(stamps, stamps[1:])] + [320]
    seq, dur = [], []
    for i, im in enumerate(images):
        if i == switch_at:  # Light -> Dark
            for f in fade(images[i - 1], im):
                seq.append(f); dur.append(FADE_MS)
        seq.append(im)
        dur.append(gaps[i] if i != switch_at - 1 else 320)
    for f in fade(images[-1], images[0]):  # Dark -> Light, back to the start
        seq.append(f); dur.append(FADE_MS)
    seq[0].save(out, save_all=True, append_images=seq[1:], duration=dur, loop=0,
                lossless=True, quality=80, method=6, minimize_size=True)
    print(out.name, seq[0].size, len(seq), "frames", f"{sum(dur) / 1000:.1f} s",
          f"{out.stat().st_size / 1e6:.2f} MB")


if __name__ == "__main__":
    out_dir = ASSETS / "hero"
    out_dir.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p, tempfile.TemporaryDirectory() as tmp:
        browser = p.chromium.launch()
        frames, stamps, switch_at = record(browser, Path(tmp))
        encode(frames, stamps, switch_at, out_dir / "main.webp")
        browser.close()
