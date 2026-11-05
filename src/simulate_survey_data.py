"""Create simulated data for demonstrating the Task 3 analysis.

These are not real survey responses and must not be presented as real findings.
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw" / "synthetic_student_survey.jsonl"
CSV_PATH = ROOT / "data" / "sample" / "synthetic_student_survey.csv"


def generate_synthetic_data(n=120, seed=42):
    rng = np.random.default_rng(seed)

    daily_hours = np.clip(
        rng.lognormal(mean=0.35, sigma=0.7, size=n),
        0,
        8,
    )

    probability = 1 / (1 + np.exp(-(-1.2 + 0.45 * daily_hours)))
    during_study = rng.binomial(1, probability, size=n)

    score = np.clip(
        2.5
        + 0.24 * daily_hours
        + 0.35 * during_study
        + rng.normal(0, 0.65, size=n),
        1,
        5,
    )

    return pd.DataFrame(
        {
            "student_id": [f"S{i:03d}" for i in range(1, n + 1)],
            "daily_video_hours": np.round(daily_hours, 2),
            "during_study": np.where(during_study == 1, "Yes", "No"),
            "study_year": rng.choice([1, 2, 3, 4], size=n),
            "simulated_procrastination_score": np.round(score, 2),
            "data_type": "synthetic_simulation",
        }
    )


def main():
    RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)

    data = generate_synthetic_data()

    with RAW_PATH.open("w", encoding="utf-8") as file:
        for record in data.to_dict(orient="records"):
            file.write(json.dumps(record) + "\n")

    data.to_csv(CSV_PATH, index=False)

    print(f"Created {len(data)} simulated records.")
    print(f"CSV file: {CSV_PATH.relative_to(ROOT)}")
    print("Reminder: these are simulated records, not real survey results.")


if __name__ == "__main__":
    main()