# Domain Model: Short-Video Use and Academic Procrastination

## Scope

This model describes the data-analysis workflow for the approved survey-topic adaptation of Task 3. The current records are simulated for demonstrating the workflow; they are not real student responses.

## Container view

```mermaid
flowchart LR
    R["Researcher"] --> G["Synthetic survey-data generator<br/>Python script"]
    G --> RAW[("Simulated raw records<br/>JSONL and CSV")]
    RAW --> P["Data processing and statistics<br/>src/process_data.py"]
    P --> CLEAN[("Cleaned records and<br/>metrics_summary.csv")]
    CLEAN --> V["Visualization module<br/>src/visualize.py"]
    V --> FIG[("Figures<br/>reports/figures/")]
    CLEAN --> N["Jupyter analysis notebook"]
    FIG --> N
    N --> REP["Task 3 report and README"]