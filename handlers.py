"""Hotkey handlers for the input translation daemon.

This module defines the handlers for registered keyboard shortcuts:
- Translation hotkey: Copies, translates, and replaces selected text
- Restart hotkey: Restarts the daemon process
"""

import logging
import os
import subprocess
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
        """Translate selected text and replace it with the translation.
        
        This method:
        1. Copies the currently selected text
        2. Sends it to the translation service
        3. Replaces the original text with the translation
        
        Logs warnings if no text is selected and errors if translation fails.
        """
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
        """Restart the program by launching run.ps1 and exiting.
        
        This method:
        1. Unhooks all registered hotkeys
        2. Launches the run.ps1 script to start a new instance
        3. Exits the current process
        
        Raises:
            SystemExit: Always exits after attempting restart
        """
        logger.info("Restart hotkey triggered")
        script_dir = Path(__file__).parent
        run_script = script_dir / "run.ps1"
        keyboard.unhook_all_hotkeys()
        logger.debug("Unregistered all hotkeys before restart")

        try:
            logger.info("Launching restart via run.ps1")
            subprocess.Popen(
                ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(run_script)],
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            logger.info("Exiting for restart")
        except Exception as e:
            logger.exception("Failed to restart: %s", e)
        finally:
            sys.exit(0)
