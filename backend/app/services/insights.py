def generate_insights(quality: dict, stats: dict, correlations: dict, rows: int) -> list:
    insights = []
    
    if quality.get("duplicates", 0) > 0:
        insights.append(f"Found {quality['duplicates']} duplicate row(s) in the dataset.")
        
    for col, count in quality.get("missing_values", {}).items():
        pct = round((count / rows) * 100, 1) if rows > 0 else 0
        if pct > 0:
            insights.append(f"'{col}' has {pct}% missing values and may require data cleaning.")
            
    for col, count in quality.get("outliers", {}).items():
        insights.append(f"'{col}' contains {count} observations classified as statistical outliers (IQR method).")
        
    for col, stat in stats.items():
        if "most_frequent" in stat and stat.get("percentage", 0) > 50:
            insights.append(f"'{stat['most_frequent']}' represents {stat['percentage']}% of all records in the '{col}' column.")
            
    for pair, val in correlations.items():
        direction = "positive" if val > 0 else "negative"
        insights.append(f"{pair} have a strong {direction} correlation ({val}).")
        
    return insights[:8]
