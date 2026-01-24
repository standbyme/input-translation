# Run the input translation daemon in the background
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# Wait 0.5 seconds to avoid hotkey conflicts if restarting
Start-Sleep -Seconds 0.5

Start-Process -FilePath "uv" -ArgumentList "run", "pythonw", "main.py" -WindowStyle Hidden -WorkingDirectory $scriptDir