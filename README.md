# DataPilot AI

> Your AI-Powered Data Analyst — upload any dataset and get instant cleaning, analysis, insights, and a downloadable report.

![DataPilot AI](https://img.shields.io/badge/DataPilot-AI-38bdf8?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

---

## What It Does

DataPilot AI is a full-stack AI-powered analytics platform. Upload a CSV or Excel file and the app automatically:

- **Profiles** your dataset — rows, columns, types, memory usage
- **Detects and fixes** data quality issues — missing values, duplicates, outliers
- **Generates interactive EDA charts** — histograms, boxplots, correlation heatmap, scatter plots
- **Narrates AI insights** — powered by Gemini, with statistical fallback
- **Exports a professional PDF report** — summary, charts, insights, recommendations

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Vite, Tailwind CSS v4 |
| Backend | FastAPI, Python 3.11 |
| Data | Pandas, NumPy, SciPy |
| Visualization | Plotly, Matplotlib |
| AI | Google Gemini 1.5 Flash |
| PDF | ReportLab |
| Deployment | Vercel (frontend), Render (backend) |

---

## Project Structure

```
DataPilot-AI/
│
├── backend/
│   ├── app/
│   │   ├── main.py               # FastAPI app entry point
│   │   ├── api/
│   │   │   └── routes.py         # All API endpoints
│   │   └── services/
│   │       ├── data_service.py       # Dataset profiling
│   │       ├── cleaning_service.py   # Data quality engine
│   │       ├── eda_service.py        # EDA chart generation
│   │       ├── insights_service.py   # AI insights (Gemini)
│   │       └── report_service.py     # PDF report generation
│   ├── uploads/                  # Uploaded datasets
│   ├── reports/                  # Generated PDF reports
│   ├── requirements.txt
│   └── .env                      # API keys (not committed)
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── UploadZone.jsx
│   │   │   ├── DataSummary.jsx
│   │   │   ├── DataCleaning.jsx
│   │   │   ├── EDACharts.jsx
│   │   │   └── AIInsights.jsx
│   │   ├── pages/
│   │   │   └── Home.jsx
│   │   └── services/
│   │       └── api.js
│   ├── index.html
│   └── vite.config.js
│
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- A [Gemini API key](https://aistudio.google.com/apikey)

### 1. Clone the repository

```bash
git clone https://github.com/swikarb69/datapilot-ai.git
cd datapilot-ai
```

### 2. Backend setup

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file in the `backend/` directory:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

Start the backend:

```bash
uvicorn app.main:app --reload
```

Backend runs at `http://localhost:8000`

### 3. Frontend setup

```bash
cd frontend
yarn install
yarn dev
```

Frontend runs at `http://localhost:5173`

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/upload` | Upload CSV or Excel file |
| GET | `/api/summary/{filename}` | Get dataset summary |
| GET | `/api/analyze/{filename}` | Detect data quality issues |
| POST | `/api/clean/{filename}` | Apply cleaning operations |
| GET | `/api/eda/{filename}` | Generate EDA charts |
| GET | `/api/insights/{filename}` | Generate AI insights |
| POST | `/api/report/{filename}` | Generate PDF report |
| GET | `/api/download/{filename}` | Download cleaned dataset |

---

## Features

### Upload & Profile
Upload any CSV or Excel file. The app instantly profiles your data — row/column counts, data types, missing values, memory usage, and a 10-row preview.

### Data Quality Check
Automatically detects missing values per column with smart imputation suggestions (mean, median, mode, drop, constant). Also detects duplicates and outliers using IQR analysis.

### Interactive EDA
Generates 6+ interactive Plotly charts — distribution histograms, boxplots, correlation heatmap, categorical bar charts, and scatter plots — all in a filterable dark-themed dashboard.

### AI Insights
Gemini analyzes your dataset profile and generates an executive summary, 6 typed insights (positive/warning/neutral), and 3 actionable recommendations. Falls back to statistical analysis when API quota is unavailable.

### PDF Report
One-click export of a professional multi-page PDF including dataset overview, column details, statistical summary, matplotlib charts, AI insights, and recommendations.

---

## Sample Dataset

A sample dataset with intentional quality issues is included for testing:

```
name, age, salary, city, department
Alice, 29, 55000, New York, Engineering
Bob, , 62000, San Francisco, Marketing
...
```

---

## Resume Bullet

> **Built DataPilot AI**, an end-to-end AI-powered analytics platform enabling users to upload CSV/Excel datasets and automatically perform data cleaning, exploratory data analysis, natural language insight generation, and downloadable PDF report export — built with FastAPI, React, Gemini AI, Pandas, Plotly, and ReportLab.

---

## License

MIT License — free to use, modify, and distribute.

---

*Built by [Swikar Bhattarai](https://github.com/swikarb69)*