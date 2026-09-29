from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.news_extractor import extract_article
from src.translator import translate_to_english
from src.topic_filter import check_topic
from src.summarizer import summarize_text

app = FastAPI(title="News Topic Classification API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


class NewsRequest(BaseModel):
    url: str
    topic: str


@app.get("/")
def home():
    return {"message": "News Topic Classification API is running"}


@app.post("/analyze")
def analyze_news(request: NewsRequest):

    title, article = extract_article(request.url)

    language, english_text = translate_to_english(article)
    print("TITLE:", title)
    print("ARTICLE LENGTH:", len(article))
    print("ARTICLE TEXT:", article[:1000])
    print("LANGUAGE:", language)
    print("ENGLISH TEXT:", english_text[:1000])

    relevant = check_topic(
        english_text,
        request.topic
    )
    print("TOPIC:", request.topic)
    print("ARTICLE TEXT:", english_text[:1000])
    print("RELEVANT:", relevant)

    if relevant:
        summary = summarize_text(
            english_text,
            3
        )

        return {
            "title": title,
            "language": language,
            "topic": request.topic,
            "status": "Relevant",
            "summary": summary
        }

    return {
        "title": title,
        "language": language,
        "topic": request.topic,
        "status": "Not Relevant",
        "summary": ""
    }