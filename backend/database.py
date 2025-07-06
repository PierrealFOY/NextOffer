from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()

#to manage database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# to create table (to be called on starting)
def create_db_tables():
    Base.metadata.create_all(bind=engine)

# to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
