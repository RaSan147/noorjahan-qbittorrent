#!/usr/bin/env bash
# Noorjahan Web UI updater for Linux / macOS (qBittorrent or qbittorrent-nox).
#
#   1. Finds the alternative Web UI folder qBittorrent uses (or takes --path).
#   2. Asks GitHub for the newest release and compares it with the installed version.
#   3. Downloads Noorjahan-WebUI.zip and SHA256SUMS.txt and checks the zip's SHA-256.
#   4. Keeps the old folder as "<folder>.backup-<date>" and puts the new one in its place.
#      If anything fails, the old folder is put back.
#   Then reload the Web UI page in your browser. qBittorrent does not need a restart.
#
# Usage: update-webui.sh [--path DIR] [--check] [--force] [--yes] [--keep-backups N]
# Needs: curl, unzip, sha256sum (or shasum), and either python3 or jq.

set -euo pipefail

REPO="chiefhamim/noorjahan-qbittorrent"
API="${NJ_TEST_API:-https://api.github.com/repos/$REPO/releases/latest}"
ASSET="Noorjahan-WebUI.zip"
SUMS="SHA256SUMS.txt"
TAG_RE='^v?[0-9]{1,4}(\.[0-9]{1,4}){0,3}$'

path=""; check=0; force=0; yes=0; keep=3
while [ $# -gt 0 ]; do
    case "$1" in
        --path) path="${2:-}"; shift 2 ;;
        --path=*) path="${1#*=}"; shift ;;
        --check) check=1; shift ;;
        --force) force=1; shift ;;
        --yes|-y) yes=1; shift ;;
        --keep-backups) keep="${2:-3}"; shift 2 ;;
        -h|--help) sed -n '2,13p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
        *) echo "Unknown option: $1 (see --help)" >&2; exit 2 ;;
    esac
done
case "$keep" in ''|*[!0-9]*) echo "--keep-backups needs a number" >&2; exit 2 ;; esac

say()  { printf '  %s\n' "$*"; }
fail() { printf '  [x] %s\n\n' "$*" >&2; exit 1; }

for tool in curl unzip; do command -v "$tool" >/dev/null 2>&1 || fail "'$tool' is not installed."; done
if command -v sha256sum >/dev/null 2>&1; then sha() { sha256sum "$1" | cut -d' ' -f1; }
elif command -v shasum >/dev/null 2>&1; then sha() { shasum -a 256 "$1" | cut -d' ' -f1; }
else fail "Neither 'sha256sum' nor 'shasum' is installed."; fi
if command -v python3 >/dev/null 2>&1; then json=python3
elif command -v jq >/dev/null 2>&1; then json=jq
else fail "Needs python3 or jq to read GitHub's answer."; fi

# read one value from GitHub's JSON: tag | asset url by name
jget() {   # jget <file> tag | jget <file> asset <name>
    if [ "$json" = python3 ]; then
        python3 - "$@" <<'PY'
import json, sys
try:
    d = json.load(open(sys.argv[1], encoding="utf-8"))
except Exception:
    sys.exit(0)
if not isinstance(d, dict):
    sys.exit(0)
if sys.argv[2] == "tag":
    t = d.get("tag_name")
    print(t if isinstance(t, str) else "")
else:
    for a in d.get("assets") or []:
        if isinstance(a, dict) and a.get("name") == sys.argv[3]:
            u = a.get("browser_download_url")
            print(u if isinstance(u, str) else "")
            break
PY
    else
        if [ "$2" = tag ]; then jq -r 'if type=="object" and (.tag_name|type)=="string" then .tag_name else "" end' "$1" 2>/dev/null || true
        else jq -r --arg n "$3" 'if type=="object" then ((.assets // [])[] | select(type=="object" and .name==$n) | .browser_download_url // "") else "" end' "$1" 2>/dev/null | head -n1 || true; fi
    fi
}

# version compare: is $1 newer than $2 ?
newer() {
    local a b i x y
    IFS=. read -r -a a <<< "${1#v}"; IFS=. read -r -a b <<< "${2#v}"
    for i in 0 1 2 3; do
        x=$((10#${a[i]:-0})); y=$((10#${b[i]:-0}))
        [ "$x" -gt "$y" ] && return 0
        [ "$x" -lt "$y" ] && return 1
    done
    return 1
}

# value from qBittorrent's settings file: ini_get <file> <section> <key>
ini_get() {
    [ -f "$1" ] || return 0
    awk -v sec="[$2]" -v key="$3" '
        /^\[.*\][ \t\r]*$/ { sub(/[ \t\r]+$/, ""); insec = ($0 == sec); next }
        insec && index($0, key "=") == 1 { v = substr($0, length(key) + 2); sub(/\r$/, "", v); gsub(/^"|"$/, "", v); print v; exit }
    ' "$1"
}

echo
say "Noorjahan Web UI updater"
say "------------------------"
echo

if [ -z "$path" ]; then
    ini="${NJ_TEST_INI:-}"
    if [ -z "$ini" ]; then
        for c in "${XDG_CONFIG_HOME:-$HOME/.config}/qBittorrent/qBittorrent.conf" \
                 "$HOME/Library/Preferences/qBittorrent/qBittorrent.ini" \
                 "$HOME/.config/qBittorrent/qBittorrent.ini"; do
            [ -f "$c" ] && { ini="$c"; break; }
        done
    fi
    # qBittorrent 5.x: [WebUI] RootFolder; older: [Preferences] WebUI\RootFolder
    path="$(ini_get "$ini" WebUI RootFolder)"
    [ -n "$path" ] || path="$(ini_get "$ini" Preferences 'WebUI\RootFolder')"
    if [ -z "$path" ]; then
        if [ "$(id -u)" -eq 0 ]; then
            fail "Couldn't find qBittorrent's settings for root. Under sudo, name the folder: sudo bash $0 --path <your Noorjahan-WebUI folder>"
        fi
        fail "Couldn't find the Web UI folder in qBittorrent's settings. Run again with --path <your Noorjahan-WebUI folder>."
    fi
    say "Web UI folder (from qBittorrent's settings):"
    alt="$(ini_get "$ini" WebUI AlternativeUIEnabled)"
    [ -n "$alt" ] || alt="$(ini_get "$ini" Preferences 'WebUI\AlternativeUIEnabled')"
else
    say "Web UI folder:"
    alt=""
fi
path="${path%/}"
say "  $path"

[ -d "$path" ] || fail "That folder doesn't exist."
[ -d "$path/public" ] && [ -d "$path/private" ] || fail "That folder isn't a qBittorrent Web UI (no 'public' and 'private' inside). Nothing was changed."
abs="$(cd "$path" && pwd -P)"
[ "$abs" != "/" ] && [ "$abs" != "$HOME" ] || fail "Refusing to replace $abs."
[ -w "$(dirname "$abs")" ] || fail "No permission to write in $(dirname "$abs"). Run as the user that owns it (or with sudo)."

installed=""
nj="$abs/private/scripts/nj-update.js"
[ -f "$nj" ] && installed="$(sed -n 's/.*NJ_VERSION *= *"\([0-9.]*\)".*/\1/p' "$nj" | head -n1)"
if [ ! -f "$nj" ] && ! grep -qs Noorjahan "$abs/README.md" && [ "$force" -eq 0 ]; then
    fail "This doesn't look like the Noorjahan Web UI. Use --force if you really want to replace it."
fi
if [ -n "$installed" ]; then say "Installed: v$installed"; else say "Installed: older than v1.2.4 (no version stamp)"; fi
[ "$alt" = false ] && say "Note: \"Use alternative WebUI\" is off in qBittorrent, so this folder is not in use right now."

work="$(mktemp -d "${TMPDIR:-/tmp}/nj-webui-XXXXXX")"
staged=""
cleanup() { [ -n "$staged" ] && rm -rf -- "$staged"; rm -rf -- "$work"; }
trap cleanup EXIT

curl -fsSL --max-time 30 -H 'Accept: application/vnd.github+json' -A noorjahan-webui-updater "$API" -o "$work/rel.json" \
    || fail "Couldn't reach GitHub."
tag="$(jget "$work/rel.json" tag)"
printf '%s' "$tag" | grep -Eq "$TAG_RE" || fail "GitHub answered with an unexpected release tag: '$tag'."
say "Newest:    $tag"
zip_url="$(jget "$work/rel.json" asset "$ASSET")"
sum_url="$(jget "$work/rel.json" asset "$SUMS")"
[ -n "$zip_url" ] || fail "Release $tag has no $ASSET attached."
[ -n "$sum_url" ] || fail "Release $tag has no $SUMS attached, so the download can't be checked. Nothing was changed."
if [ -z "${NJ_TEST_API:-}" ]; then
    for u in "$zip_url" "$sum_url"; do
        case "$u" in "https://github.com/$REPO/releases/download/"*) ;; *) fail "Release asset has an unexpected download address: $u" ;; esac
    done
fi

is_newer=1
[ -n "$installed" ] && ! newer "$tag" "$installed" && is_newer=0
if [ "$check" -eq 1 ]; then
    if [ "$is_newer" -eq 1 ]; then say "An update is available."; else say "You are up to date."; fi
    echo; exit 0
fi
if [ "$is_newer" -eq 0 ] && [ "$force" -eq 0 ]; then say "You are up to date. Nothing to do."; echo; exit 0; fi

if [ "$yes" -eq 0 ]; then
    printf '  Replace the Web UI with %s? The old folder is kept as a backup. [Y/n] ' "$tag"
    read -r answer || answer=n
    case "$answer" in ''|y|Y|yes|Yes) ;; *) say "Cancelled. Nothing was changed."; echo; exit 0 ;; esac
fi

say "Downloading $ASSET ..."
curl -fsSL --max-time 300 -A noorjahan-webui-updater "$zip_url" -o "$work/$ASSET" || fail "Download failed."
curl -fsSL --max-time 60 -A noorjahan-webui-updater "$sum_url" -o "$work/$SUMS" || fail "Download of $SUMS failed."
want="$(tr -d '\r' < "$work/$SUMS" | awk -v n="$ASSET" '($2 == n || $2 == "*" n) && $1 ~ /^[0-9a-fA-F]{64}$/ { print tolower($1); exit }')"
[ -n "$want" ] || fail "$SUMS has no line for $ASSET."
got="$(sha "$work/$ASSET" | tr 'A-F' 'a-f')"
[ "$want" = "$got" ] || fail "Checksum mismatch: the download is damaged or was changed (expected $want, got $got)."
say "[ok] Checksum matches."

mkdir "$work/x"
unzip -q "$work/$ASSET" -d "$work/x" 2>/dev/null || fail "The download isn't a valid zip file."
src=""
for d in "$work/x" "$work/x"/* "$work/x"/*/*; do
    [ -d "$d/public" ] && [ -d "$d/private" ] && { src="$d"; break; }
done
[ -n "$src" ] || fail "The zip doesn't contain a Web UI folder (public + private)."
[ -f "$src/private/index.html" ] || fail "The zip is missing private/index.html."

parent="$(dirname "$abs")"; leaf="$(basename "$abs")"
staged="$parent/.$leaf.new-$$"
cp -R "$src" "$staged" || fail "Couldn't copy the new Web UI next to the old one."
# keep the old folder's owner and permissions (e.g. qbittorrent-nox running as another user)
if [ "$(id -u)" -eq 0 ]; then chown -R --reference="$abs" "$staged" 2>/dev/null || true; fi
chmod -R u+rwX,go+rX "$staged" 2>/dev/null || true

backup="$parent/$leaf.backup-$(date +%Y%m%d-%H%M%S)"
mv -- "$abs" "$backup" || fail "Couldn't move the old folder aside. Nothing was changed."
if ! mv -- "$staged" "$abs"; then
    mv -- "$backup" "$abs"
    fail "Couldn't put the new folder in place. The old Web UI was restored."
fi
staged=""
say "[ok] Updated to $tag."
say "     Old version kept in $backup"

# prune old backups (names sort by date)
ls -1d "$parent/$leaf".backup-* 2>/dev/null | sort -r | tail -n +"$((keep + 1))" | while IFS= read -r old; do rm -rf -- "$old"; done

echo
say "Reload the Web UI page in your browser to see it. qBittorrent does not need a restart."
echo
