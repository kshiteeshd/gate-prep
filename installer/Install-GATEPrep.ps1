# Fallback installer (no Inno Setup needed): copies the built app to %LOCALAPPDATA%\Programs\GATEPrep,
# creates Start-menu + Desktop shortcuts and registers an "Apps & features" uninstall entry.
$ErrorActionPreference = "Stop"
$src = Join-Path (Split-Path $PSScriptRoot -Parent) "dist\GATEPrep"
if (-not (Test-Path (Join-Path $src "GATEPrep.exe"))) { throw "Build first: run BUILD_EXE.bat" }
$dst = Join-Path $env:LOCALAPPDATA "Programs\GATEPrep"
Get-Process GATEPrep -ErrorAction SilentlyContinue | Stop-Process -Force
if (Test-Path $dst) { Remove-Item $dst -Recurse -Force }
New-Item -ItemType Directory -Force $dst | Out-Null
Copy-Item "$src\*" $dst -Recurse -Force
$exe = Join-Path $dst "GATEPrep.exe"
$ws = New-Object -ComObject WScript.Shell
foreach ($lnk in @((Join-Path ([Environment]::GetFolderPath("Programs")) "GATE Prep.lnk"), (Join-Path ([Environment]::GetFolderPath("Desktop")) "GATE Prep.lnk"))) {
    $s = $ws.CreateShortcut($lnk); $s.TargetPath = $exe; $s.WorkingDirectory = $dst; $s.Save()
}
$k = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\GATEPrep"
New-Item -Path $k -Force | Out-Null
Set-ItemProperty $k DisplayName "GATE Prep"
Set-ItemProperty $k DisplayIcon $exe
Set-ItemProperty $k InstallLocation $dst
Set-ItemProperty $k UninstallString "powershell -NoProfile -ExecutionPolicy Bypass -File `"$dst\Uninstall.ps1`""
@"
Get-Process GATEPrep -ErrorAction SilentlyContinue | Stop-Process -Force
Remove-Item "$(Join-Path ([Environment]::GetFolderPath('Programs')) 'GATE Prep.lnk')","$(Join-Path ([Environment]::GetFolderPath('Desktop')) 'GATE Prep.lnk')" -ErrorAction SilentlyContinue
Remove-Item "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\GATEPrep" -Recurse -ErrorAction SilentlyContinue
Remove-Item "$dst" -Recurse -Force
"@ | Set-Content (Join-Path $dst "Uninstall.ps1")
Write-Host "Installed to $dst  (your progress lives in $env:LOCALAPPDATA\GATEPrep)"
Start-Process $exe
