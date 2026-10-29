
import re

def get_topic_words(keyword):
    topics = {
        "sports": [
            "sports", "cricket", "football", "soccer",
            "match", "player", "team", "tournament",
            "championship", "runs", "goal", "score",
            "arsenal", "chelsea", "league"
        ],
        "business": [
            "business", "company", "market", "stock",
            "finance", "economy", "bank", "investment",
            "revenue", "profit", "trade"
        ],
        "technology": [
            "technology", "tech", "software", "computer",
            "artificial intelligence", "internet",
            "smartphone", "robot", "cyber", "digital",
            "chip", "data", "cloud", "microsoft", "google"
        ],
        "science": [
            "science", "scientist", "research", "study",
            "experiment", "biology", "environment",
            "ecosystem", "species", "space", "nasa",
            "physics", "chemistry"
        ],
        "world": [
            "world", "international", "war", "president",
            "election", "minister", "diplomatic",
            "conflict", "nation", "government"
        ]
    }

    return topics.get(keyword.strip().lower(), [])


def check_topic(text, keyword):
    words = get_topic_words(keyword)

    if not words:
        return False

    text = text.lower()

    for word in words:
        pattern = r"\b" + re.escape(word) + r"\b"
        if re.search(pattern, text):
            return True

    return False
