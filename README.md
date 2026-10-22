# Short-Video Consumption and Academic Procrastination Analysis

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python Version](https://img.shields.io/badge/Python-3.11-blue.svg)
![Reproducibility Status](https://img.shields.io/badge/Reproducibility-100%25-brightgreen.svg)

## 📌 Authors & Project Profile
* **Authors:** Imatai Sultangali, Myzappar Shyntas
* **Research Type:** Quantitative Research (Correlational and Causal-Comparative)
* **GitHub Repository:** [task2-methodology-repo](https://github.com/sultangaliimatai-create/task2-methodology-repo)

---

## 🔬 Project Overview & Research Aim
This repository contains the methodology, benchmark testbed, data pipeline, and statistical validation scripts for analyzing the relationship between short-form video consumption (TikTok, Instagram Reels, YouTube Shorts) and academic procrastination among university students.

### Research Questions & Hypotheses
* **RQ1 (Descriptive):** How common is academic procrastination, and how much time do students spend watching short videos?
  * $H_0$: $\le 50\%$ of students report moderate-to-high academic procrastination.
  * $H_1$: $> 50\%$ of students report moderate-to-high academic procrastination.
* **RQ2 (Correlational):** Is there a positive relationship between daily short-video consumption and PASS procrastination scores?
  * $H_0$: Pearson correlation $r = 0$.
  * $H_1$: Pearson correlation $r > 0$.
* **RQ3 (Causal-Comparative):** Do heavy consumers (>3 hours/day) have significantly higher procrastination scores than moderate consumers ($\le 1$ hour/day)?
  * $H_0$: $\mu_{\text{heavy}} = \mu_{\text{moderate}}$.
  * $H_1$: $\mu_{\text{heavy}} > \mu_{\text{moderate}}$.

---

## 📂 Repository Structure
```text
task2-methodology-repo/
├── .gitignore               # Excludes binary data, logs, and temp files
├── LICENSE                  # Open-source MIT License
├── README.md                # Project documentation and reproducibility guide
├── requirements.txt         # Explicitly pinned Python package dependencies
├── configs/
│   └── config.yaml          # Research parameters, thresholds, and file paths
├── data/
│   ├── raw/                 # Raw unedited logs and survey data (.jsonl / .csv)
│   ├── processed/           # Aggregated clean metrics (metrics_summary.csv)
│   └── sample/
│       └── sample_data.csv  # Synthetic survey test sample
├── notebooks/               # Exploratory data analysis notebooks
├── models/                  # Saved statistical models and reliability metrics
├── reports/
│   └── figures/             # Publication-grade vector (.pdf) and raster (.png) plots
└── src/
    ├── benchmark.py         # Synthetic survey data generation & PASS score calculation
    ├── process_data.py      # Log cleaning, warm-up filtering, and outlier detection
    └── visualize.py         # Publication-ready plots (Axes, CI, Colorblind-safe)
