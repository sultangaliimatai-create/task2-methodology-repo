import os
import json
import numpy as np
import pandas as pd
from scipy import stats

def run_benchmark():
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)

    print("Running benchmark data generation & collection...")
    
    np.random.seed(42)
    n_samples = 100
    daily_hours = np.random.exponential(scale=2.0, size=n_samples).round(2)
    pass_score = (15 + 2.5 * daily_hours + np.random.normal(0, 3, n_samples)).round(1)

    df = pd.DataFrame({
        "student_id": range(1, n_samples + 1),
        "daily_video_hours": daily_hours,
        "pass_procrastination_score": pass_score
    })

    raw_log_path = "data/raw/benchmark_run.jsonl"
    with open(raw_log_path, "w") as f:
        for idx, row in df.iterrows():
            log_entry = {
                "phase": "warmup" if idx < 10 else "benchmark",
                "student_id": int(row["student_id"]),
                "daily_hours": float(row["daily_video_hours"]),
                "pass_score": float(row["pass_procrastination_score"])
            }
            f.write(json.dumps(log_entry) + "\n")
    print(f"Raw logs saved to {raw_log_path}")

    df_clean = df.iloc[10:].copy()
    
    r_val, p_val = stats.pearsonr(df_clean["daily_video_hours"], df_clean["pass_procrastination_score"])

    moderate = df_clean[df_clean["daily_video_hours"] <= 1.0]["pass_procrastination_score"]
    heavy = df_clean[df_clean["daily_video_hours"] > 3.0]["pass_procrastination_score"]
    t_stat, t_pval = stats.ttest_ind(heavy, moderate, equal_var=False)

    summary_df = pd.DataFrame([{
        "sample_size": len(df_clean),
        "pearson_r": round(r_val, 4),
        "pearson_p_value": round(p_val, 4),
        "t_statistic": round(t_stat, 4),
        "t_p_value": round(t_pval, 4),
        "moderate_mean_score": round(moderate.mean(), 2),
        "heavy_mean_score": round(heavy.mean(), 2)
    }])

    summary_path = "data/processed/metrics_summary.csv"
    summary_df.to_csv(summary_path, index=False)
    print(f"Processed metrics successfully written to {summary_path}")
    print(summary_df.to_string())

if __name__ == "__main__":
    run_benchmark()
