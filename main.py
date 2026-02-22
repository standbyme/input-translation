import logging
import os
import sys
import time
from pathlib import Path

import keyboard
import pyperclip
from dotenv import load_dotenv
from openai import OpenAI

MODEL = "gpt-5-nano"


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("translation.log", mode="w"),
    ],
)
logger = logging.getLogger(__name__)


def get_client() -> OpenAI:
    logger.debug("Loading environment variables from .env")
    load_dotenv()
    api_key = os.getenv("API_KEY")
    logger.debug("API_KEY present: %s", bool(api_key))
    if not api_key:
        logger.error("Missing API_KEY in .env; exiting")
        sys.exit(1)

    logger.debug("Initializing OpenAI client")
    return OpenAI(api_key=api_key)


client = get_client()


def safe_copy_selected_text(delay: float = 1) -> str:
    """Copy selected text; restore clipboard on failure."""
    time.sleep(0.2 * delay)
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
        time.sleep(0.1 * delay)

        keyboard.press_and_release("ctrl+c")
        logger.debug("Sent Ctrl+C to copy selection")
        time.sleep(0.1 * delay)

        copied_text = pyperclip.paste().strip()
        logger.debug("Clipboard still empty, retrying...")

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


def restart_program():
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


def translate_and_replace():
    text_to_translate = safe_copy_selected_text()
    logger.debug("Text to translate length: %d", len(text_to_translate))

    if not text_to_translate:
        logger.warning("No text detected to translate")
        return

    try:
        logger.debug("Sending translation request to model %s", MODEL)
        response = client.responses.create(
            model=MODEL,
            instructions="You are a professional translator. Translate the following text into natural, academic, and fluent English. Output ONLY the translation results.",
            input=text_to_translate,
            service_tier="priority",
        )

        translated_text = response.output_text.strip()
        logger.debug("Received translated text length: %d", len(translated_text))

        pyperclip.copy(translated_text)
        logger.debug("Copied translated text to clipboard")

        keyboard.send("ctrl+a")
        time.sleep(0.01)
        keyboard.press_and_release("ctrl+v")
        logger.debug("Replaced selected text with translation")

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


if __name__ == "__main__":
    logger.info("Starting input translation daemon...")
    logger.info("Press Ctrl+Alt+T to translate selected text")
    logger.debug("Logger level set to DEBUG")

    try:
        # Register hotkey: Ctrl+Alt+T triggers translate_and_replace
        keyboard.add_hotkey(
            "ctrl+alt+t",
            translate_and_replace,
        )
        logger.info("Hotkey Ctrl+Alt+T registered for translation")
        # Register hotkey: Ctrl+Alt+R triggers program restart
        keyboard.add_hotkey(
            "ctrl+alt+r",
            restart_program,
        )
        logger.info("Hotkey Ctrl+Alt+R registered for restart")
        logger.debug("Awaiting hotkey activations")

        # Keep the program running
        keyboard.wait()
    except KeyboardInterrupt:
        logger.info("Shutdown requested by user")
    except Exception as e:
        logger.exception("Daemon error: %s", e)
    finally:
        logger.info("Input translation daemon stopped")
