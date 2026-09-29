from news_extractor import extract_article

url = input("Enter news article URL: ")

title, text = extract_article(url)

print("\nTitle:")
print(title)

print("\nArticle:")
print(text)