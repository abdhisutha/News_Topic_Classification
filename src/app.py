from news_extractor import extract_article
from translator import translate_to_english
from topic_filter import check_topic
from summarizer import summarize_text


url = input("Enter news article URL: ")
keyword = input("Enter topic/keyword: ")

title, article = extract_article(url)

print("\nTitle:")
print(title)

language, english_text = translate_to_english(article)

print("\nDetected Language:", language)

if check_topic(english_text, keyword):
    print("Status: Relevant")

    summary = summarize_text(english_text, 3)

    print("\nSummary:")
    print(summary)

else:
    print("Status: Not Relevant")