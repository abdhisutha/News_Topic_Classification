import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_PATH = "abdhisutha/newsai-bert-agnews"

st.set_page_config(
    page_title="NEWSAI - News Classifier",
    page_icon="📰",
    layout="centered"
)

st.title("📰 NEWSAI")
st.subheader("AI-Powered News Topic Classification")
st.write("Classify news articles using your trained BERT model.")

@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
    model.eval()
    return tokenizer, model

try:
    with st.spinner("Loading BERT model..."):
        tokenizer, model = load_model()

    article = st.text_area(
        "Paste your news article here",
        height=220,
        placeholder="Enter news content..."
    )

    if st.button("Analyze News", use_container_width=True):
        if article.strip():
            inputs = tokenizer(
                article,
                return_tensors="pt",
                truncation=True,
                padding=True,
                max_length=512
            )

            with torch.no_grad():
                outputs = model(**inputs)

            prediction = torch.argmax(outputs.logits, dim=1).item()

            categories = {
                0: "World",
                1: "Sports",
                2: "Business",
                3: "Technology"
            }

            st.success(f"Predicted Category: {categories[prediction]}")
        else:
            st.warning("Please enter a news article.")

except Exception as e:
    st.error(f"Model loading failed: {e}")
