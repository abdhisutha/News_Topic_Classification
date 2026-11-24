
import requests
import trafilatura
from bs4 import BeautifulSoup
from trafilatura.metadata import extract_metadata


def extract_article(url):
    url = url.strip()

    if not url.startswith(("http://", "https://")):
        raise Exception("Please enter a valid article URL.")

    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(
        url,
        headers=headers,
        timeout=20
    )
    response.raise_for_status()

    downloaded = response.text

    text = trafilatura.extract(
        downloaded,
        include_comments=False,
        include_tables=False,
        favor_precision=True,
        deduplicate=True
    )

    metadata = extract_metadata(downloaded)
    title = metadata.title if metadata and metadata.title else ""

    if not title:
        soup = BeautifulSoup(downloaded, "html.parser")
        if soup.title:
            title = soup.title.get_text(" ", strip=True)

    if not text or len(text.strip()) < 100:
        raise Exception(
            "Could not extract enough article content."
        )

    if not title:
        raise Exception("Article title not found.")

    return title, text
