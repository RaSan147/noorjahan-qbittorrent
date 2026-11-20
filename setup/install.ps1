# Noorjahan for qBittorrent - installer
# Installs the Inter font for the current user (no admin needed), copies both themes
# into qBittorrent's folder and, if qBittorrent is closed, can switch the theme on.
# Nothing is deleted. qBittorrent.ini is backed up before it is changed.
# NJ_TEST_ROOT=<folder> redirects every path and the registry key (for testing).

$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$test = $env:NJ_TEST_ROOT

if ($test) {
    $fontDir  = Join-Path $test 'Fonts'
    $fontKey  = 'HKCU:\Software\NoorjahanInstallerTest\Fonts'
    $qbtDir   = Join-Path $test 'qBittorrent'
} else {
    $fontDir  = Join-Path $env:LOCALAPPDATA 'Microsoft\Windows\Fonts'
    $fontKey  = 'HKCU:\Software\Microsoft\Windows NT\CurrentVersion\Fonts'
    $qbtDir   = Join-Path $env:APPDATA 'qBittorrent'
}
$themeDir = Join-Path $qbtDir 'themes'
$ini      = Join-Path $qbtDir 'qBittorrent.ini'

function Say($t, $c = 'Gray') { Write-Host $t -ForegroundColor $c }

Say ''
Say '  Noorjahan for qBittorrent' 'Cyan'
Say '  -------------------------' 'Cyan'
Say ''

# 1. Inter font ---------------------------------------------------------------
function Test-Inter {
    if ($test) { $keys = @($fontKey) }
    else { $keys = @($fontKey, 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts') }
    foreach ($k in $keys) {
        if (-not (Test-Path $k)) { continue }
        $p = Get-ItemProperty $k
        foreach ($n in $p.PSObject.Properties.Name) {
            if ($n -match '^Inter( |\(|$)' -and $n -notmatch '^Inter \d+pt') { return $true }
        }
    }
    return $false
}

if (Test-Inter) {
    Say '  [ok] Inter is already installed.' 'Green'
} else {
    New-Item -ItemType Directory -Force $fontDir | Out-Null
    if (-not (Test-Path $fontKey)) { New-Item -Force $fontKey | Out-Null }
    $fonts = @(@{ File = 'Inter.ttf'; Name = 'Inter (TrueType)' },
               @{ File = 'Inter-Italic.ttf'; Name = 'Inter Italic (TrueType)' })
    foreach ($f in $fonts) {
        $src = Join-Path $here ('fonts\' + $f.File)
        $dst = Join-Path $fontDir $f.File
        Copy-Item $src $dst -Force
        New-ItemProperty -Path $fontKey -Name $f.Name -Value $dst -PropertyType String -Force | Out-Null
    }
    if (-not $test) {
        # let running apps know (new apps see the font anyway)
        Add-Type -Namespace NJ -Name Font -MemberDefinition @'
[DllImport("gdi32.dll", CharSet = CharSet.Unicode)] public static extern int AddFontResource(string f);
[DllImport("user32.dll")] public static extern System.IntPtr SendMessageTimeout(System.IntPtr h, uint m, System.IntPtr w, System.IntPtr l, uint f, uint t, out System.IntPtr r);
'@
        foreach ($f in $fonts) { [void][NJ.Font]::AddFontResource((Join-Path $fontDir $f.File)) }
        $r = [IntPtr]::Zero
        [void][NJ.Font]::SendMessageTimeout([IntPtr]0xffff, 0x001D, [IntPtr]::Zero, [IntPtr]::Zero, 2, 1000, [ref]$r)
    }
    Say '  [ok] Installed the Inter font (for this Windows user).' 'Green'
}

# 2. Themes -------------------------------------------------------------------
New-Item -ItemType Directory -Force $themeDir | Out-Null
foreach ($t in 'Noorjahan Light.qbtheme', 'Noorjahan Dark.qbtheme') {
    Copy-Item (Join-Path $here $t) (Join-Path $themeDir $t) -Force
}
Say "  [ok] Copied both themes to $themeDir" 'Green'
Say ''

# 3. Switch it on (only when qBittorrent is closed) ----------------------------
$running = $false
if (-not $test) { $running = [bool](Get-Process qbittorrent -ErrorAction SilentlyContinue) }

function Set-IniValue([string[]]$lines, [string]$section, [string]$key, [string]$value) {
    $out = New-Object System.Collections.Generic.List[string]
    $in = $false; $done = $false; $seen = $false
    foreach ($l in $lines) {
        if ($l -match '^\s*\[(.+)\]\s*$') {
            if ($in -and -not $done) { $out.Add("$key=$value"); $done = $true }
            $in = ($Matches[1] -eq $section); if ($in) { $seen = $true }
            $out.Add($l); continue
        }
        if ($in -and $l.StartsWith("$key=")) { if (-not $done) { $out.Add("$key=$value"); $done = $true }; continue }
        $out.Add($l)
    }
    if ($in -and -not $done) { $out.Add("$key=$value"); $done = $true }
    if (-not $seen) { if ($out.Count -and $out[$out.Count - 1] -ne '') { $out.Add('') }; $out.Add("[$section]"); $out.Add("$key=$value") }
    return ,$out.ToArray()
}

# Qt offers the windows11 style only on Windows 11 (build 22000+); Windows 10 uses windowsvista
$style = if ([Environment]::OSVersion.Version.Build -ge 22000) { 'windows11' } else { 'windowsvista' }

if ($running) {
    Say '  qBittorrent is open, so its settings were left alone. To finish:' 'Yellow'
    Say '    Tools > Options > Behavior: tick "Use custom UI theme", choose a file from'
    Say "    $themeDir"
    Say "    set Style to $style, then restart qBittorrent."
} elseif (-not (Test-Path $ini)) {
    Say '  qBittorrent has no settings file yet (open it once first). To finish:' 'Yellow'
    Say '    Tools > Options > Behavior: tick "Use custom UI theme", choose a file from'
    Say "    $themeDir"
    Say "    and set Style to $style."
} else {
    $ans = if ($env:NJ_TEST_ANSWER) { $env:NJ_TEST_ANSWER } else { Read-Host '  Turn it on now? [L] Light  [D] Dark  [N] No, I will do it myself' }
    $pick = switch -Regex ($ans) { '^[lL]' { 'Light' } '^[dD]' { 'Dark' } default { $null } }
    if ($pick) {
        $bak = "$ini.before-noorjahan-" + (Get-Date -Format 'yyyyMMdd-HHmmss') + '.bak'
        Copy-Item $ini $bak
        $lines = [System.IO.File]::ReadAllLines($ini)
        $path  = (Join-Path $themeDir "Noorjahan $pick.qbtheme").Replace('\', '/')
        $lines = Set-IniValue $lines 'Preferences' 'General\UseCustomUITheme' 'true'
        $lines = Set-IniValue $lines 'Preferences' 'General\CustomUIThemePath' $path
        $lines = Set-IniValue $lines 'Appearance' 'Style' $style
        [System.IO.File]::WriteAllLines($ini, $lines)
        Say "  [ok] Noorjahan $pick is on. Your old settings are saved as" 'Green'
        Say "       $bak"
        Say '  Open qBittorrent to see it.'
    } else {
        Say '  Settings left alone. To switch it on later:'
        Say '    Tools > Options > Behavior: tick "Use custom UI theme", choose a file from'
        Say "    $themeDir"
        Say "    and set Style to $style."
    }
}
Say ''
