<#
.SYNOPSIS
    Updates the Noorjahan Web UI for qBittorrent to the newest GitHub release.

.DESCRIPTION
    1. Finds the alternative Web UI folder qBittorrent uses (or takes -Path).
    2. Asks GitHub for the newest release and compares it with the installed version.
    3. Downloads Noorjahan-WebUI.zip and SHA256SUMS.txt, and checks the zip's SHA-256.
    4. Keeps the old folder as "<folder>.backup-<date>" and puts the new one in its place.
       If anything fails, the old folder is put back.
    Then reload the Web UI page in your browser. qBittorrent does not need a restart.

.PARAMETER Path
    The Noorjahan-WebUI folder (the one that holds "public" and "private").
    Default: the folder set in qBittorrent's settings.

.PARAMETER Check
    Only report the installed and newest versions. Changes nothing.

.PARAMETER Force
    Install even if the installed version is the same or newer.

.PARAMETER Yes
    Don't ask before replacing the folder.

.PARAMETER KeepBackups
    How many old backups to keep next to the folder (default 3).

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File update-webui.ps1
.EXAMPLE
    powershell -ExecutionPolicy Bypass -File update-webui.ps1 -Path "D:\qBittorrent\Noorjahan-WebUI" -Yes
#>
[CmdletBinding()]
param(
    [string]$Path,
    [switch]$Check,
    [switch]$Force,
    [switch]$Yes,
    [ValidateRange(0, 50)][int]$KeepBackups = 3
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2.0

$Repo   = 'chiefhamim/noorjahan-qbittorrent'
$Api    = if ($env:NJ_TEST_API) { $env:NJ_TEST_API } else { "https://api.github.com/repos/$Repo/releases/latest" }
$Asset  = 'Noorjahan-WebUI.zip'
$Sums   = 'SHA256SUMS.txt'
$TagRe  = '^v?\d{1,4}(\.\d{1,4}){0,3}$'

# Windows PowerShell 5.1 may default to TLS 1.0
try { [Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12 } catch { }
$ProgressPreference = 'SilentlyContinue'   # makes Invoke-WebRequest much faster on 5.1

function Say([string]$t, [string]$c = 'Gray') { Write-Host $t -ForegroundColor $c }
function Fail([string]$t) { Say "  [x] $t" 'Red'; Say ''; exit 1 }

function ConvertTo-Version([string]$tag) {
    $parts = @(($tag -replace '^v', '').Split('.') | ForEach-Object { [int]$_ })
    while ($parts.Count -lt 4) { $parts += 0 }
    return New-Object Version $parts[0], $parts[1], $parts[2], $parts[3]
}

# ---------------------------------------------------------------- where is the Web UI?
function Get-IniValue([string]$file, [string]$section, [string]$key) {
    if (-not (Test-Path -LiteralPath $file)) { return $null }
    $in = $false
    foreach ($l in [IO.File]::ReadAllLines($file)) {
        if ($l -match '^\s*\[(.+)\]\s*$') { $in = ($Matches[1] -eq $section); continue }
        if ($in -and $l.StartsWith("$key=")) { return $l.Substring($key.Length + 1).Trim('"') }
    }
    return $null
}

function Find-WebUiFolder {
    $ini = if ($env:NJ_TEST_INI) { $env:NJ_TEST_INI } else { Join-Path $env:APPDATA 'qBittorrent\qBittorrent.ini' }
    # qBittorrent 5.x keeps it in [WebUI]; older versions in [Preferences] as WebUI\RootFolder
    $root = Get-IniValue $ini 'WebUI' 'RootFolder'
    if (-not $root) { $root = Get-IniValue $ini 'Preferences' 'WebUI\RootFolder' }
    if ($root) { $root = $root.Replace('\\', '\').Replace('/', '\') }
    return $root
}

Say ''
Say '  Noorjahan Web UI updater' 'Cyan'
Say '  ------------------------' 'Cyan'
Say ''

if (-not $Path) {
    $Path = Find-WebUiFolder
    if (-not $Path) {
        Fail ("Couldn't find the Web UI folder in qBittorrent's settings.`n" +
              "      Run again with -Path ""<your Noorjahan-WebUI folder>"".")
    }
    Say "  Web UI folder (from qBittorrent's settings):"
}
else { Say '  Web UI folder:' }
$Path = [IO.Path]::GetFullPath($Path.TrimEnd('\', '/'))
Say "    $Path"

if (-not (Test-Path -LiteralPath $Path -PathType Container)) { Fail "That folder doesn't exist." }
if (-not ((Test-Path -LiteralPath (Join-Path $Path 'public') -PathType Container) -and
          (Test-Path -LiteralPath (Join-Path $Path 'private') -PathType Container))) {
    Fail "That folder isn't a qBittorrent Web UI (no 'public' and 'private' inside). Nothing was changed."
}
$driveRoot = [IO.Path]::GetPathRoot($Path)
if ($Path -eq $driveRoot.TrimEnd('\')) { Fail 'Refusing to replace a whole drive.' }

# installed version: from scripts/nj-update.js (added in 1.2.4; older builds don't have it)
$installed = $null
$nj = Join-Path $Path 'private\scripts\nj-update.js'
if (Test-Path -LiteralPath $nj) {
    $m = Select-String -LiteralPath $nj -Pattern 'NJ_VERSION\s*=\s*"([0-9.]+)"' | Select-Object -First 1
    if ($m) { $installed = $m.Matches[0].Groups[1].Value }
}
$isNoorjahan = (Test-Path -LiteralPath $nj) -or
               (Select-String -LiteralPath (Join-Path $Path 'README.md') -Pattern 'Noorjahan' -Quiet -ErrorAction SilentlyContinue)
if (-not $isNoorjahan -and -not $Force) {
    Fail "This doesn't look like the Noorjahan Web UI. Use -Force if you really want to replace it."
}
if ($installed) { Say "  Installed: v$installed" } else { Say '  Installed: older than v1.2.4 (no version stamp)' }
if (-not $PSBoundParameters.ContainsKey('Path')) {
    $iniFile = if ($env:NJ_TEST_INI) { $env:NJ_TEST_INI } else { Join-Path $env:APPDATA 'qBittorrent\qBittorrent.ini' }
    $altOn = Get-IniValue $iniFile 'WebUI' 'AlternativeUIEnabled'
    if (-not $altOn) { $altOn = Get-IniValue $iniFile 'Preferences' 'WebUI\AlternativeUIEnabled' }
    if ($altOn -eq 'false') { Say '  Note: "Use alternative WebUI" is off in qBittorrent, so this folder is not in use right now.' 'Yellow' }
}

# ---------------------------------------------------------------- newest release
try {
    $rel = Invoke-RestMethod -Uri $Api -Headers @{ 'Accept' = 'application/vnd.github+json'; 'User-Agent' = 'noorjahan-webui-updater' } -TimeoutSec 30
}
catch { Fail "Couldn't reach GitHub: $($_.Exception.Message)" }
function Get-Prop($o, [string]$n) {
    if (($null -ne $o) -and ($o -is [psobject]) -and $o.PSObject.Properties[$n]) { return $o.$n }
    return $null
}
$tag = [string](Get-Prop $rel 'tag_name')
if ($tag -notmatch $TagRe) { Fail "GitHub answered with an unexpected release tag: '$tag'." }
Say "  Newest:    $tag"

$assets   = @(Get-Prop $rel 'assets' | Where-Object { $null -ne $_ })
$zipAsset = $assets | Where-Object { (Get-Prop $_ 'name') -eq $Asset } | Select-Object -First 1
$sumAsset = $assets | Where-Object { (Get-Prop $_ 'name') -eq $Sums } | Select-Object -First 1
foreach ($a in @($zipAsset, $sumAsset)) {
    if ($a -and ([string](Get-Prop $a 'browser_download_url') -notmatch "^https://github\.com/$([regex]::Escape($Repo))/releases/download/")) {
        if (-not $env:NJ_TEST_API) { Fail "Release asset has an unexpected download address: $(Get-Prop $a 'browser_download_url')" }
    }
}
if (-not $zipAsset) { Fail "Release $tag has no $Asset attached." }
if (-not $sumAsset) { Fail "Release $tag has no $Sums attached, so the download can't be checked. Nothing was changed." }

$newer = (-not $installed) -or ((ConvertTo-Version $tag) -gt (ConvertTo-Version $installed))
if ($Check) {
    if ($newer) { Say "  An update is available." 'Yellow' } else { Say '  You are up to date.' 'Green' }
    Say ''; exit 0
}
if (-not $newer -and -not $Force) { Say '  You are up to date. Nothing to do.' 'Green'; Say ''; exit 0 }

if (-not $Yes) {
    $a = Read-Host "  Replace the Web UI with $($tag)? The old folder is kept as a backup. [Y/n]"
    if ($a -and $a -notmatch '^[yY]') { Say '  Cancelled. Nothing was changed.'; Say ''; exit 0 }
}

# ---------------------------------------------------------------- download + verify
$work = Join-Path ([IO.Path]::GetTempPath()) ('nj-webui-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $work | Out-Null
$staged = $null
try {
    $zip = Join-Path $work $Asset
    $sum = Join-Path $work $Sums
    Say "  Downloading $Asset ..."
    Invoke-WebRequest -Uri $zipAsset.browser_download_url -OutFile $zip -UseBasicParsing -TimeoutSec 300 -Headers @{ 'User-Agent' = 'noorjahan-webui-updater' }
    Invoke-WebRequest -Uri $sumAsset.browser_download_url -OutFile $sum -UseBasicParsing -TimeoutSec 60 -Headers @{ 'User-Agent' = 'noorjahan-webui-updater' }

    $line = Get-Content -LiteralPath $sum | Where-Object { $_ -match "^\s*([0-9a-fA-F]{64})\s+\*?$([regex]::Escape($Asset))\s*$" } | Select-Object -First 1
    if (-not $line) { throw "$Sums has no line for $Asset." }
    $want = ([regex]::Match($line, '[0-9a-fA-F]{64}')).Value.ToLowerInvariant()
    # plain .NET instead of Get-FileHash / Expand-Archive: those modules can fail to load
    # when Windows PowerShell 5.1 is started from a PowerShell 7 window (mixed PSModulePath)
    $sha = [Security.Cryptography.SHA256]::Create()
    $fs  = [IO.File]::OpenRead($zip)
    try { $got = (-join ($sha.ComputeHash($fs) | ForEach-Object { $_.ToString('x2') })) }
    finally { $fs.Dispose(); $sha.Dispose() }
    if ($want -ne $got) { throw "Checksum mismatch: the download is damaged or was changed (expected $want, got $got)." }
    Say '  [ok] Checksum matches.' 'Green'

    $ex = Join-Path $work 'x'
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    try { [IO.Compression.ZipFile]::ExtractToDirectory($zip, $ex) }
    catch { throw "The download isn't a valid zip file ($($_.Exception.Message))." }
    # the zip holds one folder ("Noorjahan-WebUI") with public/ and private/
    $src = Get-ChildItem -LiteralPath $ex -Directory -Recurse -Depth 2 |
           Where-Object { (Test-Path -LiteralPath (Join-Path $_.FullName 'public')) -and (Test-Path -LiteralPath (Join-Path $_.FullName 'private')) } |
           Select-Object -First 1
    if (-not $src -and (Test-Path -LiteralPath (Join-Path $ex 'public')) -and (Test-Path -LiteralPath (Join-Path $ex 'private'))) { $src = Get-Item -LiteralPath $ex }
    if (-not $src) { throw "The zip doesn't contain a Web UI folder (public + private)." }
    if (-not (Test-Path -LiteralPath (Join-Path $src.FullName 'private\index.html'))) { throw 'The zip is missing private\index.html.' }

    # stage next to the real folder (same drive, so the final swap is a quick rename)
    $parent = Split-Path -Parent $Path
    $leaf   = Split-Path -Leaf $Path
    $staged = Join-Path $parent ".$leaf.new-$([guid]::NewGuid().ToString('N').Substring(0, 8))"
    Copy-Item -LiteralPath $src.FullName -Destination $staged -Recurse

    # ------------------------------------------------------------ swap
    $stamp  = Get-Date -Format 'yyyyMMdd-HHmmss'
    $backup = Join-Path $parent "$leaf.backup-$stamp"
    Rename-Item -LiteralPath $Path -NewName (Split-Path -Leaf $backup)
    try {
        Rename-Item -LiteralPath $staged -NewName $leaf
        $staged = $null
    }
    catch {
        Rename-Item -LiteralPath $backup -NewName $leaf   # put the old one back
        throw "Couldn't put the new folder in place ($($_.Exception.Message)). The old Web UI was restored."
    }
    Say "  [ok] Updated to $tag." 'Green'
    Say "       Old version kept in $backup"

    # prune old backups
    if ($KeepBackups -ge 0) {
        Get-ChildItem -LiteralPath $parent -Directory -Filter "$leaf.backup-*" |
            Sort-Object Name -Descending | Select-Object -Skip $KeepBackups |
            ForEach-Object { Remove-Item -LiteralPath $_.FullName -Recurse -Force }
    }
    Say ''
    Say '  Reload the Web UI page in your browser to see it. qBittorrent does not need a restart.'
    Say ''
}
catch {
    if ($staged -and (Test-Path -LiteralPath $staged)) { Remove-Item -LiteralPath $staged -Recurse -Force -ErrorAction SilentlyContinue }
    Fail $_.Exception.Message
}
finally {
    Remove-Item -LiteralPath $work -Recurse -Force -ErrorAction SilentlyContinue
}
