from newspaper import Article


def extract_article(url):
    url = url.strip()

    if url.lower().startswith("url:"):
        url = url[4:].strip()

    article = Article(url)

    article.download()
    article.parse()

    return article.title, article.text