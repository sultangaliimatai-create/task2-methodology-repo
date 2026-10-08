import os
import pandas as pd
import yaml

def run_benchmark():
    config_path = "configs/config.yaml"
    if not os.path.exists(config_path):
        print(f"Error: Config file not found at {config_path}")
        return

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    data_path = config.get("data_path", "data/sample/sample_data.csv")
    df = pd.read_csv(data_path)

    print("=== Benchmark Run Successful ===")
    print(f"Loaded {len(df)} sample records.")
    print(f"Average Procrastination Score: {df['procrastination_score'].mean():.2f}")

if __name__ == "__main__":
    run_benchmark()
