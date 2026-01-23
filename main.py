import logging
import os
import sys
import time

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
        logging.FileHandler("translation.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


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


def safe_copy_selected_text(delay: float = 0.5) -> str:
    """Copy selected text; restore clipboard on failure."""
    logger.debug("Starting safe copy with delay %.3f", delay)
    original_clipboard = pyperclip.paste()
    logger.debug("Captured original clipboard (%d chars)", len(original_clipboard))
    pyperclip.copy("")
    logger.debug("Clipboard cleared")

    try:
        keyboard.send("ctrl+a")
        logger.debug("Sent Ctrl+A to select all")
        time.sleep(delay)

        keyboard.send("ctrl+c")
        logger.debug("Sent Ctrl+C to copy selection")
        time.sleep(delay)
        copied_text = pyperclip.paste().strip()
        logger.debug("Copied text length: %d", len(copied_text))
        return copied_text
    finally:
        # Best effort to avoid losing user's clipboard
        pyperclip.copy(original_clipboard)
        logger.debug("Restored original clipboard")


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
            input=[
                {
                    "role": "system",
                    "content": "You are a professional translator. Translate the following text into natural, academic, and fluent English. Output ONLY the translation results.",
                },
                {"role": "user", "content": text_to_translate},
            ],
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
        keyboard.add_hotkey("ctrl+alt+t", translate_and_replace)
        logger.info("Hotkey registered successfully")
        logger.debug("Awaiting hotkey activations")

        # Keep the program running
        keyboard.wait()
    except KeyboardInterrupt:
        logger.info("Shutdown requested by user")
    except Exception as e:
        logger.exception("Daemon error: %s", e)
    finally:
        logger.info("Input translation daemon stopped")
