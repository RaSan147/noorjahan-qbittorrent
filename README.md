<div align="center">

# Noorjahan

**A calmer, evenly spaced Light & Dark theme for qBittorrent — with a matching Web UI.**

[![Version](https://img.shields.io/badge/version-1.2.5-1D786B?style=flat-square)](CHANGELOG.md)
[![qBittorrent](https://img.shields.io/badge/qBittorrent-5.3%20%C2%B7%20Web%20UI%205.2.3%2B-55514C?style=flat-square)](https://www.qbittorrent.org)
[![Platforms](https://img.shields.io/badge/platforms-Windows%20%C2%B7%20Linux%20Web%20UI-55514C?style=flat-square)](#compatibility)
[![License](https://img.shields.io/badge/license-GPL--2.0-55514C?style=flat-square)](LICENSE)

<br>

### [Download & Try the Live Demo → noorjahan.hamim2964.workers.dev](https://noorjahan.hamim2964.workers.dev/)

[Download](https://noorjahan.hamim2964.workers.dev/#download) · [Try Desktop Replica](https://noorjahan.hamim2964.workers.dev/#tour) · [Try Web UI](https://noorjahan.hamim2964.workers.dev/#webui) · [Before & After](https://noorjahan.hamim2964.workers.dev/#compare)

</div>

---

Noorjahan replaces qBittorrent's default chrome with warm stone surfaces, a single copper-patina teal accent, consistent 8 px card spacing, and 88 recoloured outline icons — using colour only when something is happening.

> [!NOTE]
> The full showcase — including an interactive browser replica of the desktop app, a live Web UI demo, and side-by-side before/after comparisons — lives on the **[project website](https://noorjahan.hamim2964.workers.dev/)**.

## Previews

| Light | Dark |
| :---: | :---: |
| [![Desktop Main Window — Light](https://i.ibb.co.com/BV0tyZvJ/01-pc-main-light.png)](https://ibb.co.com/VWftgSbG)<br><sub>Desktop · Main Window (Light)</sub> | [![Desktop Main Window — Dark](https://i.ibb.co.com/qL22FyS3/02-pc-main-dark.png)](https://ibb.co.com/0pzzVD7R)<br><sub>Desktop · Main Window (Dark)</sub> |
| [![Desktop Options — Light](https://i.ibb.co.com/kgr3RLyz/03-pc-options-light.png)](https://ibb.co.com/svD50TPc)<br><sub>Desktop · Options (Light)</sub> | [![Desktop Options — Dark](https://i.ibb.co.com/hF7RbmJX/04-pc-options-dark.png)](https://ibb.co.com/Mk2DrCx8)<br><sub>Desktop · Options (Dark)</sub> |
| [![Web UI — Light](https://i.ibb.co.com/7Jng9FVd/05-webui-light.png)](https://ibb.co.com/Z6BHZCKp)<br><sub>Web UI (Light)</sub> | [![Web UI — Dark](https://i.ibb.co.com/20fFX6rh/06-webui-dark.png)](https://ibb.co.com/RGVgLSKb)<br><sub>Web UI (Dark)</sub> |

<p align="center"><sub>Click any screenshot for full resolution · <a href="https://ibb.co.com/album/y6b6dZ">Full album</a> · <a href="https://noorjahan.hamim2964.workers.dev/#compare">Interactive before &amp; after</a></sub></p>

## Highlights

- **Measured card layout** — sidebar, transfer list, details panel, and status bar sit on a uniform 8 px grid with soft rounded corners and subtle hairline borders.
- **88 outline icons** — recoloured Fluent UI System Icons (plus Lucide magnet icons) across the toolbar, menus, dialogs, and all 14 torrent states.
- **Semantic state colour** — blue for downloading, green for seeding, amber for waiting, red for errors; neutral surfaces everywhere else.
- **Readable progress & controls** — slim underline progress bars that can match row state colours, pill-style detail tabs, and a rocket/turtle speed-limit toggle.
- **Consistent across surfaces** — covers the main window, Options, Add Torrent, Torrent Creator, and a matching Light/Dark Web UI that follows your system theme.

## Compatibility

| Target | Supported Versions | Platform |
| :--- | :--- | :--- |
| **Desktop App** | qBittorrent 5.3 | Windows 10 & 11 (works with or without Inter) |
| **Web UI** | qBittorrent 5.2.3 & 5.3.0 | Windows & Linux (tested on qBittorrent-nox / Raspberry Pi 4) |

## Download & Setup

All official packages (`Noorjahan-Setup.zip`, `Noorjahan-Light.qbtheme`, `Noorjahan-Dark.qbtheme`, and `Noorjahan-WebUI.zip`) are free to download from the website:

**[→ Download Noorjahan v1.2.5](https://noorjahan.hamim2964.workers.dev/#download)**

They are also attached to every [GitHub release](https://github.com/chiefhamim/noorjahan-qbittorrent/releases/latest) with a `SHA256SUMS.txt`, always under the same names, so the newest file is always at:

```
https://github.com/chiefhamim/noorjahan-qbittorrent/releases/latest/download/<file name>
```

### Windows — Quick Setup
1. Download `Noorjahan-Setup.zip` from [the website](https://noorjahan.hamim2964.workers.dev/#download) and extract it.
2. Run **`Install Noorjahan.cmd`** — installs both themes and the [Inter](https://rsms.me/inter/) font for your user (no admin needed), backs up `qBittorrent.ini`, and can switch the theme on automatically.

### Windows — Manual Setup
1. Download `Noorjahan-Light.qbtheme` or `Noorjahan-Dark.qbtheme` from [the website](https://noorjahan.hamim2964.workers.dev/#download) and save it in a permanent folder (e.g. `%APPDATA%\qBittorrent\themes`).
2. Open **Tools › Options › Behavior**, enable **Use custom UI theme**, and select the `.qbtheme` file.
3. On the same page, set **Style** to **`windows11`** (or **`windowsvista`** on Windows 10), then restart qBittorrent.

### Web UI
1. Download and extract `Noorjahan-WebUI.zip` from [the website](https://noorjahan.hamim2964.workers.dev/#download).
2. Open **Tools › Options › Web UI**, enable **Use alternative WebUI**, and select the `Noorjahan-WebUI` folder.
3. Hard-refresh the Web UI in your browser (`Ctrl+F5`).

### Web UI — Updates
From 1.2.4 the Web UI checks GitHub once a day and shows a small notice when a newer release is out. It never installs anything by itself, because qBittorrent can't let a web page write to its own folder. To turn the check off, click **Stop checking** in the notice or use **Help › Noorjahan update check**. The check is a plain request to `api.github.com`, so GitHub sees your IP address. No cookies or referrer are sent, and the setting stays in your browser.

To install an update, run the updater script. It finds your `Noorjahan-WebUI` folder from qBittorrent's settings, checks the download's SHA-256, keeps the old folder as a backup, and swaps in the new one. Then reload the page; qBittorrent does not need a restart.

**Windows (PowerShell):**
```powershell
irm https://github.com/chiefhamim/noorjahan-qbittorrent/releases/latest/download/update-webui.ps1 -OutFile update-webui.ps1
powershell -ExecutionPolicy Bypass -File .\update-webui.ps1
```

**Linux / Raspberry Pi** (run as the user that owns the folder):
```bash
curl -fsSLO https://github.com/chiefhamim/noorjahan-qbittorrent/releases/latest/download/update-webui.sh
bash update-webui.sh
```

Options: `-Path` / `--path` to name the folder yourself, `-Check` / `--check` to only look, `-Yes` / `--yes` to skip the question, `-KeepBackups` / `--keep-backups` (default 3).

The desktop `.qbtheme` can't be swapped while qBittorrent runs, so it has no in-app notice; download the new file and restart qBittorrent.

> [!TIP]
> In **Behavior › Transfer List**, enable **Make progress bars follow text colors** so each progress bar matches its torrent's state colour (blue while downloading, green while seeding).

## Building from Source

This repository contains the theme source (`src/`), Windows installer scripts (`setup/`), and Web UI typography assets (`fonts/`). To compile `.qbtheme` bundles locally, install `PySide6-Essentials` (which bundles `rcc.exe`) and run:

```bash
python src/build.py <path-to-rcc.exe>
```

This writes `build/light`, `build/dark`, and `dist/Noorjahan Light.qbtheme` / `dist/Noorjahan Dark.qbtheme`. See [CHANGELOG.md](CHANGELOG.md) for the release history.

## Credits & License

Noorjahan's architecture, visual design, Qt stylesheet, icon recolouring, Web UI restyle, and installer are by [chiefhamim](https://github.com/chiefhamim) and are licensed under [GPL-2.0-or-later](LICENSE). Not affiliated with the qBittorrent project.

| Component | Source | License |
| :--- | :--- | :--- |
| Base app & Web UI | [qBittorrent](https://www.qbittorrent.org) | GPL-2.0-or-later |
| Icons (86 of 88) | [Fluent UI System Icons](https://github.com/microsoft/fluentui-system-icons) by Microsoft | MIT |
| Magnet icons (2 of 88) | [Lucide](https://lucide.dev) | ISC |
| Typefaces | [Inter](https://rsms.me/inter/) · [Geist](https://vercel.com/font) | SIL OFL 1.1 |

---

<p align="center">
  <sub>In loving memory of my mother, <strong>Noorjahan</strong> (نور جهان — <em>light of the world</em>) · 9 July 2026</sub>
</p>
