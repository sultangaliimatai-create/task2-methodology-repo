"""Clean and summarize simulated student survey data."""

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw" / "synthetic_student_survey.jsonl"
PROCESSED_DIR = ROOT / "data" / "processed"


def load_data():
    with RAW_PATH.open("r", encoding="utf-8") as file:
        records = [json.loads(line) for line in file if line.strip()]
    return pd.DataFrame(records)


def process_data():
    raw = load_data()

    required = {
        "student_id",
        "daily_video_hours",
        "during_study",
        "study_year",
        "simulated_procrastination_score",
        "data_type",
    }

    missing = required - set(raw.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    original_count = len(raw)
    data = raw.drop_duplicates(subset="student_id").copy()

    data["daily_video_hours"] = pd.to_numeric(
        data["daily_video_hours"], errors="coerce"
    )
    data["simulated_procrastination_score"] = pd.to_numeric(
        data["simulated_procrastination_score"], errors="coerce"
    )

    valid = (
        data["daily_video_hours"].between(0, 24)
        & data["simulated_procrastination_score"].between(1, 5)
        & data["during_study"].isin(["Yes", "No"])
    )
    clean = data.loc[valid].copy()

    clean["consumption_group"] = pd.cut(
        clean["daily_video_hours"],
        bins=[-np.inf, 1, 3, np.inf],
        labels=["Baseline (<=1 h/day)", "Middle (1-3 h/day)", "Heavy (>3 h/day)"],
    )

    rows = [
        {
            "section": "data_quality",
            "group": "all",
            "metric": "records_loaded",
            "value": original_count,
        },
        {
            "section": "data_quality",
            "group": "all",
            "metric": "records_analyzed",
            "value": len(clean),
        },
        {
            "section": "data_quality",
            "group": "all",
            "metric": "duplicate_ids_removed",
            "value": original_count - len(data),
        },
        {
            "section": "data_quality",
            "group": "all",
            "metric": "invalid_records_removed",
            "value": len(data) - len(clean),
        },
    ]

    for group_name, group in clean.groupby("consumption_group", observed=True):
        scores = group["simulated_procrastination_score"]
        rows.extend(
            [
                {
                    "section": "descriptive",
                    "group": str(group_name),
                    "metric": "n",
                    "value": len(group),
                },
                {
                    "section": "descriptive",
                    "group": str(group_name),
                    "metric": "mean_score",
                    "value": scores.mean(),
                },
                {
                    "section": "descriptive",
                    "group": str(group_name),
                    "metric": "median_score",
                    "value": scores.median(),
                },
            ]
        )

    x = clean["daily_video_hours"]
    y = clean["simulated_procrastination_score"]
    correlation, correlation_p = stats.pearsonr(x, y)

    rows.extend(
        [
            {
                "section": "association",
                "group": "all",
                "metric": "pearson_r",
                "value": correlation,
            },
            {
                "section": "association",
                "group": "all",
                "metric": "pearson_p_value",
                "value": correlation_p,
            },
        ]
    )

    baseline = clean.loc[
        clean["daily_video_hours"] <= 1,
        "simulated_procrastination_score",
    ]
    heavy = clean.loc[
        clean["daily_video_hours"] > 3,
        "simulated_procrastination_score",
    ]

    if len(baseline) >= 2 and len(heavy) >= 2:
        t_stat, t_p = stats.ttest_ind(heavy, baseline, equal_var=False)
        rows.extend(
            [
                {
                    "section": "group_comparison",
                    "group": "heavy_vs_baseline",
                    "metric": "welch_t_statistic",
                    "value": t_stat,
                },
                {
                    "section": "group_comparison",
                    "group": "heavy_vs_baseline",
                    "metric": "welch_p_value",
                    "value": t_p,
                },
            ]
        )

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    clean.to_csv(
        PROCESSED_DIR / "cleaned_synthetic_students.csv",
        index=False,
    )
    pd.DataFrame(rows).to_csv(
        PROCESSED_DIR / "metrics_summary.csv",
        index=False,
    )

    print(f"Records loaded: {original_count}")
    print(f"Records analyzed: {len(clean)}")
    print("Summary saved to data/processed/metrics_summary.csv")
    print("SIMULATION ONLY: these are not real student survey results.")


if __name__ == "__main__":
    process_data()