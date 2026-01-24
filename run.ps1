# Run the input translation daemon in the background
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

Start-Process -FilePath "uv" -ArgumentList "run", "pythonw", "main.py" -WindowStyle Hidden -WorkingDirectory $scriptDir