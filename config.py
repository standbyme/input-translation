"""Configuration settings for the input translation daemon.

This module contains all configurable constants for the application,
including OpenAI model settings, hotkey bindings, timing parameters,
and logging configuration.
"""

# OpenAI Settings
MODEL = "gpt-4o-mini"  # OpenAI model to use for translation

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
