
import requests
import trafilatura
from bs4 import BeautifulSoup
from newspaper import Article


def extract_article(url):
    url = url.strip()

    if not url.startswith(("http://", "https://")):
        raise Exception("Please enter a valid article URL.")

    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(
            url, headers=headers, timeout=20
        )
        response.raise_for_status()

        text = trafilatura.extract(
            response.text,
            include_comments=False,
            include_tables=False
        )

        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.get_text(" ", strip=True) if soup.title else ""

        if text and len(text) > 100 and title:
            return title, text
    except Exception:
        pass

    try:
        article = Article(url)
        article.download()
        article.parse()

        if article.text and len(article.text) > 100 and article.title:
            return article.title, article.text
    except Exception:
        pass

    try:
        amp_url = url.rstrip("/") + "/amp/"
        response = requests.get(
            amp_url, headers=headers, timeout=20
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.find("h1").get_text(" ", strip=True) if soup.find("h1") else ""

        text = " ".join(
            p.get_text(" ", strip=True)
            for p in soup.find_all("p")
        )

        if len(text) > 100 and title:
            return title, text
    except Exception:
        pass

    raise Exception(
        "Could not extract the article. Try another news article URL."
    )
