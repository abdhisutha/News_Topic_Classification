import mlflow

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("News_Topic_Classification")

with mlflow.start_run():

    mlflow.log_param("model", "BERT")
    mlflow.log_param("dataset", "AG News")
    mlflow.log_param("train_samples", 1000)
    mlflow.log_param("test_samples", 200)
    mlflow.log_param("epochs", 1)

    mlflow.log_metric("accuracy", 0.90)
    mlflow.log_metric("precision", 0.9043)
    mlflow.log_metric("recall", 0.90)
    mlflow.log_metric("f1_score", 0.9012)

print("BERT results logged to MLflow!")