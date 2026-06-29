from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from app.services.data_service import load_dataset, get_summary
from app.services.cleaning_service import analyze_issues, apply_cleaning
from app.services.eda_service import generate_eda
from app.services.insights_service import generate_insights

from app.services.report_service import generate_report
from app.services.insights_service import generate_insights
from fastapi.responses import FileResponse
import uuid

import shutil
import os

router = APIRouter()
UPLOAD_DIR = "uploads"


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith((".csv", ".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Only CSV and Excel files are supported.")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    summary = load_dataset(file_path)
    return {"filename": file.filename, "summary": summary}


@router.get("/summary/{filename}")
async def get_dataset_summary(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found.")
    return get_summary(file_path)


@router.get("/analyze/{filename}")
async def analyze_dataset(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found.")
    return analyze_issues(file_path)


@router.post("/clean/{filename}")
async def clean_dataset(filename: str, instructions: dict):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found.")
    return apply_cleaning(file_path, instructions)


@router.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found.")
    return FileResponse(file_path, media_type="text/csv", filename=filename)

@router.get("/eda/{filename}")
async def get_eda(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found.")
    return generate_eda(file_path)

@router.get("/insights/{filename}")
async def get_insights(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found.")
    return generate_insights(file_path)

@router.post("/report/{filename}")
async def create_report(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found.")
    
    insights = generate_insights(file_path)
    report_path = generate_report(file_path, insights)
    
    return FileResponse(
        report_path,
        media_type="application/pdf",
        filename=os.path.basename(report_path)
    )