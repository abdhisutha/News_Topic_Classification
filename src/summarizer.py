
import re
from collections import Counter

BOILERPLATE = [
    "read more",
    "click here",
    "subscribe now",
    "download the app",
    "related news",
    "follow us",
    "advertisement",
    "also read",
    "hello and welcome",
    "stay tuned",
    "what exactly is",
    "for more updates"
]


def summarize_text(text, keyword=None, sentences=3):
    if not text or len(text.strip()) < 20:
        return "Not enough article content to generate a summary."

    parts = re.split(r'(?<=[.!?।])\s+|\n+', text.strip())

    clean_sentences = []
    seen = set()

    for sentence in parts:
        sentence = re.sub(r'\s+', ' ', sentence).strip()
        lower = sentence.lower()

        if len(sentence.split()) < 7:
            continue

        if sentence.endswith("?"):
            continue

        if any(phrase in lower for phrase in BOILERPLATE):
            continue

        if lower in seen:
            continue

        seen.add(lower)
        clean_sentences.append(sentence)

    if not clean_sentences:
        return "No meaningful article content found."

    words = re.findall(r'\w+', " ".join(clean_sentences).lower())
    frequencies = Counter(
        word for word in words if len(word) > 2
    )

    scored = []

    for index, sentence in enumerate(clean_sentences):
        sentence_words = re.findall(r'\w+', sentence.lower())

        useful_words = [
            word for word in sentence_words
            if len(word) > 2
        ]

        if not useful_words:
            continue

        score = sum(
            frequencies[word] for word in useful_words
        ) / len(useful_words)

        position_bonus = 1 / (index + 1)
        score += position_bonus

        scored.append((score, index, sentence))

    selected = sorted(
        scored,
        key=lambda item: item[0],
        reverse=True
    )[:sentences]

    selected.sort(key=lambda item: item[1])

    return " ".join(item[2] for item in selected)
