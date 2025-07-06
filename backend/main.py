from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import Settings, settings

from database import create_db_tables
from models import models as orm_models

from routers import auth as auth_router
from routers import jobs as jobs_router
from utils.colorText import colorText

settings = Settings()

app = FastAPI(
    title="Job Scraper API",
    description="A FastAPI backend for aggregating job listings from various sources.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    print("Creating database tables...")
    create_db_tables() # create tables for all tables
    print("Database tables created (if they didn't exist).")
    print(colorText("---------------------------------------------------", "vert_fonce"))
    print(colorText("     Welcome to the Job Scraper API! 🌞", "vert_fonce"))
    print(colorText("---------------------------------------------------", "vert_fonce"))
app.include_router(auth_router.router)
app.include_router(jobs_router.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Job Scraper API! Visit /docs for API documentation."}