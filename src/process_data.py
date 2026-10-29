import os
import json
import pandas as pd
import numpy as np

def process_raw_logs(raw_file_path="data/raw/benchmark_run.jsonl"):
   
    if not os.path.exists(raw_file_path):
        raise FileNotFoundError(f"Файл {raw_file_path} не найден! Запустите сперва python src/benchmark.py")

    # 1. Загрузка и парсинг сырых логов JSONL
    records = []
    with open(raw_file_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line.strip()))
    
    df_raw = pd.DataFrame(records)
    total_raw_count = len(df_raw)
    print(f"[+] Успешно загружено записей из raw log: {total_raw_count}")

    # 2. Подсчет Guardrail Metric (Процент ошибок/сбоев для предотвращения Selection Bias)
    if "status_code" in df_raw.columns:
        error_mask = df_raw["status_code"] != 200
    else:
        error_mask = df_raw["pass_score"].isna() | (df_raw["daily_hours"] < 0)

    error_count = int(error_mask.sum())
    error_rate = (error_count / total_raw_count) * 100 if total_raw_count > 0 else 0.0
    print(f"[+] Guardrail Metric — Error Rate: {error_rate:.2f}% ({error_count}/{total_raw_count})")

    # 3. Фильтрация прогрева (Warm-up Filtering)
    df_benchmark = df_raw[df_raw["phase"] == "benchmark"].copy()
    warmup_count = total_raw_count - len(df_benchmark)
    print(f"[+] Отфильтровано записей фазы 'warmup': {warmup_count} | Осталось рабочих: {len(df_benchmark)}")

    # 4. Детекция выбросов методом Interquartile Range (1.5x IQR)
    q1 = df_benchmark["pass_score"].quantile(0.25)
    q3 = df_benchmark["pass_score"].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    # Неразрушающая пометка выбросов флагом (без удаления реальных спайков нагрузки)
    df_benchmark["is_outlier"] = (df_benchmark["pass_score"] < lower_bound) | (df_benchmark["pass_score"] > upper_bound)
    outliers_found = int(df_benchmark["is_outlier"].sum())
    print(f"[+] Выявлено аппаратных выбросов (IQR bounds [{lower_bound:.2f}, {upper_bound:.2f}]): {outliers_found}")

    return df_benchmark

if __name__ == "__main__":
    df_clean = process_raw_logs()
    print("\n--- Пример обработанных данных (первые 5 строк) ---")
    print(df_clean.head())
