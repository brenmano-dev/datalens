import pandas as pd
import numpy as np

def calculate_quality(df: pd.DataFrame, schema: list) -> dict:
    """
    Analyzes data quality: duplicates, missing values, outliers, and computes a score.
    """
    rows = len(df)
    if rows == 0:
        return {"score": 0, "duplicates": 0, "missing_values": {}, "outliers": {}}

    # 1. Duplicates
    duplicates = int(df.duplicated().sum())

    # 2. Missing Values
    missing_values = {}
    total_missing = 0
    total_cells = rows * len(df.columns)
    
    for col in df.columns:
        missing_count = int(df[col].isnull().sum())
        if missing_count > 0:
            missing_values[col] = missing_count
            total_missing += missing_count

    # 3. Outliers (IQR method for numerical columns)
    outliers = {}
    total_outliers = 0
    
    numerical_cols = [col["name"] for col in schema if col["type"] == "numerical"]
    for col in numerical_cols:
        series = df[col].dropna()
        if len(series) < 4:  # Too few data points for meaningful IQR
            continue
            
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outlier_count = int(((series < lower_bound) | (series > upper_bound)).sum())
        if outlier_count > 0:
            outliers[col] = outlier_count
            total_outliers += outlier_count

    # 4. Data Quality Score (0-100)
    score = 100
    
    # Transparent Deductions:
    # - 1 point for every 1% of duplicate rows (max 20 point deduction)
    dup_penalty = min(20, (duplicates / rows) * 100)
    
    # - 1 point for every 1% of missing cells (max 40 point deduction)
    missing_penalty = min(40, (total_missing / total_cells) * 100)
    
    # - 0.5 points for every 1% of cells that are outliers (max 20 point deduction)
    outlier_penalty = min(20, (total_outliers / total_cells) * 100 * 0.5)

    score = max(0, int(score - dup_penalty - missing_penalty - outlier_penalty))

    return {
        "score": score,
        "duplicates": duplicates,
        "missing_values": missing_values,
        "outliers": outliers
    }
