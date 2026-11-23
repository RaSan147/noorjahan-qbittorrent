"""Builds the README's images.

  python tools/readme_assets.py headings
      Writes .github/assets/headings/<slug>-light.svg and -dark.svg. The text is
      Inter SemiBold turned into outlines, so nothing depends on the viewer's fonts.
  python tools/readme_assets.py shots <folder of original screenshots>
      Makes the screenshot corners transparent (8 px Windows 11 radius at 200 %)
      and writes .github/assets/shots/.
  python tools/readme_assets.py banner
      Rounds .github/assets/banner.png to the radius the hero screenshot shows.

Needs Pillow, fontTools and uharfbuzz. Set INTER to a SemiBold .ttf if the default isn't found.
"""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / ".github" / "assets"

# Light value for GitHub's white page, dark value for its #0d1117 page.
# All taken from the theme's own palette in src/build.py.
COLOURS = {
    "teal":   ("#17695E", "#6FD0BE"),   # accentText
    "blue":   ("#2F5E92", "#8DB4E4"),   # downloading
    "green":  ("#2E7046", "#82CF99"),   # seeding
    "amber":  ("#B0821A", "#E2B653"),   # waiting
    "copper": ("#C0652A", "#EB9560"),   # icon copper
}

# slug, text, colour, size in px (GitHub's own h2 is 24 px, h3 is 20 px)
HEADINGS = [
    ("what-it-changes", "What it changes", "teal", 26),
    ("gallery", "Gallery", "blue", 26),
    ("install", "Install", "green", 26),
    ("desktop", "Desktop · Windows 10 & 11", "green", 20),
    ("web-ui", "Web UI", "green", 20),
    ("compatibility", "Compatibility", "amber", 26),
    ("credits", "Credits & License", "copper", 26),
]

SHOT_RADIUS = 16          # px in the 200 % screenshots
HERO_WIDTH = 3520         # width of the hero screenshot


def font_path():
    env = os.environ.get("INTER")
    if env:
        return Path(env)
    local = Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft/Windows/Fonts/Inter_24pt-SemiBold.ttf"
    return local if local.exists() else Path("C:/Windows/Fonts/Inter_24pt-SemiBold.ttf")


def headings():
    import uharfbuzz as hb
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.ttLib import TTFont

    path = font_path()
    data = path.read_bytes()
    font = TTFont(path)
    glyphs = font.getGlyphSet()
    order = font.getGlyphOrder()
    upm = font["head"].unitsPerEm
    asc, desc = font["hhea"].ascent, font["hhea"].descent
    hbfont = hb.Font(hb.Face(data))

    out = ASSETS / "headings"
    out.mkdir(parents=True, exist_ok=True)
    for slug, text, colour, size in HEADINGS:
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(hbfont, buf, {"kern": True, "liga": True})
        scale = size / upm
        pen = SVGPathPen(glyphs, ntos=lambda v: ("%.2f" % v).rstrip("0").rstrip("."))
        x = 0
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            name = order[info.codepoint]
            tp = TransformPen(pen, (scale, 0, 0, -scale, (x + pos.x_offset) * scale, asc * scale))
            glyphs[name].draw(tp)
            x += pos.x_advance
        width = round(x * scale + 1)
        height = round((asc - desc) * scale)
        light, dark = COLOURS[colour]
        for mode, fill in (("light", light), ("dark", dark)):
            svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
                   f'viewBox="0 0 {width} {height}" role="img" aria-label="{text.replace("&", "&amp;")}">'
                   f'<path fill="{fill}" d="{pen.getCommands()}"/></svg>\n')
            (out / f"{slug}-{mode}.svg").write_text(svg, encoding="utf-8")
        print(f"{slug}: {width}x{height}")


def rounded(im, radius):
    """Return im with transparent, anti-aliased round corners."""
    from PIL import Image, ImageChops, ImageDraw

    ss = 4
    im = im.convert("RGBA")
    w, h = im.size
    mask = Image.new("L", (w * ss, h * ss), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w * ss - 1, h * ss - 1), radius * ss, fill=255)
    mask = mask.resize((w, h), Image.LANCZOS)
    im.putalpha(ImageChops.multiply(im.getchannel("A"), mask))
    return im


def shots(src):
    from PIL import Image

    out = ASSETS / "shots"
    out.mkdir(parents=True, exist_ok=True)
    for f in sorted(Path(src).glob("*.png")):
        im = Image.open(f)
        # The window shots have white outside the rounded corner; cut it a hair
        # wider than the window's own radius so no white edge pixels survive.
        r = SHOT_RADIUS + 1
        rounded(im, r).save(out / f.name, optimize=True)
        print(f.name, im.size)


def banner():
    from PIL import Image

    p = ASSETS / "banner.png"
    im = Image.open(p)
    r = round((SHOT_RADIUS + 1) * im.width / HERO_WIDTH)
    rounded(im, r).save(p, optimize=True)
    print("banner radius", r)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "headings":
        headings()
    elif cmd == "shots" and len(sys.argv) > 2:
        shots(sys.argv[2])
    elif cmd == "banner":
        banner()
    else:
        sys.exit(__doc__)
