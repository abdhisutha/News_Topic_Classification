
from langdetect import detect, LangDetectException
from deep_translator import GoogleTranslator
from deep_translator.exceptions import TooManyRequests


def translate_to_english(text):
    text = text.strip()

    if len(text) < 20:
        raise ValueError("Article text is too short.")

    try:
        language = detect(text)
    except LangDetectException:
        raise ValueError("Could not detect the article language.")

    if language == "en":
        return language, text

    try:
        translated = GoogleTranslator(
            source="auto",
            target="en"
        ).translate(text)

        if not translated:
            raise ValueError("Translation returned empty text.")

        return language, translated

    except TooManyRequests:
        raise ValueError(
            "Translation service is temporarily busy. Please try again later."
        )
    except Exception as error:
        raise ValueError(
            f"Translation failed: {error}"
        ) from error
