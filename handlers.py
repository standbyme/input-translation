"""Hotkey handlers for the input translation daemon."""

import logging
import os
import sys
from pathlib import Path

import keyboard

from clipboard import paste_text, safe_copy_selected_text
from translator import TranslationService

logger = logging.getLogger(__name__)


class HotkeyHandler:
    """Handler for hotkey actions."""

    def __init__(self, translation_service: TranslationService):
        """Initialize the hotkey handler.
        
        Args:
            translation_service: The translation service to use
        """
        self.translation_service = translation_service

    def translate_and_replace(self) -> None:
        """Translate selected text and replace it."""
        text_to_translate = safe_copy_selected_text()
        logger.debug("Text to translate length: %d", len(text_to_translate))

        if not text_to_translate:
            logger.warning("No text detected to translate")
            return

        try:
            translated_text = self.translation_service.translate(text_to_translate)
            paste_text(translated_text)
            logger.info("Translation completed successfully")

        except Exception as e:
            logger.exception(
                "Translation failed for text (%d chars): %s\nException: %s",
                len(text_to_translate),
                (
                    text_to_translate[:100] + "..."
                    if len(text_to_translate) > 100
                    else text_to_translate
                ),
                e,
            )

    @staticmethod
    def restart_program() -> None:
        """Restart the program by launching run.ps1 and exiting."""
        logger.info("Restart hotkey triggered")
        script_dir = Path(__file__).parent
        run_script = script_dir / "run.ps1"
        keyboard.unhook_all_hotkeys()
        logger.debug("Unregistered all hotkeys before restart")

        try:
            logger.info("Launching restart via run.ps1")
            os.system(f'powershell -NoProfile -ExecutionPolicy Bypass -File "{run_script}"')
            logger.info("Exiting for restart")
        except Exception as e:
            logger.exception("Failed to restart: %s", e)
        finally:
            sys.exit(0)
