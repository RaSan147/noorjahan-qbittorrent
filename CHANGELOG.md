# Changelog

All notable changes to Noorjahan for qBittorrent are documented here.
Download the latest release at [noorjahan.hamim2964.workers.dev](https://noorjahan.hamim2964.workers.dev/#download).

## 1.2.5
- **Unified `12 px` card radius** across the Transfer List, Sidebar, Details panel, Status Bar footer card, RSS cards, RSS Downloader cards, Execution Log, Options, Manage Cookies, and Plugins dialogs.
- **Maximized status bar hover fix:** Widened the right clearance on status bar pills and dividers so the Upload speed hover pill never overflows the `12 px` card corner when qBittorrent is maximized and Qt hides `QSizeGrip`.
- **Locked top toolbar height:** Matched `QToolBar QToolButton` vertical margin to `QToolBar QComboBox` so switching between `Transfers`, `Search`, `RSS`, and `Execution Log` never resizes or shifts the top panel.
- **Aligned vertical scrollbars:** Offset vertical scrollbars below column headers and the top progress divider in `Transfer List`, `General`, `Trackers`, `Peers`, `Content`, `RSS feeds`, `Plugins`, `Search Plugins`, `Manage Cookies`, and `Add New Torrent` so thumbs never poke into header banners.
- **Speed tab polish:** Leveled the `Period:` label with both dropdowns and restyled the `SpeedPlotView` chart into a recessed `10 px` rounded field card with muted `8.5 pt` axis labels.
- **RSS Downloader, RSS tab & Options fixes:** Restyled RSS Downloader into 3 equal-height `12 px` cards with true `10 px` `windows11` splitter gaps, aligned right edges, and removed branch artifacts; scoped `OptionsDialog` selectors so child dialogs opened from Options never inherit Options widths; aligned main tabs flush left and `Filter by` flush right; improved icon-to-text spacing on RSS/Search buttons and stripped trailing `...`.
- **Final-audit untouched areas polished:** Styled **Execution Log** into a matching `12 px` card, restyled **Manage Cookies** (`12 px` card, header dividers, opaque branch, framed `+`/trash buttons), **Plugins / Search Plugins**, and expanded **Statistics** so all 4 cards fit cleanly without scrolling.
- **Web UI & updater fixes:** Added `tools/stamp-webui-version.py` (`${CACHEID}_nj<ver>` cache-busting without qBittorrent restart), lowered `#njUpdate` z-index to `90` with 6-hour error backoff, added pause-on-exit to `update-webui.ps1`, and improved `sudo` guidance in `update-webui.sh`.

## 1.2.4
Web UI only; the desktop themes and the setup zip are the same as 1.2.3. Thanks to @schweppes-0x for the idea ([#2](https://github.com/chiefhamim/noorjahan-qbittorrent/issues/2)).
- **Update notice in the Web UI.** Once a day it asks GitHub for the newest release and, if there is a newer one, shows a small notice with a link to what changed. Dismiss it per version, turn it off with **Stop checking**, or use **Help › Check for Noorjahan update** / **Help › Noorjahan update check**. It only reads the public release info and sends no cookies or referrer; GitHub does see your IP address.
- **Release files on GitHub.** Every release now carries `Noorjahan-WebUI.zip`, `Noorjahan-Setup.zip`, both `.qbtheme` files, the updater scripts and `SHA256SUMS.txt`, under the same names each time. The newest is always at `https://github.com/chiefhamim/noorjahan-qbittorrent/releases/latest/download/<file>`.
- **Updater scripts** (`tools/update-webui.ps1` for Windows, `tools/update-webui.sh` for Linux and Raspberry Pi). They find the Web UI folder from qBittorrent's settings, check the download's SHA-256, keep the old folder as a backup and swap in the new one. Reload the page afterwards; qBittorrent does not need a restart.

## 1.2.3
- Fixed clipped button text on both sides of **Remove torrent and content** (and other long primary dialog buttons) when a button becomes the active default (`QPushButton:default` now keeps the same font weight as `QPushButton` so glyphs match Qt's layout `sizeHint`).

## 1.2.2
- Fixed clipped warning icons in the **Remove torrent(s)** dialog and **RSS Downloader** (Must Contain, Must Not Contain, and Episode Filter validation icons).
- Fixed clipped `<` and `>` tab-bar scroll buttons in **About qBittorrent** (and other overflowing tab bars), replacing them with clean themed chevrons inside framed buttons.
- Increased status-bar label height to `16 px` so the restart-required warning icon renders without vertical clipping.

## 1.2.1
- Fixed menu bar rendering without the Inter font (Windows 10 and Windows 11 without Inter).
- Added `Noorjahan-Setup.zip` one-click installer for both themes and the Inter font (no admin required).
- Redesigned the Web UI Add Torrent dialog to match the desktop app (cards, single label column, fitted file list, Cancel next to Add).
- Refined the desktop Add Torrent dialog (clean selected file pill, header divider line, styled Tags button).
- Verified Web UI compatibility on Linux (`qBittorrent-nox` 5.2.3 on Raspberry Pi 4).
- Increased row height in **Tools › Options › Advanced** so dropdowns and inputs no longer crowd together.
- Switched Light theme body text to Medium weight to match Dark and improve Qt pixel-snapped legibility on Windows.

## 1.2
- Replaced the status-bar speed-limit switch with a rocket at full speed and a turtle on alternative limits (animated in the Web UI).
- Rebalanced the Torrent Creator dialog (single label column, drop zone, rounded progress bar, right-aligned buttons).
- Evenly spaced toolbar group dividers in the Web UI to match the desktop app.

## 1.1
- Made downloading rows blue across desktop and Web UI, including stalled downloads.
- Changed transfer progress to a slim underline bar beneath the percentage that can follow row state colours.
- Aligned Web UI download icons with the desktop app.

## 1.0
- Initial release: Light and Dark `.qbtheme` bundles for qBittorrent 5.3 on Windows, plus matching Light/Dark Web UI.
