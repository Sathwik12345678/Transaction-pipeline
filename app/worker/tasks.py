from app.worker.celery_app import celery
from app.database import SessionLocal
from app.models import Job, Transaction
import pandas as pd


@celery.task
def process_job(job_id):
    db = SessionLocal()
    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return "Job not found"
        # Update status
        job.status = "Processing"
        db.commit()
        # Read CSV
        file_path = f"uploads/{job.filename}"
        print("Reading:", file_path)
        df = pd.read_csv(file_path)
        # Raw row count
        job.row_count_raw = len(df)
        # --------------------------
        # DATA CLEANING
        # --------------------------
        # Normalize dates
        df["date"] = pd.to_datetime(
            df["date"],
            errors="coerce",
            dayfirst=True
        ).dt.strftime("%Y-%m-%d")
        # Remove duplicates
        df = df.drop_duplicates()
        # Remove $
        df["amount"] = (
            df["amount"]
            .astype(str)
            .str.replace("$", "", regex=False)
        )
        # Convert amount to numeric
        df["amount"] = pd.to_numeric(
            df["amount"],
            errors="coerce"
        )
        # Uppercase status
        df["status"] = (
            df["status"]
            .astype(str)
            .str.upper()
        )
        # Uppercase currency
        df["currency"] = (
            df["currency"]
            .astype(str)
            .str.upper()
        )
        # Fill missing category
        df["category"] = df["category"].fillna("Uncategorised")
        # --------------------------
        # ANOMALY DETECTION
        # --------------------------
        df["is_anomaly"] = False
        df["anomaly_reason"] = ""
        # Rule 1: Amount > 3x account median
        for account in df["account_id"].unique():
            account_df = df[df["account_id"] == account]
            median_amount = account_df["amount"].median()
            threshold = median_amount * 3
            mask = (
                (df["account_id"] == account)
                &
                (df["amount"] > threshold)
            )
            df.loc[mask, "is_anomaly"] = True
            df.loc[
                mask,
                "anomaly_reason"
            ] = "Amount exceeds 3x account median"
        # Rule 2: USD transaction with domestic merchants
        domestic_merchants = [
            "Swiggy",
            "Ola",
            "IRCTC"
        ]
        mask = (
            df["currency"].eq("USD")
            &
            df["merchant"].isin(domestic_merchants)
        )
        df.loc[mask, "is_anomaly"] = True
        df.loc[
            mask,
            "anomaly_reason"
        ] = "USD transaction with domestic merchants"
        anomaly_count = int(df["is_anomaly"].sum())
        # Clean row count
        job.row_count_clean = len(df)
        db.commit()
        print("Raw Rows:", job.row_count_raw)
        print("Clean Rows:", job.row_count_clean)
        print("Anomalies Found:", anomaly_count)
        # --------------------------
        # STORE TRANSACTIONS
        # --------------------------
        for _, row in df.iterrows():
            transaction = Transaction(
                job_id=job.id,
                txn_id=str(row["txn_id"]),
                date=str(row["date"]),
                merchant=str(row["merchant"]),
                amount=float(row["amount"])
                if pd.notna(row["amount"])
                else 0,
                currency=str(row["currency"]),
                status=str(row["status"]),
                category=str(row["category"]),
                account_id=str(row["account_id"]),
                is_anomaly=bool(row["is_anomaly"]),
                anomaly_reason=str(row["anomaly_reason"])
            )
            db.add(transaction)
        db.commit()
        print("Transactions Saved:", len(df))
        # Complete Job
        job.status = "Completed"
        db.commit()
        return "Done"
    except Exception as e:
        print("ERROR:", str(e))
        if job:
            job.status = "Failed"
            job.error_message = str(e)
            db.commit()
        return str(e)
    finally:
        db.close()