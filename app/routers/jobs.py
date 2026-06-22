from fastapi import APIRouter, UploadFile, File
from sqlalchemy.orm import Session
from datetime import datetime
import os
from app.database import SessionLocal
from app.models import Job, Transaction,JobSummary
from app.worker.tasks import process_job
router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)
# Upload CSV
@router.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    db: Session = SessionLocal()
    job = Job(
        filename=file.filename,
        status="Pending",
        row_count_raw=0,
        row_count_clean=0,
        created_at=datetime.now()
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    process_job.delay(job.id)
    return {
        "job_id": job.id,
        "status": job.status
    }
# Get all jobs
@router.get("/")
def get_jobs():
    db: Session = SessionLocal()
    jobs = db.query(Job).all()
    return jobs
# Get job status
@router.get("/{job_id}/status")
def get_job_status(job_id: int):
    db: Session = SessionLocal()
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        return {"error": "Job not found"}
    return {
        "job_id": job.id,
        "status": job.status
    }
# Get job results
# Get job results
@router.get("/{job_id}/results")
def get_results(job_id: int):
    db: Session = SessionLocal()
    job = db.query(Job).filter(
        Job.id == job_id
    ).first()
    if not job:
        return {"error": "Job not found"}
    transactions = db.query(Transaction).filter(
        Transaction.job_id == job_id
    ).all()

    anomalies = db.query(Transaction).filter(
        Transaction.job_id == job_id,
        Transaction.is_anomaly.is_(True)
    ).all()
    summary = db.query(JobSummary).filter(
        JobSummary.job_id == job_id
    ).first()

    return {
        "job_id": job.id,
        "status": job.status,

        "total_transactions": len(transactions),
        "anomaly_count": len(anomalies),

        "total_spend_inr":
            summary.total_spend_inr
            if summary else 0,

        "total_spend_usd":
            summary.total_spend_usd
            if summary else 0,

        "risk_level":
            summary.risk_level
            if summary else None,

        "summary":
            summary.narrative
            if summary else None,

        "anomalies": [
            {
                "txn_id": a.txn_id,
                "merchant": a.merchant,
                "amount": a.amount,
                "reason": a.anomaly_reason
            }
            for a in anomalies
        ]
    }