"""Create publication-style figures from simulated survey data."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed" / "cleaned_synthetic_students.csv"
FIGURES_DIR = ROOT / "reports" / "figures"
RNG = np.random.default_rng(42)


def bootstrap_mean_ci(values, n_boot=2000):
    """Calculate a percentile 95% bootstrap confidence interval."""
    values = np.asarray(values, dtype=float)
    samples = RNG.choice(values, size=(n_boot, len(values)), replace=True)
    means = samples.mean(axis=1)
    return np.quantile(means, [0.025, 0.975])


def main():
    data = pd.read_csv(DATA_PATH)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    # Figure 1: viewing time and simulated score
    x = data["daily_video_hours"].to_numpy()
    y = data["simulated_procrastination_score"].to_numpy()
    x_grid = np.linspace(x.min(), x.max(), 100)

    slope, intercept = np.polyfit(x, y, 1)
    fitted_line = slope * x_grid + intercept

    boot_lines = []
    for _ in range(1000):
        indexes = RNG.choice(len(data), size=len(data), replace=True)
        sample_x = x[indexes]
        sample_y = y[indexes]

        if np.unique(sample_x).size > 1:
            sample_slope, sample_intercept = np.polyfit(sample_x, sample_y, 1)
            boot_lines.append(sample_slope * x_grid + sample_intercept)

    ci_low, ci_high = np.percentile(boot_lines, [2.5, 97.5], axis=0)

    fig, ax = plt.subplots(figsize=(8, 5))
    colors = {"No": "#0072B2", "Yes": "#D55E00"}

    for answer, color in colors.items():
        subset = data["during_study"] == answer
        ax.scatter(
            x[subset],
            y[subset],
            color=color,
            label=f"During study: {answer}",
            alpha=0.75,
        )

    ax.plot(x_grid, fitted_line, color="black", label="Fitted trend")
    ax.fill_between(
        x_grid,
        ci_low,
        ci_high,
        color="gray",
        alpha=0.25,
        label="95% bootstrap interval",
    )
    ax.set_title("Simulated video use and procrastination score")
    ax.set_xlabel("Short-video use (hours per day)")
    ax.set_ylabel("Simulated procrastination score (1–5)")
    ax.legend()
    ax.text(
        0.02,
        0.02,
        "Simulation only — not real survey results",
        transform=ax.transAxes,
        fontsize=8,
    )
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "video_hours_vs_score.png", dpi=300)
    fig.savefig(FIGURES_DIR / "video_hours_vs_score.pdf")
    plt.close(fig)

    # Figure 2: score distributions and group mean confidence intervals
    group_names = [
        "Baseline (<=1 h/day)",
        "Middle (1-3 h/day)",
        "Heavy (>3 h/day)",
    ]
    groups = [
        data.loc[
            data["consumption_group"] == name,
            "simulated_procrastination_score",
        ].dropna().to_numpy()
        for name in group_names
    ]

    fig, ax = plt.subplots(figsize=(8, 5))
    boxplot = ax.boxplot(groups, patch_artist=True)

    palette = ["#0072B2", "#E69F00", "#009E73"]
    for box, color in zip(boxplot["boxes"], palette):
        box.set_facecolor(color)
        box.set_alpha(0.65)

    means = [values.mean() for values in groups]
    intervals = [bootstrap_mean_ci(values) for values in groups]
    lower_errors = [mean - interval[0] for mean, interval in zip(means, intervals)]
    upper_errors = [interval[1] - mean for mean, interval in zip(means, intervals)]

    ax.errorbar(
        [1, 2, 3],
        means,
        yerr=[lower_errors, upper_errors],
        fmt="D",
        color="black",
        capsize=5,
        label="Mean ± 95% bootstrap CI",
    )
    ax.set_xticks([1, 2, 3])
    ax.set_xticklabels(group_names, rotation=10)
    ax.set_title("Simulated scores by video-use group")
    ax.set_xlabel("Short-video use group")
    ax.set_ylabel("Simulated procrastination score (1–5)")
    ax.legend()
    ax.text(
        0.02,
        0.02,
        "Simulation only — not real survey results",
        transform=ax.transAxes,
        fontsize=8,
    )
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "score_by_video_group.png", dpi=300)
    fig.savefig(FIGURES_DIR / "score_by_video_group.pdf")
    plt.close(fig)

    print("Figures saved as PNG (300 DPI) and PDF in reports/figures/")
    print("Reminder: the figures use simulated data.")


if __name__ == "__main__":
    main()