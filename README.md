# The Interconnection Between Short-Form Video Consumption and Academic Procrastination

## Authors
- Imatay Sultangali
- Muzappar Shyntas

## Research Question
Does daily short-form video consumption (Shorts/Reels/TikTok) significantly correlate with and predict academic procrastination levels among university students?

## Repository Structure
├── configs/
│   └── config.yaml
├── data/
│   └── sample/
│       └── sample_data.csv
├── src/
│   └── benchmark.py
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
## Planned Benchmarks
| Benchmark | Description | Target Metric |
|---|---|---|
| Sample Data Test | Execution of basic processing script | Script Execution Time / Status |
| Correlation Test | Pearson/Spearman correlation analysis | Correlation Coefficient (r) |
| Group Comparison | T-test between moderate (<=1h) & heavy (>3h) users | p-value / Cohen's d |

## Quickstart Guide
To run the test benchmark on the sample dataset:

1. Clone the repository:
   ```bash
   git clone [https://github.com/sultangaliimatai-create/task2-methodology-repo.git](https://github.com/sultangaliimatai-create/task2-methodology-repo.git)
   cd task2-methodology-repo
   pip install -r requirements.txt
   python src/benchmark.py
