"""Stamp a Noorjahan Web UI folder with a release version.

    python stamp-webui-version.py <Noorjahan-WebUI folder> <version, e.g. 1.2.5>

1. Sets NJ_VERSION in private/scripts/nj-update.js (what the update notice and
   the updater scripts compare against).
2. Appends "_nj<version with _ for .>" (e.g. _nj1_2_5) to every ${CACHEID}
   in the .html and .js files.
   qBittorrent fills ${CACHEID} with an id that only changes when qBittorrent
   restarts, and browsers keep CSS/JS for 12 hours. Without a per-release
   suffix, a browser keeps using the old CSS/JS after the folder is updated.

Run it for every release, before zipping. Running it twice is harmless.
"""
import pathlib
import re
import sys

if len(sys.argv) != 3 or not re.fullmatch(r"\d{1,4}(\.\d{1,4}){0,3}", sys.argv[2]):
    sys.exit(__doc__)
root = pathlib.Path(sys.argv[1])
ver = sys.argv[2]
if not (root / "private").is_dir() or not (root / "public").is_dir():
    sys.exit(f"{root} is not a Web UI folder (no public/ and private/)")

nj = root / "private" / "scripts" / "nj-update.js"
src = nj.read_bytes()
new, n = re.subn(rb'const NJ_VERSION = "[0-9.]+";', f'const NJ_VERSION = "{ver}";'.encode(), src)
if n != 1:
    sys.exit("NJ_VERSION not found exactly once in nj-update.js")
nj.write_bytes(new)

# No dots in the suffix: MochaUI picks a file's type from the URL's last ".xxx"
# (/\.\w+$/), so "Tabs.css?v=id-nj1.2.5" would look like a ".5" file and the
# dialog that needs it would fail to open. Letters, digits and "_" only.
token = re.compile(rb"\$\{CACHEID\}(?:[-_]nj[0-9._]+)?")
stamp = b"${CACHEID}_nj" + ver.replace(".", "_").encode()
files = changed = hits = 0
for f in sorted(root.rglob("*")):
    if f.suffix.lower() not in (".html", ".js") or not f.is_file():
        continue
    files += 1
    data = f.read_bytes()
    out, k = token.subn(stamp, data)
    if k:
        hits += k
        if out != data:
            f.write_bytes(out)
            changed += 1
print(f"NJ_VERSION = {ver}; {hits} cache ids stamped in {changed} changed files ({files} scanned)")
