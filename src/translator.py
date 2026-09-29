from langdetect import detect
from deep_translator import GoogleTranslator


def translate_to_english(text):
    language = detect(text)

    if language == "en":
        return language, text

    translated = GoogleTranslator(
        source=language,
        target="en"
    ).translate(text)

    return language, translated