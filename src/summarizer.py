import re
from src.topic_filter import get_topic_words

def summarize_text(text, keyword, sentences=3):

    topic_words = get_topic_words(keyword)

    all_sentences = re.split(r'(?<=[.!?])\s+', text)

    relevant = []

    for sentence in all_sentences:
        sentence_lower = sentence.lower()

        score = sum(
            1 for word in topic_words
            if word in sentence_lower
        )

        if score > 0 and len(sentence.split()) > 5:
            relevant.append((score, sentence.strip()))

    relevant.sort(key=lambda x: x[0], reverse=True)

    selected = []

    for score, sentence in relevant:
        if sentence not in selected:
            selected.append(sentence)

        if len(selected) == sentences:
            break

    if not selected:
        return "No specific information found for this topic."

    return " ".join(selected)