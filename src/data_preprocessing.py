from datasets import load_dataset
from transformers import AutoTokenizer

dataset = load_dataset("sh0416/ag_news")

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

def preprocess(examples):
    text = [
        title + " " + description
        for title, description in zip(examples["title"], examples["description"])
    ]
    return tokenizer(text, truncation=True, padding="max_length", max_length=128)

tokenized_data = dataset.map(preprocess, batched=True)

print(tokenized_data)
print(tokenized_data["train"][0])