from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
import shutil

from app.services.data_service import load_dataset, get_summary
from app.services.cleaning_service import analyze_issues, apply_cleaning
from app.services.eda_service import generate_eda
from app.services.insights_service import generate_insights
from app.services.report_service import generate_report

router = APIRouter()

# ----------------------------------------------------
# Base project directory
# ----------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent.parent

UPLOAD_DIR = BASE_DIR / "uploads"
REPORT_DIR = BASE_DIR / "reports"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)


# ----------------------------------------------------
# Upload Dataset
# ----------------------------------------------------
@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".csv", ".xlsx", ".xls")):
        raise HTTPException(
            status_code=400,
            detail="Only CSV and Excel files are supported."
        )

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    summary = load_dataset(str(file_path))

    return {
        "filename": file.filename,
        "summary": summary
    }


# ----------------------------------------------------
# Dataset Summary
# ----------------------------------------------------
@router.get("/summary/{filename}")
async def get_dataset_summary(filename: str):
    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found.")

    return get_summary(str(file_path))


# ----------------------------------------------------
# Analyze Dataset
# ----------------------------------------------------
@router.get("/analyze/{filename}")
async def analyze_dataset(filename: str):
    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found.")

    return analyze_issues(str(file_path))


# ----------------------------------------------------
# Clean Dataset
# ----------------------------------------------------
@router.post("/clean/{filename}")
async def clean_dataset(filename: str, instructions: dict):
    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found.")

    return apply_cleaning(str(file_path), instructions)


# ----------------------------------------------------
# Download File
# ----------------------------------------------------
@router.get("/download/{filename}")
async def download_file(filename: str):
    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found.")

    return FileResponse(
        path=str(file_path),
        media_type="text/csv",
        filename=file_path.name,
    )


# ----------------------------------------------------
# EDA
# ----------------------------------------------------
@router.get("/eda/{filename}")
async def get_eda(filename: str):
    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found.")

    return generate_eda(str(file_path))


# ----------------------------------------------------
# AI Insights
# ----------------------------------------------------
@router.get("/insights/{filename}")
async def get_insights(filename: str):
    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found.")

    return generate_insights(str(file_path))


# ----------------------------------------------------
# Generate PDF Report
# ----------------------------------------------------
@router.post("/report/{filename}")
async def create_report(filename: str):
    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found.")

    insights = generate_insights(str(file_path))
    report_path = generate_report(str(file_path), insights)

    return FileResponse(
        path=str(report_path),
        media_type="application/pdf",
        filename=Path(report_path).name,
    )