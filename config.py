"""Configuration settings for the input translation daemon."""

# OpenAI Settings
MODEL = "gpt-4o-mini"

# Hotkey Settings
TRANSLATE_HOTKEY = "ctrl+alt+t"
RESTART_HOTKEY = "ctrl+alt+r"

# Timing Settings
CLIPBOARD_DELAY = 1.0
COPY_SLEEP = 0.05
PASTE_SLEEP = 0.01

# Logging Settings
LOG_FILE = "translation.log"
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
