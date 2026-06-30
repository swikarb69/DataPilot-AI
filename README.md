<div align="center">

# DataPilot AI

### Your AI-Powered Data Analyst

Upload any dataset and get instant cleaning, analysis, AI-narrated insights, and a downloadable PDF report — no code required.

[![Live Demo](https://img.shields.io/badge/LIVE_DEMO-data--pilot--ai--silk.vercel.app-22C55E?style=for-the-badge&logo=vercel&logoColor=white)](https://data-pilot-ai-silk.vercel.app)
[![API Docs](https://img.shields.io/badge/API_DOCS-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://datapilot-ai-backend-umul.onrender.com/docs)

![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini_AI-8E75B2?style=for-the-badge&logo=google&logoColor=white)

</div>

---

## Overview

DataPilot AI turns a raw CSV or Excel file into a full analyst-grade report in minutes. Upload a dataset and the platform automatically:

- **Profiles** it — rows, columns, types, memory usage, missing data
- **Cleans** it — detects missing values, duplicates, and outliers, then applies the imputation strategy you choose
- **Visualizes** it — 6+ interactive Plotly charts: distributions, boxplots, correlation heatmap, categorical breakdowns, scatter plots
- **Explains** it — Gemini-powered narrative insights with an automatic statistical fallback if the AI is unavailable
- **Reports** it — a single click exports a fully designed, chart-embedded PDF report

This isn't a notebook demo. It's a deployed, end-to-end product — a React frontend talking to a FastAPI backend, both live in production.

---

## Live Demo

| | |
|---|---|
| 🌐 **App** | [data-pilot-ai-silk.vercel.app](https://data-pilot-ai-silk.vercel.app) |
| 🔌 **API Docs** | [datapilot-ai-backend-umul.onrender.com/docs](https://datapilot-ai-backend-umul.onrender.com/docs) |

> Note: the backend is hosted on Render's free tier, which spins down after inactivity. The first request after idle time may take 30–60 seconds to wake up.

---

## How It Works

```
Upload CSV/Excel
        │
        ▼
Dataset Profiling  →  rows, columns, types, missing %, preview
        │
        ▼
Data Quality Check  →  missing values, duplicates, outliers detected
        │
        ▼
Cleaning Engine  →  mean / median / mode / drop / constant imputation
        │
        ▼
Automated EDA  →  6+ interactive Plotly charts + statistical summary
        │
        ▼
AI Insights  →  Gemini-narrated summary, typed insights, recommendations
        │
        ▼
PDF Report  →  one-click, fully designed, chart-embedded export
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Vite, Tailwind CSS v4, Lucide Icons |
| Backend | FastAPI, Python 3.11 |
| Data Processing | Pandas, NumPy, SciPy |
| Visualization | Plotly (interactive), Matplotlib (PDF export) |
| AI | Google Gemini 1.5 Flash, with statistical fallback engine |
| PDF Generation | ReportLab |
| Deployment | Vercel (frontend) · Render (backend) |

---

## Project Structure

```
DataPilot-AI/
│
├── backend/
│   ├── app/
│   │   ├── main.py                   # FastAPI app entry point
│   │   ├── api/
│   │   │   └── routes.py             # All API endpoints
│   │   └── services/
│   │       ├── data_service.py       # Dataset profiling
│   │       ├── cleaning_service.py   # Data quality engine
│   │       ├── eda_service.py        # Interactive EDA chart generation
│   │       ├── insights_service.py   # AI insights (Gemini + fallback)
│   │       └── report_service.py     # PDF report generation
│   ├── uploads/                      # Uploaded datasets (gitignored)
│   ├── reports/                      # Generated PDF reports (gitignored)
│   ├── requirements.txt
│   └── .env                          # API keys (gitignored)
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

## Getting Started Locally

### Prerequisites

- Python 3.10+
- Node.js 18+
- A free [Gemini API key](https://aistudio.google.com/apikey)

### 1. Clone the repository

```bash
git clone https://github.com/swikarb69/DataPilot-AI.git
cd DataPilot-AI
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

Create a `.env` file inside `backend/`:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

Start the backend:

```bash
uvicorn app.main:app --reload
```

→ Backend runs at `http://localhost:8000` · Swagger docs at `http://localhost:8000/docs`

### 3. Frontend setup

```bash
cd frontend
yarn install
yarn dev
```

→ Frontend runs at `http://localhost:5173`

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/upload` | Upload a CSV or Excel file |
| `GET` | `/api/summary/{filename}` | Get dataset summary & preview |
| `GET` | `/api/analyze/{filename}` | Detect data quality issues |
| `POST` | `/api/clean/{filename}` | Apply cleaning operations |
| `GET` | `/api/eda/{filename}` | Generate interactive EDA charts |
| `GET` | `/api/insights/{filename}` | Generate AI insights |
| `POST` | `/api/report/{filename}` | Generate downloadable PDF report |
| `GET` | `/api/download/{filename}` | Download the cleaned dataset |

Full interactive docs available at [`/docs`](https://datapilot-ai-backend-umul.onrender.com/docs) (Swagger UI, auto-generated by FastAPI).

---

## Feature Breakdown

### 📁 Upload & Profile
Drag-and-drop CSV or Excel upload. Instant profiling — row/column counts, data types, missing-value percentages, memory footprint, and a live preview table.

### 🧹 Data Quality Check
Per-column missing value detection with strategy selection (mean, median, mode, drop, constant). Duplicate row detection. Outlier detection via IQR. One click applies every fix and returns a cleaned, downloadable dataset.

### 📊 Interactive EDA
6+ Plotly charts generated automatically per dataset — distribution histograms, boxplots, a correlation heatmap, categorical value-count bars, and scatter plots — filterable by chart type, all rendered in a dark, dashboard-style UI.

### 🤖 AI Insights
Gemini 1.5 Flash analyzes the dataset's statistical profile and produces an executive summary, six typed insights (positive / warning / neutral), and three actionable recommendations. If the API quota is exhausted, a pure-Python statistical engine generates equivalent insights from real correlation and distribution analysis — the feature never breaks.

### 📄 PDF Report
One click exports a multi-page, professionally designed PDF: dataset overview, column details, statistical summary, matplotlib-rendered charts, AI insights, and recommendations — ready to attach to an email or share with a client.

---

## Resume Bullet

> **Built and deployed DataPilot AI**, a full-stack AI-powered analytics platform enabling users to upload CSV/Excel datasets and automatically perform data cleaning, exploratory data analysis, Gemini-powered insight generation, and downloadable PDF report export. Built with FastAPI, React, Pandas, Plotly, and ReportLab; deployed on Vercel and Render.

---

## License

MIT License — free to use, modify, and distribute.

---

<div align="center">

*Built by [Swikar Bhattarai](https://github.com/swikarb69)*

</div>