"""Build Noorjahan Light / Dark .qbtheme bundles for qBittorrent 5.x.

    python src/build.py [path-to-rcc.exe]

Writes build/<variant>/ (readable folder theme, usable directly by pointing
qBittorrent at its config.json) and dist/Noorjahan <Variant>.qbtheme.
"""
import json, re, shutil, string, subprocess, sys
from pathlib import Path

import os
from icons import ICONS, UI
try:
    from icons import FIT
except ImportError:
    FIT = {}
if os.environ.get("NOORJAHAN_NOFIT"):
    FIT = {}  # measure raw glyphs (scratchpad fit.py)

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"

LIGHT = dict(
    variant="Light", bodyWeight="500",
    canvas="#ECEAE7", card="#FBFAF9", field="#F4F2EF", alt="#FBFAF9",
    line="#DEDAD5", line2="#EAE7E3", lineStrong="#C9C4BD", boxLine="#B5AFA7",
    text="#1B1A18", text2="#55514C", text3="#8A857E", disabled="#9C968F",
    accent="#1D786B", accentHover="#17695E", onAccent="#FFFFFF",
    prim="#1D786B", primHover="#17695E", onPrim="#FFFFFF", colsep="#D3CEC7", segOn="#FBFAF9", accentSoft="rgba(29, 120, 107, 26)", accentText="#17695E",
    selOff="rgba(27, 26, 24, 11)", disLine="#C9C4BD",
    accentLine="rgba(29, 120, 107, 90)",
    hover="rgba(27, 26, 24, 10)", sel="rgba(27, 26, 24, 20)",
    selStrong="rgba(27, 26, 24, 31)", selSolid="#E9E7E3",
    scroll="rgba(27, 26, 24, 46)", scrollHover="rgba(27, 26, 24, 82)",
    groove="rgba(27, 26, 24, 14)", chunk="#D3CEC7", chunkOff="#E3E0DB",
    err="#B33A27", errSoft="rgba(179, 58, 39, 22)",
    # icon roles
    i_n="#55514C", i_accent="#1D786B", i_dl="#3B6EA5", i_up="#3B8956", i_stall="#B0821A",
    i_check="#6956AC", i_err="#BF412E", i_ok="#3B8956", i_idle="#988F84",
    i_blue="#3B6EA5", i_violet="#6956AC", i_amber="#B0821A", i_copper="#C0652A",
    # transfer-list row text by state
    r_dl="#2F5E92", r_up="#2E7046", r_stalledUp="#57524A", r_stalledDl="#4F6F94",
    r_check="#5B4BA0", r_idle="#8A857E", r_queued="#55514C", r_err="#B33A27", r_meta="#2F5E92",
    p_have="#1D786B", p_partial="#8CC5BB", p_missing="#E6E3DF",
)

DARK = dict(
    variant="Dark", bodyWeight="500",
    canvas="#111110", card="#191918", field="#201F1E", alt="#191918",
    line="#2B2A28", line2="#222120", lineStrong="#3B3937", boxLine="#4F4C48",
    text="#F3F1ED", text2="#C3BEB6", text3="#938D85", disabled="#7E7972",
    accent="#52C3AF", accentHover="#6FD0BE", onAccent="#04201B",
    prim="#21786B", primHover="#288A7B", onPrim="#F2FBF9", colsep="#3A3836", segOn="#2C2B29", accentSoft="rgba(82, 195, 175, 30)", accentText="#6FD0BE",
    selOff="rgba(255, 255, 255, 10)", disLine="#3B3937",
    accentLine="rgba(82, 195, 175, 90)",
    hover="rgba(255, 255, 255, 9)", sel="rgba(255, 255, 255, 18)",
    selStrong="rgba(255, 255, 255, 28)", selSolid="#2A2928",
    scroll="rgba(255, 255, 255, 31)", scrollHover="rgba(255, 255, 255, 56)",
    groove="rgba(255, 255, 255, 12)", chunk="#3A3836", chunkOff="#272624",
    err="#F27A64", errSoft="rgba(242, 122, 100, 28)",
    i_n="#C3BEB6", i_accent="#52C3AF", i_dl="#7AA5DA", i_up="#76C98E", i_stall="#E2B653",
    i_check="#A796F0", i_err="#F0705A", i_ok="#76C98E", i_idle="#938D85",
    i_blue="#7AA5DA", i_violet="#A796F0", i_amber="#E2B653", i_copper="#EB9560",
    r_dl="#8DB4E4", r_up="#82CF99", r_stalledUp="#A7A197", r_stalledDl="#9FB6D3",
    r_check="#B4A6F2", r_idle="#938D85", r_queued="#C3BEB6", r_err="#F27A64", r_meta="#8DB4E4",
    p_have="#52C3AF", p_partial="#2C6E64", p_missing="#272624",
)


def role_colour(t, role):
    if "i_" + role in t:
        return t["i_" + role]
    return t[role]


def shape_svg(shape, attrs):
    p = shape.split()
    if p[0] == "c":
        return f'<circle cx="{p[1]}" cy="{p[2]}" r="{p[3]}" {attrs}/>'
    if p[0] == "r":
        return f'<rect x="{p[1]}" y="{p[2]}" width="{p[3]}" height="{p[4]}" rx="{p[5]}" {attrs}/>'
    return f'<path d="{shape}" {attrs}/>'



def rocket_svg(t):
    """Wide (3:2) and tightly cropped, climbing at 22 degrees: qBittorrent draws this
    button's icon in a 24x16 box, so a square icon would only get 16x16 of it."""
    ink, acc, fire = t["i_n"], t["i_accent"], t["i_copper"]
    art = '<g stroke="{fire}" stroke-width="2" stroke-linecap="round" fill="none"><path d="M1.5 8.5h4"/><path d="M0.5 15.5h4"/></g><path d="M7.6 9.6v4.8L1.8 12z" fill="{fire}"/><path d="M14 6.6 9.4 2.4H6.2l3 4.2zM14 17.4l-4.6 4.2H6.2l3-4.2z" fill="{acc}"/><path d="M7.4 6.4h17.2c4.6 0 8.4 2.4 10.6 5.6-2.2 3.2-6 5.6-10.6 5.6H7.4z" fill="{ink}"/><circle cx="24.2" cy="12" r="2.3" fill="{acc}"/><path d="M12.2 12h5.6" stroke="{acc}" stroke-width="1.6" stroke-linecap="round"/>'.format(ink=ink, acc=acc, fire=fire)
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="36" height="24" viewBox="0.00 2.90 34.20 22.80">'
            f'<g transform="rotate(-22 18 12)">{art}</g></svg>\n')


def turtle_svg(t):
    acc = t["i_accent"]
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="36" height="24" viewBox="1.4 6.6 22.5 15">'
            f'<g stroke="{acc}" stroke-width="1.9" stroke-linecap="round" fill="none">'
            '<path d="M6.6 15.2 5.6 18.6"/><path d="M9.2 15.2 9.8 18.6"/><path d="M14.8 15.2 13.9 18.6"/><path d="M17.4 15.2 18.2 18.6"/></g>'
            f'<g fill="none" stroke="{acc}" stroke-width="1.4"><path d="M19.2 13.8c.6-.3 1-.7 1.2-1.1" stroke-linecap="round"/><circle cx="21.2" cy="11.9" r="1.75"/></g>'
            f'<circle cx="21.8" cy="11.5" r=".3" fill="{acc}"/>'
            f'<path d="M4.4 15c0-4.1 3.4-7.2 7.6-7.2s7.6 3.1 7.6 7.2z" fill="{acc}" fill-opacity=".18" stroke="{acc}" stroke-width="1.4" stroke-linejoin="round"/>'
            f'<path d="M8.4 15 9.7 11.4h4.6l1.3 3.6M9.7 11.4 8.6 9.1M14.3 11.4l1.1-2.3" fill="none" stroke="{acc}" stroke-width="1" stroke-linejoin="round" stroke-opacity=".8"/>'
            f'<path d="M3.6 15h16.8M4.4 15.1 2.6 16.1" stroke="{acc}" stroke-width="1.4" stroke-linecap="round" fill="none"/></svg>\n')


def svg(colour, elements, size=24, fit=None, t=None):
    """fit=(scale, tx, ty): optical keyline fit. Stroke widths are divided by
    the scale so every icon keeps a true 1.5px line."""
    out = []
    k = 1 / fit[0] if fit else 1
    sw = f"{1.5 * k:.3f}"
    stroke = f'fill="none" stroke="{colour}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"'
    for el in elements:
        if isinstance(el, str):
            out.append(shape_svg(el, stroke))
        elif el[0] == "d":
            out.append(shape_svg(el[1], f'fill="{colour}" fill-opacity="0.16" stroke="none"'))
        elif el[0] == "d2":
            out.append(shape_svg(el[1], f'fill="{colour}" fill-opacity="0.38" stroke="none"'))
        elif el[0] == "f":
            out.append(shape_svg(el[1], f'fill="{colour}" stroke="none"'))
        elif el[0] == "dash":
            out.append(shape_svg(el[1], stroke + ' stroke-dasharray="2.6 2.4"'))
        elif el[0] == "p":   # filled-outline geometry from a modern set: ("p", d, transform)
            tf = f' transform="{el[2]}"' if el[2] else ""
            out.append(f'<path d="{el[1]}" fill="{colour}" stroke="none"{tf}/>')
        elif el[0] == "pu":  # its soft underlay: ("pu", d, transform)
            tf = f' transform="{el[2]}"' if el[2] else ""
            out.append(f'<path d="{el[1]}" fill="{colour}" fill-opacity="0.16" stroke="none"{tf}/>')
        elif el[0] == "t":
            st = stroke.replace(f'stroke-width="{sw}"', f'stroke-width="{el[2] * k:.3f}"')
            if len(el) > 3 and t:  # optional own colour role, e.g. a tick on a filled box
                st = st.replace(f'stroke="{colour}"', f'stroke="{role_colour(t, el[3])}"')
            out.append(shape_svg(el[1], st))
    body = "".join(out)
    if fit:
        body = f'<g transform="translate({fit[1]} {fit[2]}) scale({fit[0]})">{body}</g>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24">'
            + body + "</svg>\n")


def config(t):
    disabled = t["disabled"]
    palette = {
        "Palette.Window": t["canvas"], "Palette.WindowText": t["text"],
        "Palette.WindowTextDisabled": disabled,
        "Palette.Base": t["card"], "Palette.AlternateBase": t["alt"],
        "Palette.Text": t["text"], "Palette.TextDisabled": disabled,
        "Palette.ToolTipBase": t["card"], "Palette.ToolTipText": t["text"],
        "Palette.ToolTipTextDisabled": disabled,
        "Palette.BrightText": t["text"], "Palette.BrightTextDisabled": disabled,
        "Palette.Highlight": t["selSolid"], "Palette.HighlightedText": t["text"],
        "Palette.HighlightedTextDisabled": disabled,
        "Palette.Button": t["field"], "Palette.ButtonText": t["text"],
        "Palette.ButtonTextDisabled": disabled,
        "Palette.Link": t["accent"], "Palette.LinkVisited": t["i_check"],
        "Palette.Light": t["card"], "Palette.Midlight": t["field"],
        "Palette.Mid": t["line"], "Palette.Dark": t["lineStrong"], "Palette.Shadow": t["line"],
    }
    states = {
        "Downloading": "r_dl", "ForcedDownloading": "r_dl",
        "DownloadingMetadata": "r_meta", "ForcedDownloadingMetadata": "r_meta",
        "StalledDownloading": "r_stalledDl", "QueuedDownloading": "r_queued",
        "StoppedDownloading": "r_idle",
        "Uploading": "r_up", "ForcedUploading": "r_up",
        "StalledUploading": "r_stalledUp", "QueuedUploading": "r_queued",
        "StoppedUploading": "r_idle",
        "CheckingDownloading": "r_check", "CheckingUploading": "r_check",
        "CheckingResumeData": "r_check", "Moving": "r_check",
        "Error": "r_err", "MissingFiles": "r_err",
    }
    colours = {f"TransferList.{k}": t[v] for k, v in states.items()}
    colours.update({
        "ProgressBar": t["i_dl"],
        "PiecesBar.Border": t["p_missing"], "PiecesBar.Piece": t["p_have"],
        "PiecesBar.PartialPiece": t["p_partial"], "PiecesBar.MissingPiece": t["p_missing"],
        "Log.TimeStamp": t["text3"], "Log.Normal": t["text"], "Log.Info": t["i_dl"],
        "Log.Warning": t["i_stall"], "Log.Critical": t["i_err"], "Log.BannedPeer": t["i_err"],
        "RSS.UnreadArticle": t["text"], "RSS.ReadArticle": t["text3"],
    })
    # Palette.* is only read from "colors"; the rest is read from whichever section
    # matches the palette's lightness. Each bundle is single-mode, so both get the same.
    return {"colors": {**palette, **colours}, "colors.dark": dict(colours)}


PILL_ICONS = [
    "help-about", "trackers", "peers", "network-server", "directory", "chart-line",
    "list-add", "task-complete", "view-refresh", "downloading",
    "edit-find", "task-reject", "plugins",
]


def build(t, rcc):
    name = t["variant"].lower()
    out = ROOT / "build" / name
    if out.exists():
        shutil.rmtree(out)
    (out / "icons" / "dark").mkdir(parents=True)
    (out / "ui").mkdir()

    qss = string.Template((SRC / "stylesheet.qss.tmpl").read_text(encoding="utf-8")).substitute(t)
    left = re.findall(r"\$[A-Za-z]+", qss)
    if left:
        sys.exit(f"unresolved tokens: {left}")
    (out / "stylesheet.qss").write_text(qss, encoding="utf-8")
    (out / "config.json").write_text(json.dumps(config(t), indent=4) + "\n", encoding="utf-8")

    for icon, (role, els) in ICONS.items():
        data = svg(role_colour(t, role), els, fit=FIT.get(icon))
        (out / "icons" / f"{icon}.svg").write_text(data, encoding="utf-8")
        (out / "icons" / "dark" / f"{icon}.svg").write_text(data, encoding="utf-8")
    # status-bar speed switch: a rocket while unlimited, the turtle when the
    # alternative limits are on (static here; Qt icons can't animate)
    for icon, data in (("slow_off", rocket_svg(t)), ("slow", turtle_svg(t))):
        (out / "icons" / f"{icon}.svg").write_text(data, encoding="utf-8")
        (out / "icons" / "dark" / f"{icon}.svg").write_text(data, encoding="utf-8")
    # details-tab pill icons: the same art on a canvas 6 units (4px at 16px) wider
    # on the right. Qt fixes the icon-to-text gap at 4px; this doubles it.
    for icon in PILL_ICONS:
        role, els = ICONS[icon]
        data = svg(role_colour(t, role), els, fit=FIT.get(icon))
        data = data.replace('width="24" height="24" viewBox="0 0 24 24"', 'width="30" height="24" viewBox="0 0 30 24"', 1)
        (out / "ui" / f"pill-{icon}.svg").write_text(data, encoding="utf-8")
    for icon, (role, els, size) in UI.items():
        (out / "ui" / f"{icon}.svg").write_text(svg(role_colour(t, role), els, size, t=t), encoding="utf-8")
    # status bar footer card, drawn as a 9-slice border image (the status bar
    # ignores margins): 8px clear left/right/below, radius 12 (matching all cards).
    # Slices: top 12, sides 21, bottom 20.
    (out / "ui" / "statusbar-card.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="40" viewBox="0 0 48 40">'
        f'<rect x="8.5" y="0.5" width="31" height="31" rx="12" fill="{t['card']}" stroke="{t['line']}"/></svg>',
        encoding="utf-8")
    # status bar item hover / pressed pill, drawn as a border image the exact
    # height of the item (30 = 4 + 14 text + 12) so nothing is stretched
    # vertically: a 22px pill on top, the 8px below it clear (that strip lifts
    # the items onto the card's centre line), and 14px clear on the right (8px
    # outside the card + 6px inner clearance so the last pill never overflows
    # the 12px card corner when maximized and Qt hides QSizeGrip)
    def paint(c):
        c = c.strip()
        if c.startswith("rgba"):
            r, g, b, a = [int(v) for v in c[5:-1].split(",")]
            return f"#{r:02X}{g:02X}{b:02X}", f"{a / 255:.3f}"
        return c, "1"
    for state, (fill, line) in {"hover": ("field", "line"), "press": ("accentSoft", "accentLine")}.items():
        f, fo = paint(t[fill]); l, lo = paint(t[line])
        (out / "ui" / f"status-{state}.svg").write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" width="54" height="30" viewBox="0 0 54 30">'
            f'<rect x="0.5" y="0.5" width="39" height="21" rx="7" fill="{f}" fill-opacity="{fo}" '
            f'stroke="{l}" stroke-opacity="{lo}"/></svg>', encoding="utf-8")

    files = sorted(p.relative_to(out).as_posix() for p in out.rglob("*") if p.is_file())
    qrc = ['<!DOCTYPE RCC><RCC version="1.0">', '<qresource prefix="/">']
    qrc += [f"    <file>{f}</file>" for f in files]
    qrc += ["</qresource>", "</RCC>"]
    (out / "theme.qrc").write_text("\n".join(qrc) + "\n", encoding="utf-8")

    dist = ROOT / "dist" / f"Noorjahan {t['variant']}.qbtheme"
    dist.parent.mkdir(exist_ok=True)
    subprocess.run([rcc, "--binary", "--compress-algo", "zlib", "-o", str(dist), "theme.qrc"],
                   cwd=out, check=True)
    print(f"{dist.name}: {len(files)} files, {dist.stat().st_size // 1024} KB")


def svg_body(colour, elements):
    return svg(colour, elements).split(">", 1)[1].rsplit("</svg>", 1)[0]


def webui_icons():
    """Overwrite the WebUI's icons with Noorjahan ones of the same name. One file per
    icon carries both palettes; the WebUI sets `color-scheme` on the page, which SVG
    images follow through prefers-color-scheme."""
    images = ROOT / "webui" / "private" / "images"
    if not images.is_dir():
        return
    n = 0
    for icon, (role, els) in ICONS.items():
        target = images / f"{icon}.svg"
        if not target.exists():
            continue
        target.write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">'
            "<style>.d{display:none}@media (prefers-color-scheme:dark){.l{display:none}.d{display:inline}}</style>"
            f'<g class="l">{svg_body(role_colour(LIGHT, role), els)}</g>'
            f'<g class="d">{svg_body(role_colour(DARK, role), els)}</g></svg>\n', encoding="utf-8")
        n += 1
    # sidebar / panel chevron
    chevron = ["m7 9.5 5 5 5-5"]
    (images / "collapse.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">'
        "<style>.d{display:none}@media (prefers-color-scheme:dark){.l{display:none}.d{display:inline}}</style>"
        f'<g class="l">{svg_body(LIGHT["text3"], chevron)}</g>'
        f'<g class="d">{svg_body(DARK["text2"], chevron)}</g></svg>' + chr(10), encoding="utf-8")
    print(f"webui: {n} icons")

    # stylesheet = Modern Default base + Noorjahan layer (both kept in src/)
    css = images.parent / "css"
    base = (SRC / "webui-style.base.css").read_text(encoding="utf-8")
    layer = (SRC / "webui-noorjahan.css").read_text(encoding="utf-8")
    (css / "style.css").write_text(base.rstrip() + chr(10) + layer, encoding="utf-8")
    fonts = [f for f in (ROOT / "fonts").glob("*.woff2")]
    for d in (css / "fonts", ROOT / "webui" / "public" / "css" / "fonts"):
        d.mkdir(exist_ok=True)
        for f in fonts:
            shutil.copy2(f, d / f.name)

    # transfer list rows are 32px (CSS above); the virtual list must agree
    js = images.parent / "scripts" / "dynamicTable.js"
    src = js.read_text(encoding="utf-8")
    old = 'this.rowHeight = (clientData.get("display_density") === "compact") ? 20 : 25;'
    new = 'this.rowHeight = (clientData.get("display_density") === "compact") ? 20 : 32;'
    if old in src:
        js.write_text(src.replace(old, new), encoding="utf-8")
    assert new in js.read_text(encoding="utf-8"), "TorrentsTable rowHeight patch failed"


if __name__ == "__main__":
    rcc = sys.argv[1] if len(sys.argv) > 1 else "rcc"
    for theme in (LIGHT, DARK):
        build(theme, rcc)
    webui_icons()
