from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DataBaseURL = "postgresql://postgres:Sathwik1804@localhost:5432/transactions"
engine = create_engine(DataBaseURL)
SessionLocal = sessionmaker(
  autocommit = False,
  autoflush = False,
  bind = engine
)
Base = declarative_base()