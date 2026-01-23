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


def get_client() -> OpenAI:
    load_dotenv()
    api_key = os.getenv("API_KEY")
    if not api_key:
        logger.error("Missing API_KEY in .env; exiting")
        sys.exit(1)

    return OpenAI(api_key=api_key)


client = get_client()


def safe_copy_selected_text(delay: float = 0.05) -> str:
    """Copy selected text; restore clipboard on failure."""

    original_clipboard = pyperclip.paste()
    pyperclip.copy("")

    try:
        keyboard.send("ctrl+a")
        time.sleep(delay)

        keyboard.send("ctrl+c")
        time.sleep(delay)
        return pyperclip.paste().strip()
    finally:
        # Best effort to avoid losing user's clipboard
        pyperclip.copy(original_clipboard)


def translate_and_replace():
    text_to_translate = safe_copy_selected_text()

    if not text_to_translate:
        logger.warning("No text detected to translate")
        return

    try:
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

        pyperclip.copy(translated_text)

        keyboard.send("ctrl+a")
        time.sleep(0.01)
        keyboard.press_and_release("ctrl+v")

    except Exception as e:
        logger.exception(
            "Translation failed for text (%d chars): %s\nException: %s",
            len(text_to_translate),
            text_to_translate[:100] + "..." if len(text_to_translate) > 100 else text_to_translate,
            e,
        )


if __name__ == "__main__":
    translate_and_replace()
