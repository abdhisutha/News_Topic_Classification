
import os
import mlflow
import torch
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

MODEL_PATH = "./src/models/bert_agnews"
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("Model folder not found: " + MODEL_PATH)

mlflow.set_tracking_uri("file:./mlruns_review")
mlflow.set_experiment("News_Topic_Classification")

dataset = load_dataset("sh0416/ag_news")
test_data = dataset["test"].select(range(200))

texts = [
    title + " " + description
    for title, description in zip(
        test_data["title"], test_data["description"]
    )
]
actual = [label - 1 for label in test_data["label"]]

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()

predicted = []

for i in range(0, len(texts), 8):
    inputs = tokenizer(
        texts[i:i+8],
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )

    with torch.no_grad():
        outputs = model(**inputs)

    predicted.extend(outputs.logits.argmax(dim=1).tolist())

accuracy = accuracy_score(actual, predicted)
precision = precision_score(actual, predicted, average="macro", zero_division=0)
recall = recall_score(actual, predicted, average="macro", zero_division=0)
f1 = f1_score(actual, predicted, average="macro", zero_division=0)

with mlflow.start_run(run_name="BERT_Existing_Model_Evaluation"):
    mlflow.log_param("model", "bert-base-uncased")
    mlflow.log_param("dataset", "AG News")
    mlflow.log_param("test_samples", 200)

    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("precision", precision)
    mlflow.log_metric("recall", recall)
    mlflow.log_metric("f1_score", f1)

    mlflow.log_artifacts(MODEL_PATH, artifact_path="model")

print("MLflow run completed!")
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)
