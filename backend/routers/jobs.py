from datetime import date, datetime
from auth.authentication import get_current_user
from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Dict, Any
from auth.schemas import FavoriteJobRequest, JobBase, UserResponse
from utils.colorText import colorText
from services.job_aggregator import JobAggregator
from models.models import Job, LikedJob, SeenJob, AppliedJob, User
from pydantic import BaseModel, ConfigDict, field_validator, ValidationError
from sqlalchemy.orm import Session
from database import get_db
import asyncio
from starlette.status import HTTP_404_NOT_FOUND
from core.config import settings


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)

class JobResponse(JobBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

    @field_validator("dateCreation", mode="before")
    @classmethod
    def ensure_date(cls, v):
        if isinstance(v, datetime):
            return v.strftime("%d/%m/%Y")
        elif isinstance(v, date):
            return v.strftime("%d/%m/%Y")
        elif isinstance(v, str):
            try:
                # Attempt to parse ISO format first
                dt_object = datetime.fromisoformat(v.replace('Z', '+00:00'))
                return dt_object.strftime("%d/%m/%Y")
            except ValueError:
                return v
        return str(v)
    

###################
###### ROUTES ######

@router.get("/", response_model=List[JobResponse])
async def get_jobs(
    offset: int = Query(0, ge=0),
    limit: int = Query(settings.JOB_LIMIT, ge=1, le=100),
    db: Session = Depends(get_db)
):
    jobs_from_db = JobAggregator.get_jobs_from_db(offset=offset, limit=limit, db=db)
    print(colorText(f"{len(jobs_from_db)} jobs found.", 'vert_fonce'))
    return [JobResponse.model_validate(job) for job in jobs_from_db]

@router.post("/import")
async def import_jobs(db: Session = Depends(get_db)):
    await JobAggregator.aggregate_jobs(db)
    return {"message": "Job import initiated successfully."}


@router.get("/{id}", response_model=JobResponse)
async def get_job_by_id(id: int, db: Session = Depends(get_db)):
    job_in_db = db.query(Job).filter(Job.id == id).first()

    if not job_in_db:
        print(colorText(f'no job exists with id {id}', 'rouge'))
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Job not found")

    print(colorText(f'job {id} successfully found', 'vert_fonce'))
    return JobResponse.model_validate(job_in_db)


@router.post("/liked-jobs", response_model=UserResponse)
async def like_job(
    payload: FavoriteJobRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    from routers.auth import get_user_by_id

    # 1. Check if job is already liked by the user
    already_liked = db.query(LikedJob).filter_by(
        user_id=current_user.id,
        job_id=payload.job_id
    ).first()

    if already_liked:
        raise HTTPException(status_code=409, detail="Job already liked")
    # 2. Try to find the job in DB
    job_in_db = db.query(Job).filter_by(id=payload.job_id).first()
    # 3. If not found, fetch from aggregator
    if not job_in_db:
        print(colorText(f"No job exists with id {payload.job_id}", 'rouge'))
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Job not found")

    # 4. Like the job
    liked_job = LikedJob(user_id=current_user.id, job_id=payload.job_id)
    db.add(liked_job)
    db.commit()

    return get_user_by_id(current_user.id, db)


@router.delete("/liked-jobs/{job_id}", response_model=UserResponse)
async def unlike_job(job_id: int, user_id: int = Query(...), db: Session = Depends(get_db)):
    from routers.auth import get_user_by_id
    
    liked = db.query(LikedJob).filter_by(user_id=user_id, job_id=job_id).first()
    if not liked:
        raise HTTPException(status_code=404, detail="Like not found")

    db.delete(liked)
    db.commit()
    return get_user_by_id(user_id, db)

@router.get("/liked-jobs/{user_id}", response_model=List[JobResponse])
async def get_liked_jobs(user_id: int, db: Session = Depends(get_db)):
    liked_jobs = db.query(LikedJob).filter_by(user_id=user_id).all()
    jobs: List[JobResponse] = []
    
    for liked in liked_jobs:
        job = db.query(Job).filter_by(id=liked.job_id).first()
        if job:
            try:
                jobs.append(JobResponse.model_validate(job))
            except ValidationError as e:
                print(colorText(f"Validation Error for liked job {job.id}: {e}", 'rouge'))
    return jobs

## SEEN JOBS ##
@router.post("/{user_id}/seen-jobs", response_model = UserResponse)
async def see_job(
    payload: FavoriteJobRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    from routers.auth import get_user_by_id

    # 1. check if job is already seen
    already_seen = db.query(SeenJob).filter_by(
        user_id=current_user.id,
        job_id=payload.job_id,
    ).first()

    if already_seen:
        raise HTTPException(status_code=409, detail="Job already seen")
    # 2. try to find job in DB
    job_in_db = db.query(Job).filter_by(id=payload.job_id).first()

    # 3. if not in DB, fetch from aggregator
    if not job_in_db:
        print(colorText(f"No job exists with id {payload.job_id}", 'rouge'))
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Job not found")

    # 4. "See" the job
    seen_job = SeenJob(user_id=current_user.id, job_id=payload.job_id)
    db.add(seen_job)
    db.commit()

    return get_user_by_id(current_user.id, db)

@router.get("/seen-jobs/{user_id}", response_model=List[JobResponse])
async def get_seen_jobs(user_id: int, db: Session = Depends(get_db)):
    seen_jobs = db.query(SeenJob).filter_by(user_id=user_id).all()
    jobs: List[JobResponse] = []

    for seen in seen_jobs:
        job = db.query(Job).filter_by(id=seen.job_id).first()
        if job:
            try:
                jobs.append(JobResponse.model_validate(job))
            except ValidationError as e:
                print(colorText(f"Validation Error for seen job {job.id}: {e}", 'rouge'))
    return jobs

## APPLIED JOBS ##
@router.post("/{user_id}/apply-jobs", response_model = UserResponse)
async def apply_job(
    payload: FavoriteJobRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    from routers.auth import get_user_by_id

    # 1. check if job is already applied
    already_applied = db.query(SeenJob).filter_by(
        user_id=current_user.id,
        job_id=payload.job_id,
    ).first()

    if already_applied:
        raise HTTPException(status_code=409, detail="Job already applied")

    # 2. try to find job in DB
    job_in_db = db.query(Job).filter_by(id=payload.job_id).first()

    # 3. if not in DB, fetch from aggregator
    if not job_in_db:
        print(colorText(f"No job exists with id {payload.job_id}", 'rouge'))
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Job not found")

    # 4. "Apply" the job
    applied_job = SeenJob(user_id=current_user.id, job_id=payload.job_id)
    db.add(applied_job)
    db.commit()

    return get_user_by_id(current_user.id, db)


@router.get("/applied-jobs/{user_id}", response_model=List[JobResponse])
async def get_applied_jobs(user_id: int, db: Session = Depends(get_db)):
    applied_jobs = db.query(SeenJob).filter_by(user_id=user_id).all()
    jobs: List[JobResponse] = []

    for applied in applied_jobs:
        job = db.query(Job).filter_by(id=applied.job_id).first()
        if job:
            try:
                jobs.append(JobResponse.model_validate(job))
            except ValidationError as e:
                print(colorText(f"Validation Error for applied job {job.id}: {e}", 'rouge'))
    return jobs
