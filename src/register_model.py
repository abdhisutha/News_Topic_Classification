import mlflow
import os
from transformers import AutoModelForSequenceClassification, AutoTokenizer

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("News_Topic_Classification")

model_path = r"C:\Users\abdhi\PycharmProjects\News_Topic_Classification\src\models\bert_agnews"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

with mlflow.start_run() as run:

    mlflow.log_param("model", "BERT")
    mlflow.log_param("dataset", "AG News")
    mlflow.log_param("train_samples", 1000)
    mlflow.log_param("test_samples", 200)
    mlflow.log_param("epochs", 1)

    mlflow.log_metric("accuracy", 0.90)
    mlflow.log_metric("precision", 0.9043)
    mlflow.log_metric("recall", 0.90)
    mlflow.log_metric("f1_score", 0.9012)

    components = {
        "model": model,
        "tokenizer": tokenizer
    }

    model_info = mlflow.transformers.log_model(
        transformers_model=components,
        name="bert_model",
        task="text-classification",
        registered_model_name="News_Topic_BERT"
    )

    print("Run ID:", run.info.run_id)
    print("Model URI:", model_info.model_uri)

print("BERT model registered successfully!")