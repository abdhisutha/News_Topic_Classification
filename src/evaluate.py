from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import torch

dataset = load_dataset("sh0416/ag_news")

test_data = dataset["test"].select(range(200))

test_data = test_data.map(lambda x: {"label": x["label"] - 1})

tokenizer = AutoTokenizer.from_pretrained("models/bert_agnews")
model = AutoModelForSequenceClassification.from_pretrained(
    "models/bert_agnews"
)

predictions = []
actual = []

for item in test_data:

    text = item["title"] + " " + item["description"]

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )

    with torch.no_grad():
        output = model(**inputs)

    prediction = torch.argmax(output.logits, dim=1).item()

    predictions.append(prediction)
    actual.append(item["label"])

print("Accuracy:", round(accuracy_score(actual, predictions) * 100, 2), "%")
print("Precision:", round(precision_score(
    actual, predictions, average="weighted", zero_division=0
) * 100, 2), "%")
print("Recall:", round(recall_score(
    actual, predictions, average="weighted", zero_division=0
) * 100, 2), "%")
print("F1 Score:", round(f1_score(
    actual, predictions, average="weighted", zero_division=0
) * 100, 2), "%")