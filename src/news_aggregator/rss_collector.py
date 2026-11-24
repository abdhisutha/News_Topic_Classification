
import feedparser
import requests
from src.news_aggregator.database import initialize_database, save_news, get_news_count

NEWS_FEEDS = {
    "World": [
        "https://feeds.bbci.co.uk/news/world/rss.xml",
        "https://www.theguardian.com/world/rss"
    ],
    "Business": [
        "https://feeds.bbci.co.uk/news/business/rss.xml",
        "https://www.theguardian.com/business/rss"
    ],
    "Technology": [
        "https://feeds.bbci.co.uk/news/technology/rss.xml",
        "https://www.theguardian.com/technology/rss"
    ],
    "Sports": [
        "https://feeds.bbci.co.uk/sport/rss.xml"
    ],
    "Science": [
        "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml"
    ]
}

def collect_news():
    all_news = []

    for category, urls in NEWS_FEEDS.items():
        for url in urls:
            try:
                response = requests.get(
                    url,
                    timeout=15,
                    headers={"User-Agent": "NEWSAI/1.0"}
                )

                feed = feedparser.parse(response.content)

                for entry in feed.entries:
                    image = ""

                    if "media_content" in entry:
                        image = entry.media_content[0].get("url", "")

                    elif "media_thumbnail" in entry:
                        image = entry.media_thumbnail[0].get("url", "")

                    all_news.append({
                        "title": entry.get("title", ""),
                        "url": entry.get("link", ""),
                        "description": entry.get("summary", ""),
                        "source": feed.feed.get("title", "News"),
                        "category": category,
                        "image": image,
                        "published": entry.get("published", "")
                    })

                print(f"Collected: {category} - {feed.feed.get('title', url)}")

            except Exception as e:
                print(f"Failed: {url} - {e}")

    return all_news


if __name__ == "__main__":
    initialize_database()
    articles = collect_news()
    save_news(articles)
    print("Total articles in database:", get_news_count())
