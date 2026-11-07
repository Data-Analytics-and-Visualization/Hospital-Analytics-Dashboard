"""
Hospital Patient Data Visualisation
Generates aggregate charts from the cleaned hospital dataset.
No patient-level records are displayed.
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# Locate the project folder and cleaned dataset.
try:
    BASE_DIR = Path(__file__).resolve().parent
except NameError:
    BASE_DIR = Path.cwd()

possible_paths = [
    BASE_DIR / "cleaned_hospital_patient_data.csv",
    BASE_DIR / "clean_dataset" / "cleaned_hospital_patient_data.csv",
]

DATA_PATH = next((path for path in possible_paths if path.exists()), None)

if DATA_PATH is None:
    raise FileNotFoundError(
        "Could not find cleaned_hospital_patient_data.csv. "
        "Place it beside this script or inside the clean_dataset folder."
    )

OUTPUT_DIR = BASE_DIR / "analysis_outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA_PATH)

required_columns = [
    "Condition", "Age", "Length_of_Stay", "Total_Cost",
    "Readmission", "Outcome", "Insurance_Claimed", "Satisfaction"
]
missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    raise ValueError(f"Missing required dataset columns: {missing_columns}")

print("Dataset loaded:", DATA_PATH.name)
print("Dataset shape:", df.shape)


def save_chart(filename):
    """Save the current chart and close its figure."""
    plt.tight_layout()
    output_path = OUTPUT_DIR / filename
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    print("Saved:", output_path)
    plt.close()


# 1. Patient records by medical condition
df["Condition"].value_counts().plot(
    kind="bar",
    figsize=(8, 4),
    title="Patient Records by Condition"
)
plt.xlabel("Condition")
plt.ylabel("Records")
plt.xticks(rotation=35, ha="right")
save_chart("patients_by_condition.png")


# 2. Age distribution
df["Age"].dropna().plot(
    kind="hist",
    bins=18,
    edgecolor="black",
    figsize=(8, 4),
    title="Age Distribution"
)
plt.xlabel("Age")
plt.ylabel("Frequency")
save_chart("age_distribution.png")


# 3. Average length of stay by condition
df.groupby("Condition")["Length_of_Stay"].mean().sort_values().plot(
    kind="barh",
    figsize=(8, 4),
    title="Average Length of Stay by Condition"
)
plt.xlabel("Average Length of Stay")
plt.ylabel("Condition")
save_chart("average_length_of_stay_by_condition.png")


# 4. Average total cost by condition
df.groupby("Condition")["Total_Cost"].mean().sort_values().plot(
    kind="barh",
    figsize=(8, 4),
    title="Average Total Cost by Condition"
)
plt.xlabel("Average Total Cost")
plt.ylabel("Condition")
save_chart("average_cost_by_condition.png")


# 5. Readmission, outcome and insurance-claim distributions
for column in ["Readmission", "Outcome", "Insurance_Claimed"]:
    df[column].value_counts().plot(
        kind="bar",
        figsize=(7, 4),
        title=f"{column} Distribution"
    )
    plt.xlabel(column)
    plt.ylabel("Records")
    plt.xticks(rotation=25, ha="right")
    save_chart(f"{column.lower()}_distribution.png")


# 6. Patient satisfaction scores
df["Satisfaction"].value_counts().sort_index().plot(
    kind="bar",
    figsize=(7, 4),
    title="Patient Satisfaction Scores"
)
plt.xlabel("Satisfaction Score")
plt.ylabel("Records")
save_chart("patient_satisfaction_scores.png")

print(f"\nVisualisation completed. Charts saved in: {OUTPUT_DIR}")