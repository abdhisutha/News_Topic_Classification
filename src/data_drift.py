import pandas as pd
from evidently import Report
from evidently.presets import DataDriftPreset
import os

project_path = r"C:\Users\abdhi\PycharmProjects\News_Topic_Classification"

reference_path = os.path.join(
    project_path, "data", "drift", "reference.csv"
)

current_path = os.path.join(
    project_path, "data", "drift", "current.csv"
)

report_path = os.path.join(
    project_path, "reports", "data_drift.html"
)

reference = pd.read_csv(reference_path)
current = pd.read_csv(current_path)

reference = reference[["label", "text_length"]]
current = current[["label", "text_length"]]

report = Report([
    DataDriftPreset()
])

result = report.run(
    reference_data=reference,
    current_data=current
)

os.makedirs(
    os.path.dirname(report_path),
    exist_ok=True
)

result.save_html(report_path)

print("Data Drift Report generated successfully!")
print("Report saved at:")
print(report_path)