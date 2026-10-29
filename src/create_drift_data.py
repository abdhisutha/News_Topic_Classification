from datasets import load_from_disk
import pandas as pd
import os

project_path = r"C:\Users\abdhi\PycharmProjects\News_Topic_Classification"

data_path = os.path.join(project_path, "data", "raw", "ag_news")
drift_path = os.path.join(project_path, "data", "drift")

data = load_from_disk(data_path)

train = pd.DataFrame(data["train"])
test = pd.DataFrame(data["test"])

reference = train.sample(500, random_state=42)
current = test.sample(500, random_state=10)

reference["text_length"] = (
    reference["title"].fillna("") + " " +
    reference["description"].fillna("")
).str.len()

current["text_length"] = (
    current["title"].fillna("") + " " +
    current["description"].fillna("")
).str.len()

os.makedirs(drift_path, exist_ok=True)

reference.to_csv(
    os.path.join(drift_path, "reference.csv"),
    index=False
)

current.to_csv(
    os.path.join(drift_path, "current.csv"),
    index=False
)

print("Reference data:", len(reference))
print("Current data:", len(current))
print("Drift datasets created successfully!")