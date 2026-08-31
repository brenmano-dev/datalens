# DataLens 📊
**Automated Dataset Intelligence Platform**

DataLens is a full-stack web application designed to eliminate the manual overhead of initial data exploration. By uploading a raw CSV, users immediately receive a comprehensive, automated data-quality and statistical analysis report.

## 🚀 Business Impact & Core Features
* **Automated Data Profiling:** Engineered a Pandas-based backend engine to instantly detect schema types, missing values, and calculate a deterministic 0-100 Data Quality Score.
* **Statistical Discovery:** Automated the extraction of central tendencies, dispersions, and strong numerical correlations using NumPy and SciPy principles.
* **Interactive Visualizations:** Architected a responsive React dashboard featuring Recharts integrations for immediate visual distribution analysis.
* **Modern UI/UX:** Designed a fluid, interactive frontend utilizing Tailwind CSS v4 and glassmorphism design principles for a premium SaaS experience.

## 🛠️ Technology Stack
* **Backend:** Python 3.14, FastAPI, Pandas, NumPy, Uvicorn
* **Frontend:** React, TypeScript, Vite, Tailwind CSS v4, Recharts, Lucide React
* **Architecture:** Decoupled RESTful API with multipart file handling and in-memory dataframe processing.

## ⚙️ Quick Start
```bash
# Terminal 1: Backend
cd datalens
source venv/bin/activate
PYTHONPATH=. uvicorn backend.app.main:app --reload --port 8000

# Terminal 2: Frontend
cd datalens/frontend
npm run dev
