"""Translation service for the input translation daemon."""

import logging
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

from config import MODEL

logger = logging.getLogger(__name__)


def get_client() -> OpenAI:
    """Initialize and return an OpenAI client."""
    logger.debug("Loading environment variables from .env")
    load_dotenv()
    api_key = os.getenv("API_KEY")
    logger.debug("API_KEY present: %s", bool(api_key))
    if not api_key:
        logger.error("Missing API_KEY in .env; exiting")
        sys.exit(1)

    logger.debug("Initializing OpenAI client")
    return OpenAI(api_key=api_key)


class TranslationService:
    """Service for translating text using OpenAI API."""

    def __init__(self):
        """Initialize the translation service."""
        self.client = get_client()
        self.model = MODEL

    def translate(self, text: str) -> str:
        """Translate text to English using OpenAI API.
        
        Args:
            text: The text to translate
            
        Returns:
            The translated text
            
        Raises:
            Exception: If translation fails
        """
        logger.debug("Sending translation request to model %s", self.model)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional translator. Translate the following text into natural, academic, and fluent English. Output ONLY the translation results.",
                },
                {"role": "user", "content": text},
            ],
        )

        translated_text = response.choices[0].message.content.strip()
        logger.debug("Received translated text length: %d", len(translated_text))
        return translated_text
