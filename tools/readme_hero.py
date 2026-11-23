"""Records the README's animated hero from the website's live replica.

  python tools/readme_hero.py [url]        (default http://localhost:8787/)

Run the website first (wrangler dev on :8787). For Light and Dark it takes over
the hero replica ("Try it yourself", so no tour cursor), records ~10 s of the
download simulation and writes .github/assets/hero/main-light.webp and
main-dark.webp: lossless, looping, with a short crossfade back to the first
frame and the window's 9 px corners made transparent.

Needs Pillow and Playwright (python -m playwright install chromium).
"""
import sys
import tempfile
import time
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parent))
from readme_assets import ASSETS, rounded  # noqa: E402

URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8787/"
SECONDS = 10.5
SCALE = 1.25        # 1510 px replica -> 1888 px frames
RADIUS = 9          # the replica window's border-radius in CSS px


def record(browser, scheme, folder):
    pg = browser.new_page(viewport={"width": 2560, "height": 1310}, device_scale_factor=SCALE)
    pg.goto(URL, wait_until="networkidle")
    pg.wait_for_timeout(1500)
    pg.get_by_role("button", name=scheme, exact=True).first.click()
    pg.wait_for_timeout(600)
    pg.get_by_role("button", name="Try it yourself").click()
    pg.mouse.move(5, 5)
    pg.wait_for_timeout(5000)  # let speeds settle after the takeover
    win = pg.locator("#heroLive .qbt").first
    frames, stamps, t0 = [], [], time.time()
    while time.time() - t0 < SECONDS:
        path = folder / f"{len(frames):03d}.png"
        win.screenshot(path=path, animations="allow")
        frames.append(path)
        stamps.append(time.time() - t0)
    pg.close()
    return frames, stamps


def encode(frames, stamps, out):
    images = [Image.open(f).convert("RGB") for f in frames]
    durations = [int((b - a) * 1000) for a, b in zip(stamps, stamps[1:])] + [320]
    last, first = images[-1], images[0]
    for k in range(1, 5):  # crossfade so the loop restart doesn't jump
        images.append(Image.blend(last, first, k / 5))
        durations.append(110)
    r = round(RADIUS * SCALE)
    images = [rounded(im, r) for im in images]
    images[0].save(out, save_all=True, append_images=images[1:], duration=durations,
                   loop=0, lossless=True, quality=80, method=6, minimize_size=True)
    print(out.name, images[0].size, f"{out.stat().st_size / 1e6:.2f} MB")


if __name__ == "__main__":
    out_dir = ASSETS / "hero"
    out_dir.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p, tempfile.TemporaryDirectory() as tmp:
        browser = p.chromium.launch()
        for scheme in ("Light", "Dark"):
            folder = Path(tmp) / scheme
            folder.mkdir()
            frames, stamps = record(browser, scheme, folder)
            encode(frames, stamps, out_dir / f"main-{scheme.lower()}.webp")
        browser.close()
