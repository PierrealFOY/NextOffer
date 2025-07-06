from typing import Optional
from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, Date, Table, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import date, datetime

class Job(Base):
    __tablename__ = 'jobs'

    id = Column(String, primary_key=True)
    title = Column(String)
    company = Column(String)
    url = Column(String)
    source = Column(String)
    location = Column(String)
    salary = Column(String)
    description = Column(Text)
    typeContrat = Column(String)
    dateCreation = Column(Date)
    users = relationship("User", secondary="liked_jobs")
    liked = Column(Boolean, default=False)

    def __init__(self,
                    id: str,
                    title: str,
                    company: str,
                    url: str,
                    source: str,
                    location: str,
                    salary: str,
                    description: str,
                    typeContrat: str,
                    dateCreation: date,
                    liked: Optional[bool] = False,
                ):
        self.id = id
        self.title = title
        self.company = company
        self.url = url
        self.source = source
        self.location = location
        self.salary = salary
        self.description = description
        self.typeContrat = typeContrat
        self.dateCreation = dateCreation
        self.liked = liked

    def to_dict(self):
        if isinstance(self.dateCreation, str):
            try:
                date_obj = datetime.strptime(self.dateCreation, "%Y-%m-%d").date()
            except ValueError:
                date_obj = None
        else:
            date_obj = self.dateCreation

        return {
            "id": str(self.id) if self.id else "",
            "title": str(self.title) if self.title else "",
            "company": str(self.company) if self.company else "",
            "url": str(self.url) if self.url else "",
            "source": str(self.source) if self.source else "",
            "location": str(self.location) if self.location else "",
            "salary": str(self.salary) if self.salary else "",
            "description": str(self.description) if self.description else "",
            "typeContrat": str(self.typeContrat) if self.typeContrat else "",
            "dateCreation": date_obj.strftime("%d/%m/%Y") if date_obj else "",
            "liked": self.liked,
        }


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)
    reset_password_token = Column(String, nullable=True)
    reset_password_expires_at = Column(DateTime, nullable=True)
    # favorite_jobs = relationship("Job", secondary="favorite_jobs")
    liked_jobs = relationship("LikedJob", back_populates="user")
    # jobs = relationship("Job", secondary="liked_jobs")

# class FavoriteJob(Base):
#     __tablename__ = "favorite_jobs"
    
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     job_id = Column(String, ForeignKey("jobs.id"))

class LikedJob(Base):
    __tablename__ = "liked_jobs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    job_id = Column(String, ForeignKey("jobs.id"))

    user = relationship("User", back_populates="liked_jobs")
    job = relationship("Job", lazy="joined")
