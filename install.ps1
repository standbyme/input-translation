# Installation script to create Start Menu shortcut with hotkey

# Get the directory where this script is located
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$runScript = Join-Path $scriptDir "run.ps1"

# Get the Start Menu Programs folder
$startMenuPath = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs"

# Ensure the directory exists
if (-not (Test-Path $startMenuPath)) {
    New-Item -Path $startMenuPath -ItemType Directory -Force | Out-Null
}

# Define the shortcut path
$shortcutPath = Join-Path $startMenuPath "Input Translation.lnk"

# Create the shortcut using COM object
$WScriptShell = New-Object -ComObject WScript.Shell
$shortcut = $WScriptShell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = "powershell.exe"
$shortcut.Arguments = "-WindowStyle Hidden -ExecutionPolicy Bypass -File `"$runScript`""
$shortcut.WorkingDirectory = $scriptDir
$shortcut.IconLocation = "powershell.exe,0"
$shortcut.Description = "Input Translation Tool"
$shortcut.Save()

Write-Host "Shortcut created successfully at: $shortcutPath"
Write-Host "Hotkey is now handled by the Python program (Ctrl+Shift+T)"
