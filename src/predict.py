from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

model_path = "models/bert_agnews"

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

labels = ["World", "Sports", "Business", "Sci/Tech"]

article = input("Enter news article: ")

inputs = tokenizer(
    article,
    return_tensors="pt",
    truncation=True,
    padding=True,
    max_length=128
)

with torch.no_grad():
    output = model(**inputs)

prediction = torch.argmax(output.logits, dim=1).item()

print("\nPredicted Topic:", labels[prediction])