Input Translation Daemon
\n
This tool translates selected text to fluent, academic English using an OpenAI model. Use the hotkey `Ctrl+Alt+T` to trigger translation in the active window.
\n
Logging
\n
- Logs are written to `translation.log` in the project directory.
- The log file is refreshed on each program launch (previous contents are cleared).
\n
Quick Start (Windows PowerShell with uv)

```powershell
# 1) Install uv (if not already installed)
Invoke-WebRequest -Uri https://astral.sh/uv/install.ps1 -UseBasicParsing | Invoke-Expression

# 2) Install project dependencies and create .venv from pyproject.toml
uv sync

# 3) Set your API key in .env
"API_KEY=YOUR_KEY" | Out-File -Encoding UTF8 .env

# 4) Run the program (console)
uv run python main.py

# Optional: run without console window
uv run pythonw main.py
```
\n
Usage

- Press `Ctrl+Alt+T` to translate the currently selected text.
- Press `Ctrl+Alt+R` to restart the program.

Startup Shortcut (optional)

- Use [install.ps1](install.ps1) to create a Startup folder shortcut that runs the daemon hidden on login using [run.ps1](run.ps1).
