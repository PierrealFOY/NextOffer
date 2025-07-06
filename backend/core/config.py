import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Database
    DATABASE_URL: str = os.environ.get("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable is not set")

    # Auth
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable is not set")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    RESET_TOKEN_EXPIRE_MINUTES: int = 15

    SERP_API_KEY: str = os.environ.get("SERP_API_KEY")
    if not SERP_API_KEY:
        print("Warning: SERP_API_KEY is not set.")

    FRANCETRAVAIL_CLIENT_ID: str = os.environ.get("FRANCETRAVAIL_CLIENT_ID")
    FRANCETRAVAIL_CLIENT_SECRET: str = os.environ.get("FRANCETRAVAIL_CLIENT_SECRET")
    JOBBOARD_URL: str = "https://remotive.com/api/remote-jobs"
    JOBBOARD_URL_SERP: str = "https://serpapi.com/search"
    FRANCETRAVAIL_API_URL: str = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"
    FRANCETRAVAIL_TOKEN_URL: str = "https://francetravail.io/connexion/oauth2/access_token?realm=%2Fpartenaire"
    MAILGUN_DOMAIN_NAME: str = "sandboxd286ea5bd41d473f9dada7406be22d59.mailgun.org"
    MAILGUN_API_URL: str = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN_NAME}/messages"
    MAILGUN_API_KEY: str = os.environ.get("MAILGUN_API_KEY")

    CORS_ORIGINS: list = [
        "http://localhost",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    #Frontend
    FRONTEND_URL = "http://localhost:5173"

settings = Settings()
