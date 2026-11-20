"""Noorjahan icon set for qBittorrent.

Every key is the exact file name qBittorrent loads (src/icons/<name>.svg in 5.3.0).
Each icon is (colour role, [elements]). An element is a path string, or a tuple:
  ("d", shape)  soft duotone fill (no stroke)
  ("f", shape)  solid fill (no stroke)
  ("t", shape, width)  stroke with a custom width
A shape is a path "d" string, or "c cx cy r", or "r x y w h rx".
Colour roles map to the variant's palette in build.py.
24px grid, 1.5px round stroke.  QtSvg-safe: no CSS, no <use>, no currentColor.
"""

FOLDER = "M3 7.5A2.5 2.5 0 0 1 5.5 5h3.3a2 2 0 0 1 1.4.6L12 7.4h6.5A2.5 2.5 0 0 1 21 9.9v7.6a2.5 2.5 0 0 1-2.5 2.5h-13A2.5 2.5 0 0 1 3 17.5z"
FILE = "M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"
MAGNET = "M5 3h4v8a3 3 0 0 0 6 0V3h4v8a7 7 0 0 1-14 0z"
PLAY = "M8 5.6v12.8a1 1 0 0 0 1.5.86l10.4-6.4a1 1 0 0 0 0-1.72L9.5 4.74A1 1 0 0 0 8 5.6z"
TRI = "M10.3 4.2 2.6 17.5A2 2 0 0 0 4.3 20.5h15.4a2 2 0 0 0 1.7-3L13.7 4.2a2 2 0 0 0-3.4 0z"
SHIELD = "M12 3l7 3v5.5c0 4.3-3 8-7 9.5-4-1.5-7-5.2-7-9.5V6z"
PLUG = "M6.5 7.5h11V11a5.5 5.5 0 0 1-11 0z"
TAG = "M20.6 13.4 13.4 20.6a2 2 0 0 1-2.8 0L3 13V3h10l7.6 7.6a2 2 0 0 1 0 2.8z"
MAST = ["c 12 9 2", "M12 11v10M8.5 21h7", "M8.5 5.5a5 5 0 0 0 0 7M15.5 5.5a5 5 0 0 1 0 7M5.6 2.6a9 9 0 0 0 0 12.8M18.4 2.6a9 9 0 0 1 0 12.8"]
MAST_S = ["c 9 9 2", "M9 11v10M5.5 21h7", "M5.5 5.5a5 5 0 0 0 0 7M12.5 5.5a5 5 0 0 1 0 7"]
PEERS = ["M10.9 6.8 6.1 15.2M13.1 6.8l4.8 8.4M7.5 18h9", ("d", "c 12 5 2.3"), "c 12 5 2.3", "c 5 18 2.3", "c 19 18 2.3"]
TURTLE = ["M3.5 15.5a7.5 6.5 0 0 1 15 0zM2 15.5h18.2", "M8 15.5l3-6 3 6", "M18 12.2a2 2 0 1 1 2.6 2.9", "M6.5 15.5v2.5M15.5 15.5v2.5"]
DOC_LINES = [FILE, "M14 3v5h5", "M8.5 12.5h7M8.5 16h5"]
LOGOUT = ["M14.5 4H18a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2h-3.5M10 16l4-4-4-4M14 12H4"]

ICONS = {
    # ---- toolbar / actions
    "list-add": ("accent", [("d", FILE), FILE, "M14 3v5h5M12 11.5v6M9 14.5h6"]),
    "insert-link": ("copper", [("d", MAGNET), MAGNET, "M5 7.5h4M15 7.5h4"]),
    "torrent-magnet": ("copper", [("d", MAGNET), MAGNET, "M5 7.5h4M15 7.5h4"]),
    "list-remove": ("err", ["M4 7h16M9.5 3.5h5M6.5 7l.9 12.1A2 2 0 0 0 9.4 21h5.2a2 2 0 0 0 2-1.9L17.5 7", "m10 11.5 4 4M14 11.5l-4 4"]),
    "torrent-start": ("ok", [("d", PLAY), PLAY]),
    "torrent-start-forced": ("ok", [("d", "M9 5.6v12.8a1 1 0 0 0 1.5.86l10-6.4a1 1 0 0 0 0-1.72l-10-6.4A1 1 0 0 0 9 5.6z"), "M9 5.6v12.8a1 1 0 0 0 1.5.86l10-6.4a1 1 0 0 0 0-1.72l-10-6.4A1 1 0 0 0 9 5.6z", "M4.5 5.5v13"]),
    "torrent-stop": ("amber", [("d", "M7.5 5h3v14h-3zM13.5 5h3v14h-3z"), "r 6.5 4.5 4 15 1.2", "r 13.5 4.5 4 15 1.2"]),
    "pause-session": ("amber", [("d", "c 12 12 9"), "c 12 12 9", "M10 9v6M14 9v6"]),
    "paused": ("idle", [("d", "c 12 12 9"), "c 12 12 9", "M10 9v6M14 9v6"]),
    "directory": ("amber", ["M3.5 17.5V7.5A2.5 2.5 0 0 1 6 5h3.3l2 2H17a2 2 0 0 1 2 2v1.5", ("d", "M3.5 18.5l2.6-6.3a2 2 0 0 1 1.85-1.2H19.8a1.3 1.3 0 0 1 1.2 1.8l-2.4 5.7a2 2 0 0 1-1.85 1.2H4.4z"), "M3.5 18.5l2.6-6.3a2 2 0 0 1 1.85-1.2H19.8a1.3 1.3 0 0 1 1.2 1.8l-2.4 5.7a2 2 0 0 1-1.85 1.2H4.4a.9.9 0 0 1-.9-.9z"]),
    "go-top": ("blue", ["M4 9h9M4 14h9M4 19h6", "M14.5 4h7M18 20V8.5M14.5 12 18 8.5l3.5 3.5"]),
    "go-up": ("blue", ["M4 6h9M4 12h9M4 18h6", "M18 20V8M14.5 11.5 18 8l3.5 3.5"]),
    "go-down": ("blue", ["M4 6h6M4 12h9M4 18h9", "M18 4v12M14.5 12.5 18 16l3.5-3.5"]),
    "go-bottom": ("blue", ["M4 5h6M4 10h9M4 15h9", "M14.5 20h7M18 4v11.5M14.5 12 18 15.5l3.5-3.5"]),
    "torrent-creator": ("violet", ["M11.5 21H7a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h7l5 5v2.5", "M14 3v5h5", ("d", "M19.4 13.1a1.4 1.4 0 0 1 2 2L16 20.5l-2.8.7.7-2.8z"), "M19.4 13.1a1.4 1.4 0 0 1 2 2L16 20.5l-2.8.7.7-2.8z"]),
    "configure": ("blue", ["M4 6.5h9M19 6.5h1M4 12h3M11 12h9M4 17.5h11M19 17.5h1", "c 16 6.5 2.2", "c 9 12 2.2", "c 17 17.5 2.2"]),
    "object-locked": ("amber", [("d", "r 4.5 10.5 15 10 2.5"), "r 4.5 10.5 15 10 2.5", "M8 10.5V8a4 4 0 0 1 8 0v2.5M12 14.5v2"]),
    "edit-find": ("blue", ["c 11 11 6.5", "m20 20-4.4-4.4"]),
    "edit-clear": ("n", ["c 12 12 9", "M9 9l6 6M15 9l-6 6"]),
    "edit-copy": ("blue", [("d", "r 8.5 8.5 12 12 2.5"), "r 8.5 8.5 12 12 2.5", "M15.5 8.5V6A2.5 2.5 0 0 0 13 3.5H6A2.5 2.5 0 0 0 3.5 6v7A2.5 2.5 0 0 0 6 15.5h2.5"]),
    "edit-rename": ("violet", ["M4 20h4L19 9a2.1 2.1 0 0 0-3-3L5 17z", "M14 7.5l2.5 2.5", "M13 20h7"]),
    "application-rss": ("copper", ["M5 11a8 8 0 0 1 8 8M5 5a14 14 0 0 1 14 14", ("f", "c 6 18 1.6")]),
    "application-url": ("blue", ["M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1", "M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"]),
    "application-exit": ("err", LOGOUT),
    "system-log-out": ("err", LOGOUT),
    "slow": ("accent", [("d", "M3.5 15.5a7.5 6.5 0 0 1 15 0z")] + TURTLE),
    "slow_off": ("n", TURTLE),
    "speedometer": ("accent", ["M3.5 17.5a8.5 8.5 0 1 1 17 0", "m12 17.5 4.2-5", "c 12 17.5 1.3", "M12 9v1.4M6.6 11.6l1 1M17.4 11.6l-1 1"]),
    "browser-cookies": ("amber", ["M20.5 12.5A8.5 8.5 0 1 1 11.5 3.5a3 3 0 0 0 4 4 3 3 0 0 0 5 5z", ("f", "c 9 10 1.1"), ("f", "c 14 15 1.1"), ("f", "c 8.5 15.5 1.1")]),
    "plugins": ("violet", [("d", "M10 3.5a2 2 0 0 1 4 0V6h4a1 1 0 0 1 1 1v4h-1.5a2 2 0 0 0 0 4H19v4a1 1 0 0 1-1 1h-4v-1.5a2 2 0 0 0-4 0V20H6a1 1 0 0 1-1-1v-4h1.5a2 2 0 0 0 0-4H5V7a1 1 0 0 1 1-1h4z"), "M10 3.5a2 2 0 0 1 4 0V6h4a1 1 0 0 1 1 1v4h-1.5a2 2 0 0 0 0 4H19v4a1 1 0 0 1-1 1h-4v-1.5a2 2 0 0 0-4 0V20H6a1 1 0 0 1-1-1v-4h1.5a2 2 0 0 0 0-4H5V7a1 1 0 0 1 1-1h4z"]),
    "help-about": ("blue", [("d", "c 12 12 9"), "c 12 12 9", "M12 11v5.5M12 7.7v.1"]),
    "help-contents": ("blue", ["c 12 12 9", "M9.6 9.4a2.5 2.5 0 1 1 3.4 2.4c-.6.3-1 .8-1 1.5v.5", "M12 16.8v.1"]),
    "wallet-open": ("amber", [("d", "M3.5 8h15a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5.5a2 2 0 0 1-2-2z"), "M3.5 8h15a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5.5a2 2 0 0 1-2-2V6.5A2.5 2.5 0 0 1 6 4h10.5V8", "M16 14h.01"]),
    "view-preview": ("blue", ["M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12z", ("d", "c 12 12 3"), "c 12 12 3"]),
    "view-refresh": ("accent", ["M20 12a8 8 0 1 1-2.4-5.7M20 4v4.5h-4.5"]),
    "view-statistics": ("violet", ["M4 20.5h16", ("d", "r 5 11 3.5 9.5 1"), "r 5 11 3.5 9.5 1", "r 10.25 5 3.5 15.5 1", "r 15.5 14 3.5 6.5 1"]),
    "name": ("blue", ["M3.5 18 8 6l4.5 12M5.3 14h5.4", "M15 10.5h5.5M15 14.5h5.5M15 18.5h3.5"]),
    "hash": ("blue", ["M9.5 4 8 20M16 4l-1.5 16M4.5 9h15M4 15h15"]),
    "ratio": ("accent", ["M7 20V5M3.5 8.5 7 5l3.5 3.5M17 4v15M13.5 15.5 17 19l3.5-3.5"]),
    "reannounce": ("accent", ["M20 12a8 8 0 1 1-2.4-5.7M20 4v4.5h-4.5", ("f", "c 12 12 2")]),
    "loading": ("n", ["M12 3a9 9 0 1 0 9 9"]),
    "fileicon": ("blue", [("d", FILE), FILE, "M14 3v5h5"]),
    "mail-inbox": ("blue", ["M3.5 13.5 6 5.5h12l2.5 8", ("d", "M3.5 13.5h5l1.5 2.5h4l1.5-2.5h5V18a2 2 0 0 1-2 2h-13a2 2 0 0 1-2-2z"), "M3.5 13.5h5l1.5 2.5h4l1.5-2.5h5V18a2 2 0 0 1-2 2h-13a2 2 0 0 1-2-2z"]),
    # ---- folders, categories, tags
    "folder-documents": ("amber", [("d", FOLDER), FOLDER]),
    "folder-new": ("amber", [("d", FOLDER), FOLDER, "M12 10.5v6M9 13.5h6"]),
    "folder-remote": ("amber", [("d", FOLDER), FOLDER, "M8.5 13.5h7M13 11l2.5 2.5L13 16"]),
    "view-categories": ("amber", [("d", FOLDER), FOLDER, "M8 12.5h8M8 15.5h5"]),
    "set-location": ("amber", [FOLDER, "M8.5 13.5h7M13 11l2.5 2.5L13 16"]),
    "tags": ("violet", [("d", TAG), TAG, "c 7.6 7.6 1.4"]),
    # ---- torrent states / status filters
    "filter-all": ("accent", [("d", "M12 3 3 7.5l9 4.5 9-4.5z"), "M12 3 3 7.5l9 4.5 9-4.5z", "m3 12 9 4.5 9-4.5M3 16.5 12 21l9-4.5"]),
    "downloading": ("dl", ["M12 3.5v11M7.5 10 12 14.5l4.5-4.5", "M4 15.5v2.5a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2.5"]),
    "download": ("accent", ["M12 3.5v11M7.5 10 12 14.5l4.5-4.5", ("d", "M4 15.5h16v2.5a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2z"), "M4 15.5v2.5a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2.5"]),
    "upload": ("up", ["M12 21v-9.5", ("d", "M12 12c0-4.2 2.8-7 7.5-7 0 4.2-2.8 7-7.5 7zM12 10C12 6.3 9.6 4 5 4c0 3.7 2.4 6 7 6z"), "M12 12c0-4.2 2.8-7 7.5-7 0 4.2-2.8 7-7.5 7zM12 10C12 6.3 9.6 4 5 4c0 3.7 2.4 6 7 6z", "M7.5 21h9"]),
    "checked-completed": ("ok", [("d", "c 12 12 9"), "c 12 12 9", "m8 12.4 2.8 2.8L16.2 9.6"]),
    "stopped": ("idle", [("d", "c 12 12 9"), "c 12 12 9", "r 9 9 6 6 1.2"]),
    "filter-active": ("dl", ["M3 12h3.5l2.5-6.5 5 13 2.5-6.5H21"]),
    "filter-inactive": ("idle", [("d", "M19.5 14.5A8 8 0 1 1 9.5 4.5a6.5 6.5 0 0 0 10 10z"), "M19.5 14.5A8 8 0 1 1 9.5 4.5a6.5 6.5 0 0 0 10 10z", "M15 3.5h3l-3 3h3"]),
    "filter-stalled": ("stall", ["M6.5 3h11M6.5 21h11", "M8 3c0 4.5 4 5 4 9s-4 4.5-4 9M16 3c0 4.5-4 5-4 9s4 4.5 4 9", ("d2", "M9.2 19.6c.7-1.8 2.8-2.8 2.8-2.8s2.1 1 2.8 2.8z")]),
    "stalledUP": ("stall", ["M9 20V5M5 9l4-4 4 4", "M16 13v7M20 13v7"]),
    "stalledDL": ("dl", ["M9 4v15M5 15l4 4 4-4", "M16 4v7M20 4v7"]),
    "force-recheck": ("check", [("d", "c 10.5 10.5 6.5"), "c 10.5 10.5 6.5", "m20 20-4.8-4.8", ("t", "M9.4 7.6 8.6 13.4M12.4 7.6l-.8 5.8M7.4 9.4h5.4M7 11.6h5.4", 1.15)]),
    "error": ("err", [("d", TRI), TRI, "M12 9.5V14M12 17.2v.1"]),
    "dialog-warning": ("stall", [("d", TRI), TRI, "M12 9.5V14M12 17.2v.1"]),
    "queued": ("idle", ["M4 6h12M4 11h6.5M4 16h4.5", ("d", "c 16.5 15.5 4.5"), "c 16.5 15.5 4.5", "M16.5 13.3v2.3l1.4 1.2"]),
    "task-complete": ("ok", ["m5 12.5 4.5 4.5L19 7.5"]),
    "task-reject": ("err", ["M6 6l12 12M18 6 6 18"]),
    # ---- trackers, peers, network
    "trackers": ("blue", MAST),
    "trackerless": ("idle", ["c 12 9 2", "M12 11v10M8.5 21h7M8.5 5.5a5 5 0 0 0 0 7M15.5 5.5a5 5 0 0 1 0 7", "M4 3l16 16"]),
    "tracker-warning": ("stall", MAST_S + [("t", "M19 6v6M19 15.5v.1", 2)]),
    "tracker-error": ("err", MAST_S + ["M16.5 6.5l5 5M21.5 6.5l-5 5"]),
    "peers": ("violet", PEERS),
    "peers-add": ("ok", PEERS[:1] + ["c 12 5 2.3", "c 5 18 2.3", "c 19 18 2.3"] + ["M19 3v4.5M16.75 5.25h4.5"]),
    "peers-remove": ("err", PEERS[:1] + ["c 12 5 2.3", "c 5 18 2.3", "c 19 18 2.3"] + ["M16.75 5.25h4.5"]),
    "ip-blocked": ("err", ["c 12 12 9", "M5.6 5.6l12.8 12.8"]),
    "network-server": ("blue", ["c 10.5 10.5 7.5", "M3 10.5h15M10.5 3a11 11 0 0 1 0 15M10.5 3a11 11 0 0 0 0 15", "M19 13.5V21M16.5 18.5 19 21l2.5-2.5"]),
    "network-connect": ("ok", ["M9 3v4.5M15 3v4.5", ("d", PLUG), PLUG, "M12 16.5V21"]),
    "connected": ("ok", ["M9 3v4.5M15 3v4.5", ("d2", PLUG), PLUG, "M12 16.5V21"]),
    "firewalled": ("stall", [("d", SHIELD), SHIELD, "M12 8.5v4M12 15.8v.1"]),
    "disconnected": ("err", ["M9 3v4M15 3v4M6.5 7.5H15m2.5 0V11a5.5 5.5 0 0 1-1.6 3.9M12 16.5V21M8.2 15A5.5 5.5 0 0 1 6.5 11V9", "M3.5 3.5l17 17"]),
    "security-high": ("ok", [("d", SHIELD), SHIELD, "m8.8 12 2.2 2.2 4.2-4.4"]),
    "security-low": ("stall", [SHIELD, "M9 12h6"]),
    # ---- details tabs
    "chart-line": ("accent", ["M3 20.5h18", ("d", "M4 16l4.5-5 3.5 3 7-8v14.5H4z"), "M4 16l4.5-5 3.5 3 7-8", "M15 6h4v4"]),
    # ---- options pages
    "preferences-desktop": ("blue", ["r 3 4 18 16 2.5", "M3 8.5h18", ("d", "r 6.5 12 9 4.5 2.25"), "r 6.5 12 9 4.5 2.25", "c 13.3 14.25 .9"]),
    "preferences-bittorrent": ("accent", [("t", "M12 9.5V5.1M14.2 10.8l3.8-2.2M14.2 13.2l3.8 2.2M12 14.5v4.4M9.8 13.2 6 15.4M9.8 10.8 6 8.6", 1.2), ("d2", "c 12 12 2.5"), "c 12 12 2.5", "c 12 3.5 1.6", "c 19.4 7.8 1.6", "c 19.4 16.2 1.6", "c 12 20.5 1.6", "c 4.6 16.2 1.6", "c 4.6 7.8 1.6"]),
    "preferences-webui": ("violet", [("d", "r 3 4 18 4.5 2"), "r 3 4 18 16 2.5", "M3 8.5h18", "M9 12.5l-2.2 2.2L9 16.9M15 12.5l2.2 2.2-2.2 2.2M12.8 12l-1.6 5.5"]),
    "preferences-advanced": ("copper", [("d", "r 7 7 10 10 2"), "r 7 7 10 10 2", "M10 3v4M14 3v4M10 17v4M14 17v4M3 10h4M3 14h4M17 10h4M17 14h4"]),
    # ---- RSS articles
    "rss_read_article": ("idle", DOC_LINES),
    "rss_unread_article": ("accent", [("d", FILE)] + DOC_LINES),
}

# small UI glyphs used by the stylesheet itself (ui/<name>.svg): (role, elements, size)
UI = {
    "chevron-down": ("text3", ["m7 10 5 5 5-5"], 16),
    "chevron-right": ("text3", ["m10 7 5 5-5 5"], 16),
    "chevron-up": ("text3", ["m7 14 5-5 5 5"], 16),
    "chevron-down-strong": ("text2", ["m7 10 5 5 5-5"], 16),
    "chevron-right-strong": ("text2", ["m10 7 5 5-5 5"], 16),
    "section-closed": ("text2", [("t", "m10 9 4 4-4 4", 1.9)], 16),
    "section-open": ("text2", [("t", "m8 11 4 4 4-4", 1.9)], 16),
    "chevron-down-disabled": ("disabled", ["m7 10 5 5 5-5"], 16),
    "chevron-up-disabled": ("disabled", ["m7 14 5-5 5 5"], 16),
    "sort-down": ("accent", [("t", "m6 9 6 6 6-6", 2.4)], 16),
    "sort-up": ("accent", [("t", "m6 15 6-6 6 6", 2.4)], 16),
    "check": ("onAccent", [("t", "m6 12.5 4 4 8-9", 2.6)], 16),
    "check-disabled": ("disabled", [("t", "m6 12.5 4 4 8-9", 2.6)], 16),
    "dash": ("onAccent", [("t", "M7 12h10", 2.6)], 16),
    "radio-dot": ("onAccent", [("f", "c 12 12 4.5")], 16),
    "menu-check": ("accent", [("t", "m6 12.5 4 4 8-9", 2.2)], 16),
    # menu check boxes drawn as images (TriStateWidget can't size a CSS box)
    "menu-box": ("boxLine", [("t", "M5.75 3.75h12.5a2 2 0 0 1 2 2v12.5a2 2 0 0 1-2 2H5.75a2 2 0 0 1-2-2V5.75a2 2 0 0 1 2-2z", 1.5)], 16),
    "menu-box-on": ("accent", [("f", "M6 3h12a3 3 0 0 1 3 3v12a3 3 0 0 1-3 3H6a3 3 0 0 1-3-3V6a3 3 0 0 1 3-3z"), ("t", "m8 12.3 2.8 2.8 5.4-6", 2.2, "onAccent")], 16),
    "menu-box-mixed": ("accent", [("f", "M6 3h12a3 3 0 0 1 3 3v12a3 3 0 0 1-3 3H6a3 3 0 0 1-3-3V6a3 3 0 0 1 3-3z"), ("t", "M8.5 12h7", 2.2, "onAccent")], 16),
    "menu-radio": ("accent", [("f", "c 12 12 4")], 16),
    "close": ("text3", ["M7.5 7.5l9 9M16.5 7.5l-9 9"], 16),
    "close-hover": ("text", ["M7.5 7.5l9 9M16.5 7.5l-9 9"], 16),
    "warning-16": ("err", [("d", TRI), TRI, "M12 9.5V14M12 17.2v.1"], 16),
    "warning-32": ("stall", [("d", TRI), TRI, "M12 9.5V14M12 17.2v.1"], 32),
}

# ---- optical fit (generated by scratchpad fit.py; scale, tx, ty)
FIT = {'list-add': (0.9749, 0.325, 0.325), 'insert-link': (1.0802, -0.936, 0.685), 'torrent-magnet': (1.0802, -0.936, 0.685), 'list-remove': (0.9351, 0.802, 0.569), 'torrent-start': (1.1133, -3.181, -1.359), 'torrent-start-forced': (0.9646, 0.325, 0.425), 'torrent-stop': (1.1706, -2.018, -2.018), 'directory': (0.9729, 0.058, 0.009), 'torrent-creator': (0.8947, 0.033, 1.196), 'configure': (0.997, 0.061, 0.061), 'go-top': (0.9351, 0.101, 0.802), 'go-up': (0.9351, 0.101, -0.133), 'go-down': (0.9351, 0.101, 1.738), 'go-bottom': (0.9351, 0.101, 0.802)}

# ---- icon library (2026-11-18): every icon above takes its geometry from the chosen
# library and keeps its Noorjahan colour role. Icons drawn duotone above keep a soft
# underlay: Tabler's filled variant, or Lucide's first closed shape. The hand-drawn set
# stays as the reference for roles and duotone choices (ICON_SET = "handdrawn" uses it).
import os as _os
# "fluent" | "phosphor" | "material" | "lucide" | "tabler" | "handdrawn"
ICON_SET = _os.environ.get("NOORJAHAN_ICONS", "fluent")
# "colour": each icon keeps its role colour; "mono": one neutral icon colour, with
# red/amber kept only for errors and warnings, and no soft underlays
ICON_TONE = _os.environ.get("NOORJAHAN_TONE", "colour")
# per-icon set overrides: Fluent has no magnet, so it borrows Lucide's (1.5px line,
# matching Fluent's regular weight)
ICON_OVERRIDE = {"insert-link": "lucide", "torrent-magnet": "lucide"} if ICON_SET == "fluent" else {}

from tabler_icons import TABLER
from lucide_icons import LUCIDE
from modern_icons import MODERN, TRANSFORM

def _duo(els):
    d = [e for e in els if isinstance(e, tuple) and e[0] in ("d", "d2")]
    return d[0][0] if d else None

def _library(name, role, els):
    iset = ICON_OVERRIDE.get(name, ICON_SET)
    duo = _duo(els)
    if ICON_TONE == "mono":
        role = role if role in ("err", "stall") else "n"
        duo = None
    if iset in MODERN and name in MODERN[iset]:
        _, main, under = MODERN[iset][name]; tf = TRANSFORM[iset]
        return (role, ([("pu", d, tf) for d in under] if duo else []) + [("p", d, tf) for d in main])
    if iset == "tabler" and name in TABLER:
        _, outline, filled = TABLER[name]
        return (role, ([(duo, p) for p in filled] if duo and filled else []) + outline)
    if iset == "lucide" and name in LUCIDE:
        _, strokes, closed = LUCIDE[name]
        return (role, ([(duo, closed[0])] if duo and closed else []) + strokes)
    return (role, els)

ICONS_HANDDRAWN = ICONS
if ICON_SET != "handdrawn":
    ICONS = {k: _library(k, role, els) for k, (role, els) in ICONS.items()}
    FIT = {}  # library glyphs are already optically balanced on the 24px grid
