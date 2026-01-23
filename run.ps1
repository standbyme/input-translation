# Run the input translation tool
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir
Start-Process -FilePath "uv" -ArgumentList "run", "pythonw", "main.py" -NoNewWindow -WorkingDirectory $scriptDir