"""Main entry point for the input translation daemon.

This module initializes the translation daemon, registers hotkeys,
and manages the main event loop. The daemon runs in the background
and responds to configured keyboard shortcuts.
"""

import logging

import keyboard

from config import (
    LOG_DATE_FORMAT,
    LOG_FILE,
    LOG_FORMAT,
    RESTART_HOTKEY,
    TRANSLATE_HOTKEY,
)
from handlers import HotkeyHandler
from translator import TranslationService

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    datefmt=LOG_DATE_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE, mode="w"),
    ],
)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logger.info("Starting input translation daemon...")
    logger.info("Press %s to translate selected text", TRANSLATE_HOTKEY)
    logger.info("Press %s to restart the daemon", RESTART_HOTKEY)
    logger.debug("Logger level set to DEBUG")

    try:
        # Initialize services
        translation_service = TranslationService()
        handler = HotkeyHandler(translation_service)

        # Register hotkeys
        keyboard.add_hotkey(TRANSLATE_HOTKEY, handler.translate_and_replace)
        logger.info("Hotkey %s registered for translation", TRANSLATE_HOTKEY)

        keyboard.add_hotkey(RESTART_HOTKEY, handler.restart_program)
        logger.info("Hotkey %s registered for restart", RESTART_HOTKEY)
        logger.debug("Awaiting hotkey activations")

        # Keep the program running
        keyboard.wait()
    except KeyboardInterrupt:
        logger.info("Shutdown requested by user")
    except Exception as e:
        logger.exception("Daemon error: %s", e)
    finally:
        logger.info("Input translation daemon stopped")

