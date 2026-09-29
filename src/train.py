from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import TrainingArguments, Trainer

dataset = load_dataset("sh0416/ag_news")

train_data = dataset["train"].select(range(1000))
test_data = dataset["test"].select(range(200))

train_data = train_data.map(lambda x: {"label": x["label"] - 1})
test_data = test_data.map(lambda x: {"label": x["label"] - 1})

print("Train labels:", sorted(set(train_data["label"])))
print("Test labels:", sorted(set(test_data["label"])))

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")


def preprocess(examples):
    text = [
        title + " " + description
        for title, description in zip(
            examples["title"],
            examples["description"]
        )
    ]

    return tokenizer(
        text,
        truncation=True,
        padding="max_length",
        max_length=128
    )


train_data = train_data.map(preprocess, batched=True)
test_data = test_data.map(preprocess, batched=True)

train_data = train_data.rename_column("label", "labels")
test_data = test_data.rename_column("label", "labels")

train_data.set_format("torch")
test_data.set_format("torch")

model = AutoModelForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    num_labels=4
)

training_args = TrainingArguments(
    output_dir="./models/bert_agnews",
    num_train_epochs=1,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    eval_strategy="epoch",
    save_strategy="no",
    logging_steps=50,
    report_to="none"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_data,
    eval_dataset=test_data
)

trainer.train()

trainer.save_model("./models/bert_agnews")
tokenizer.save_pretrained("./models/bert_agnews")

print("Model saved successfully!")
print("Training completed!")