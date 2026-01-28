"""Clipboard operations for the input translation daemon.

This module handles all clipboard-related functionality, including:
- Safely copying selected text while preserving the original clipboard
- Pasting translated text back to the active window
- Managing keyboard shortcuts for text selection and pasting
"""

import logging
import time

import keyboard
import pyperclip

from config import CLIPBOARD_DELAY, COPY_SLEEP, PASTE_SLEEP

logger = logging.getLogger(__name__)


def safe_copy_selected_text(delay: float = CLIPBOARD_DELAY) -> str:
    """Copy selected text while preserving the original clipboard content.
    
    This function:
    1. Saves the current clipboard content
    2. Clears the clipboard
    3. Selects all text (Ctrl+A) and copies it (Ctrl+C)
    4. Retrieves the copied text
    5. Restores the original clipboard content
    
    Args:
        delay: Timing multiplier for keyboard operations (default from config)
        
    Returns:
        The copied text as a string, or empty string if nothing was copied
    """
    time.sleep(0.1 * delay)
    logger.debug("Starting safe copy")
    original_clipboard = pyperclip.paste()
    logger.debug("Captured original clipboard (%d chars)", len(original_clipboard))
    pyperclip.copy("")
    logger.debug("Clipboard cleared")

    try:
        copied_text = ""
        pyperclip.copy("")  # Clear clipboard before each attempt

        keyboard.press_and_release("ctrl+a")
        logger.debug("Sent Ctrl+A to select all")
        time.sleep(COPY_SLEEP * delay)

        keyboard.press_and_release("ctrl+c")
        logger.debug("Sent Ctrl+C to copy selection")
        time.sleep(COPY_SLEEP * delay)

        copied_text = pyperclip.paste().strip()
        logger.debug("Clipboard content retrieved")

        # Show progress indicator after successfully copying
        if copied_text:
            keyboard.write(" translating...")
        else:
            keyboard.write(" no text copied")

        return copied_text
    finally:
        # Best effort to avoid losing user's clipboard
        pyperclip.copy(original_clipboard)
        logger.debug("Restored original clipboard")


def paste_text(text: str) -> None:
    """Paste text to replace the current selection.
    
    This function:
    1. Copies the provided text to the clipboard
    2. Selects all text in the active field (Ctrl+A)
    3. Pastes the clipboard content (Ctrl+V)
    
    Args:
        text: The text to paste
    """
    pyperclip.copy(text)
    logger.debug("Copied text to clipboard")

    keyboard.send("ctrl+a")
    time.sleep(PASTE_SLEEP)
    keyboard.press_and_release("ctrl+v")
    logger.debug("Replaced selected text")
