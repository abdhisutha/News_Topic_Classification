from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

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

MODEL_PATH = str(
    Path(__file__).resolve().parent.parent
    / "src" / "models" / "bert_agnews"
)
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

labels = {
    0: "World",
    1: "Sports",
    2: "Business",
    3: "Technology"
}


class NewsRequest(BaseModel):
    url: str
    topic: str


@app.get("/")
def home():
    return {"message": "News Topic Classification API is running"}


@app.post("/analyze")
def analyze_news(request: NewsRequest):
    try:
        title, article = extract_article(request.url)
    except Exception:
        raise HTTPException(
            status_code=422,
            detail="Could not extract the article. Try another news article URL."
        )
    try:
        language, english_text = translate_to_english(article)
    except ValueError as error:
        raise HTTPException(status_code=503, detail=str(error))
    
    inputs = tokenizer(
        english_text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )

    with torch.no_grad():
        output = model(**inputs)

    prediction = torch.argmax(output.logits, dim=1).item()
    predicted_topic = labels[prediction]

    relevant = (
            predicted_topic.lower() == request.topic.strip().lower()
            and check_topic(english_text, request.topic)
    )
    if relevant:
        summary = summarize_text(
            english_text,
            request.topic,
            3
        )
        return {
            "title": title,
            "language": language,
            "predicted_topic": predicted_topic,
            "topic": request.topic,
            "status": "Relevant",
            "summary": summary
        }

    return {
        "title": title,
        "language": language,
        "predicted_topic": predicted_topic,
        "topic": request.topic,
        "status": "Not Relevant",
        "summary": ""
    }