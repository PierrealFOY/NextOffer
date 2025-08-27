from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, field_validator, ConfigDict

class JobBase(BaseModel):
    # on creation, id is None because not yet created
    id: Optional[int] = None
    external_id: Optional[str] = None
    title: str
    company: str
    url: str
    source: str
    location: str
    salary: str
    description: str
    typeContrat: str
    dateCreation: datetime
    liked: Optional[bool] = False

    model_config = ConfigDict(from_attributes=True)

    @field_validator("dateCreation", mode="before")
    @classmethod
    def parse_date(cls, v):
        if isinstance(v, str):
            try:
                # Correct format for Remotive dates
                return datetime.fromisoformat(v.replace('Z', '+00:00'))
            except ValueError:
                try:
                    # Correct format for France Travail dates
                    return datetime.strptime(v, "%d/%m/%Y")
                except ValueError:
                    # Return a default datetime if parsing fails
                    return datetime.now()
        # If input is already a date or datetime, return it as datetime
        if isinstance(v, date):
            return datetime(v.year, v.month, v.day)
        return v

class JobResponse(JobBase):
    id: int
    @field_validator("dateCreation", mode="after")
    @classmethod
    def format_date(cls, v: datetime):
        return v.strftime("%d/%m/%Y") if isinstance(v, date) else v

class LikedJobSchema(BaseModel):
    job: JobResponse

    model_config = ConfigDict(from_attributes=True)

class SeenJobSchema(BaseModel):
    job: JobResponse

    model_config = ConfigDict(from_attributes=True)

class AppliedJobSchema(BaseModel):
    job: JobResponse

    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserSchema(BaseModel):
    id: int
    username: str
    email: str
    disabled: bool = False
    reset_password_token: Optional[str] = None
    reset_password_expires_at: Optional[datetime] = None
    # favorite_jobs: List[JobResponse] = [] # keep JObResponse or serialize bug
    liked_jobs: List[LikedJobSchema] # keep JObResponse or serialize bug
    seen_jobs: List[SeenJobSchema]
    applied_jobs: List[AppliedJobSchema]

    model_config = ConfigDict(from_attributes=True)

class FavoriteJobRequest(BaseModel):
    job_id: int
    # user_id: int

    model_config = ConfigDict(from_attributes=True)

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    disabled: bool = False
    reset_password_token: Optional[str] = None
    reset_password_expires_at: Optional[datetime] = None
    liked_jobs: List[LikedJobSchema] = []
    seen_jobs: List[SeenJobSchema] = []
    applied_jobs: List[SeenJobSchema] = []

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str = None

class ForgotPasswordRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
