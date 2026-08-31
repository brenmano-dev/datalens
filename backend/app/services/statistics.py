import pandas as pd
import numpy as np

def calculate_statistics(df: pd.DataFrame, schema: list) -> dict:
    stats = {}
    for col in schema:
        name = col["name"]
        c_type = col["type"]
        series = df[name].dropna()
        if series.empty:
            continue
        
        if c_type == "numerical":
            stats[name] = {
                "count": int(series.count()),
                "mean": round(float(series.mean()), 2),
                "median": round(float(series.median()), 2),
                "std_dev": round(float(series.std()), 2) if len(series) > 1 else 0,
                "min": round(float(series.min()), 2),
                "max": round(float(series.max()), 2),
                "q1": round(float(series.quantile(0.25)), 2),
                "q3": round(float(series.quantile(0.75)), 2)
            }
        elif c_type in ["categorical", "boolean"]:
            value_counts = series.value_counts()
            top_value = value_counts.index[0] if len(value_counts) > 0 else None
            top_freq = int(value_counts.iloc[0]) if len(value_counts) > 0 else 0
            stats[name] = {
                "unique_values": int(series.nunique()),
                "most_frequent": str(top_value) if top_value is not None else None,
                "frequency": top_freq,
                "percentage": round((top_freq / len(series)) * 100, 2) if len(series) > 0 else 0
            }
    return stats

def calculate_correlations(df: pd.DataFrame, schema: list) -> dict:
    num_cols = [col["name"] for col in schema if col["type"] == "numerical"]
    if len(num_cols) < 2:
        return {}
    
    corr_matrix = df[num_cols].corr().round(2)
    correlations = {}
    
    for i in range(len(num_cols)):
        for j in range(i + 1, len(num_cols)):
            col1, col2 = num_cols[i], num_cols[j]
            val = corr_matrix.iloc[i, j]
            if not np.isnan(val) and abs(val) >= 0.5:  # Only flag strong relationships
                correlations[f"{col1} ↔ {col2}"] = float(val)
                
    return dict(sorted(correlations.items(), key=lambda item: abs(item[1]), reverse=True))
