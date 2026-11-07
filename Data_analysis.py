"""Descriptive analysis for the Hospital Analytics Dashboard project."""
from pathlib import Path
import json
import pandas as pd

try:
    ROOT = Path(__file__).resolve().parent
except NameError:
    ROOT = Path.cwd()

# Pointing directly to the file available in your workspace root
DATA_FILE = ROOT / "cleaned_hospital_patient_data.csv"
OUT_DIR = ROOT / "analysis_outputs"
OUT_DIR.mkdir(exist_ok=True)

def main():
    df = pd.read_csv(DATA_FILE)
    numeric = df.select_dtypes(include="number")
    summary = {
        "records": int(len(df)),
        "columns": int(len(df.columns)),
        "exact_duplicate_rows": int(df.duplicated().sum()),
        "missing_cells": int(df.isna().sum().sum()),
        "mean_age": round(float(df["Age"].mean()), 2) if "Age" in df else None,
        "median_age": round(float(df["Age"].median()), 2) if "Age" in df else None,
        "mean_length_of_stay": round(float(df["Length_of_Stay"].mean()), 2) if "Length_of_Stay" in df else None,
        "mean_total_cost": round(float(df["Total_Cost"].mean()), 2) if "Total_Cost" in df else None,
        "mean_satisfaction": round(float(df["Satisfaction"].mean()), 2) if "Satisfaction" in df else None,
    }
    for col in ["Condition", "Gender", "Outcome", "Readmission", "Patient_State"]:
        if col in df:
            summary[f"{col.lower()}_counts"] = {str(k): int(v) for k, v in df[col].value_counts(dropna=False).items()}

    (OUT_DIR / "analysis_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    df.describe(include="all").transpose().to_csv(OUT_DIR / "descriptive_statistics.csv")
    profile = pd.DataFrame({
        "data_type": df.dtypes.astype(str),
        "non_missing": df.notna().sum(),
        "missing": df.isna().sum(),
        "unique_values": df.nunique(dropna=True)
    })
    profile.to_csv(OUT_DIR / "data_quality_profile.csv")
    for col in ["Condition", "Gender", "Outcome", "Readmission", "Insurance_Claimed", "Patient_State", "Medication"]:
        if col in df:
            df[col].value_counts(dropna=False).rename_axis(col).reset_index(name="count").to_csv(
                OUT_DIR / f"frequency_{col}.csv", index=False
            )
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()