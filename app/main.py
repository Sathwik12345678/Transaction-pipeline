from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routers.jobs import router as jobs_router
Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="AI Transaction Processing Pipeline"
)
app.include_router(jobs_router)
@app.get("/")
def root():
    return {
        "message": "API Running Successfully"
    }