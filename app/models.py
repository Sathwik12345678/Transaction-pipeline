from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from app.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    status = Column(String)
    row_count_raw = Column(Integer)
    row_count_clean = Column(Integer)
    created_at = Column(DateTime)
    completed_at = Column(DateTime)
    error_message = Column(Text)


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))

    txn_id = Column(String)
    date = Column(String)
    merchant = Column(String)

    amount = Column(Float)
    currency = Column(String)
    status = Column(String)

    category = Column(String)
    account_id = Column(String)

    is_anomaly = Column(Boolean, default=False)
    anomaly_reason = Column(Text)

    llm_category = Column(String)
    llm_raw_response = Column(Text)
    llm_failed = Column(Boolean, default=False)


class JobSummary(Base):
    __tablename__ = "job_summaries"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))

    total_spend_inr = Column(Float)
    total_spend_usd = Column(Float)

    top_merchants = Column(Text)
    anomaly_count = Column(Integer)

    narrative = Column(Text)
    risk_level = Column(String)