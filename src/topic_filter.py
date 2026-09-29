def check_topic(text, keyword):
    text = text.lower()
    keyword = keyword.lower()

    topics = {
        "sports": [
            "sports", "cricket", "football", "soccer",
            "match", "player", "team", "tournament",
            "championship", "runs", "goal", "score"
        ],

        "business": [
            "business", "company", "market", "stock",
            "finance", "economy", "bank", "investment"
        ],

        "technology": [
            "technology", "tech", "software", "computer",
            "ai", "artificial intelligence", "internet",
            "smartphone", "robot"
        ],

        "science": [
            "science", "scientist", "scientists",
            "research", "researchers", "study",
            "experiment", "biology", "environment",
            "ecosystem", "species", "organism"
        ],

        "world": [
            "world", "country", "government",
            "international", "war", "president", "election"
        ]
    }

    words = topics.get(keyword, [keyword])

    return any(word in text for word in words)