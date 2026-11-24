from api.news_routes import router as news_router
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)

from deep_translator import GoogleTranslator

import torch

from src.news_extractor import extract_article
from src.translator import translate_to_english
from src.topic_filter import check_topic
from src.summarizer import summarize_text


app = FastAPI(title="News Topic Classification API")
app.include_router(news_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


# Load BERT model
MODEL_PATH = "https://huggingface.co/abdhisutha/newsai-bert-agnews/tree/main"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_PATH
)

model.eval()


# Category labels
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
    return {
        "message": "News Topic Classification API is running"
    }


@app.post("/analyze")
def analyze_news(request: NewsRequest):

    # Step 1: Extract article
    try:
        title, article = extract_article(request.url)

    except Exception as error:
        raise HTTPException(
            status_code=422,
            detail=str(error)
        )

    # Step 2: Detect language and translate for BERT
    try:
        language, english_text = translate_to_english(article)

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error)
        )

    # Step 3: Generate summary from original article
    original_summary = summarize_text(
        article,
        request.topic,
        3
    )


    # Step 4: Prepare summaries based on original language
    if language == "en":
        english_summary = original_summary
        telugu_summary = None

    elif language == "te":
        telugu_summary = original_summary

        try:
            english_summary = GoogleTranslator(
                source="auto",
                target="en"
            ).translate(telugu_summary)

        except Exception as error:
            print("English summary translation failed:", error)
            english_summary = "English summary is temporarily unavailable."

    else:
        english_summary = original_summary
        telugu_summary = None

    # Step 5: Handle translation failure for classification
    if not english_text:

        return {
            "title": title,
            "language": language,
            "predicted_topic": "Unavailable",
            "topic": request.topic,
            "status": "Classification unavailable - translation failed",
            "summary": {
                "original_language": original_summary,
                "telugu": telugu_summary,
                "english": english_summary
            }
        }

    # Step 6: BERT category prediction
    inputs = tokenizer(
        english_text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )

    with torch.no_grad():
        output = model(**inputs)

    prediction = torch.argmax(
        output.logits,
        dim=1
    ).item()

    predicted_topic = labels[prediction]

    # Step 7: Check selected category
    relevant = (
        predicted_topic.lower() == request.topic.strip().lower()
        and check_topic(english_text, request.topic)
    )

    if relevant:
        status = "Relevant"

        summary = {
            "original_language": original_summary,
            "telugu": telugu_summary,
            "english": english_summary
        }

    else:
        status = "Not Relevant"
        summary = {
            "original_language": "",
            "telugu": "",
            "english": ""
        }

    # Step 8: Final response
    return {
        "title": title,
        "language": language,
        "predicted_topic": predicted_topic,
        "topic": request.topic,
        "status": status,
        "summary": summary
    }
