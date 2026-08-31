from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
import warnings

# Suppress pandas dateutil warnings for clean console output
warnings.filterwarnings("ignore", category=UserWarning)

from backend.app.services.profiler import profile_dataset
from backend.app.services.quality import calculate_quality
from backend.app.services.statistics import calculate_statistics, calculate_correlations
from backend.app.services.insights import generate_insights

app = FastAPI(title="DataLens API")

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For MVP. Restrict in production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/api/analyze")
async def analyze_dataset(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    
    try:
        contents = await file.read()
        # Read CSV into Pandas directly from memory
        df = pd.read_csv(io.BytesIO(contents))
        
        # 1. Profile Dataset
        profile = profile_dataset(df)
        
        # 2. Quality Analysis
        quality = calculate_quality(df, profile["schema"])
        
        # 3. Statistics & Correlations
        stats = calculate_statistics(df, profile["schema"])
        corrs = calculate_correlations(df, profile["schema"])
        
        # 4. Automated Insights
        insights = generate_insights(quality, stats, corrs, profile["dataset_overview"]["rows"])
        
        # Optional: Grab the first 10 rows for frontend preview
        # Replace NaNs with None so JSON serialization works
        preview = df.head(10).replace({pd.NA: None, float('nan'): None}).to_dict(orient="records")
        
        return {
            "dataset": profile["dataset_overview"],
            "schema": profile["schema"],
            "quality": quality,
            "statistics": stats,
            "correlations": corrs,
            "insights": insights,
            "preview": preview
        }
    except Exception as e:
        # In a real app, log this properly. For MVP, return bad request.
        raise HTTPException(status_code=400, detail=f"Failed to parse CSV: {str(e)}")
