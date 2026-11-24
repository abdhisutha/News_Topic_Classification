
from langdetect import detect, LangDetectException
from deep_translator import GoogleTranslator


def detect_language(text):
    text = text.strip()

    if len(text) < 20:
        raise ValueError("Article text is too short.")

    try:
        return detect(text)
    except LangDetectException:
        raise ValueError("Could not detect the article language.")


def translate_to_english(text):
    language = detect_language(text)

    if language == "en":
        return language, text

    try:
        translated = GoogleTranslator(
            source="auto",
            target="en"
        ).translate(text[:4500])

        if not translated:
            return language, None

        return language, translated

    except Exception as error:
        print("Translation unavailable:", error)
        return language, None
