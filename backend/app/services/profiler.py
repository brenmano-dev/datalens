import pandas as pd
import numpy as np

def profile_dataset(df: pd.DataFrame) -> dict:
    """
    Analyzes a Pandas DataFrame to extract basic dataset properties and infer column types.
    """
    rows, cols = df.shape
    
    columns_profile = []
    for col in df.columns:
        # Base metrics
        missing_count = int(df[col].isnull().sum())
        missing_pct = round((missing_count / rows) * 100, 2) if rows > 0 else 0
        unique_count = int(df[col].nunique())
        
        # Type inference
        col_type = "categorical"  # Default
        
        # Drop NA for accurate type inference on actual values
        valid_data = df[col].dropna()
        
        if pd.api.types.is_numeric_dtype(df[col]):
            # Check if it's actually a boolean masquerading as 0/1
            if set(valid_data.unique()).issubset({0, 1}):
                col_type = "boolean"
            else:
                col_type = "numerical"
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            col_type = "datetime"
        elif pd.api.types.is_bool_dtype(df[col]):
            col_type = "boolean"
        else:
            # Check for strings that represent booleans
            str_lower = valid_data.astype(str).str.lower()
            if set(str_lower.unique()).issubset({'true', 'false', 'yes', 'no'}):
                col_type = "boolean"
            else:
                # Attempt to convert to datetime to catch unparsed date strings
                try:
                    pd.to_datetime(valid_data, format=None, errors='raise')
                    col_type = "datetime"
                except (ValueError, TypeError):
                    pass

        columns_profile.append({
            "name": col,
            "type": col_type,
            "missing_count": missing_count,
            "missing_percentage": missing_pct,
            "unique_count": unique_count
        })

    return {
        "dataset_overview": {
            "rows": rows,
            "columns": cols
        },
        "schema": columns_profile
    }