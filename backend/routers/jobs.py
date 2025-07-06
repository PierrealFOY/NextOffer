from datetime import date, datetime
from xml.dom import ValidationErr
from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Dict, Any
from auth.schemas import FavoriteJobRequest, JobBase, UserResponse
from utils.colorText import colorText
from services.job_aggregator import JobAggregator
from models.models import Job, LikedJob, User
from pydantic import BaseModel, ConfigDict, field_validator
from sqlalchemy.orm import Session
from database import get_db
import asyncio
from starlette.status import HTTP_404_NOT_FOUND


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)

class JobResponse(JobBase):
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

###### ROUTES ######
@router.get("/", response_model=List[JobResponse])
async def get_jobs(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    jobs_data_from_aggregator = await JobAggregator.aggregate_jobs(offset=offset, limit=limit, db=db)
    
    response_jobs = []
    for job_obj in jobs_data_from_aggregator:
        try:
            response_jobs.append(JobResponse.model_validate(job_obj))
        except ValidationErr as e:
            print(colorText(f"Validation Error for job: {job_obj} - {e}", 'rouge'))
            continue
    return response_jobs

@router.get("/{id}", response_model=JobResponse)
async def get_job_by_id(id: str, db: Session = Depends(get_db)):
    jobs_data_from_aggregator = await JobAggregator.aggregate_jobs(offset=0, limit=1000, db=db)
    
    for job_obj in jobs_data_from_aggregator:  # job_obj est un objet Job
            
        if str(job_obj.id) == str(id):
            print(colorText(f'job {id} successfully found', 'vert_fonce'))
            try:
                return JobResponse.model_validate(job_obj)
            except ValidationErr as e:
                print(colorText(f"Validation Error for job {id}: {job_obj} - {e}", 'rouge'))
                raise HTTPException(status_code=500, detail=f"Failed to serialize job {id}")
    print(colorText(f'no job exists with id {id}', 'rouge'))
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Job not found")

# @router.post("/favorite-job", response_model=UserResponse)
# async def toggle_favorite_job(payload: FavoriteJobRequest, db: Session = Depends(get_db)):
#     from routers.auth import get_user_by_id
#     job_id = payload.job_id
#     user_id = payload.user_id

#     # 1. Check if the job already exists in the database
#     job_in_db = db.query(Job).filter(Job.id == job_id).first()
#     if not job_in_db:
#         # 2. if not in the database, get it from the API
#         jobs_data_from_aggregator = await JobAggregator.aggregate_jobs(offset=0, limit=1000, db=db)
#         job_data: Dict[str, Any] | None = None
#         for job_obj in jobs_data_from_aggregator:
#           if str(job_obj.id) == str(job_id):
#               job_data = JobResponse.model_validate(job_obj).model_dump()
#               break

#         if not job_data:
#             print(colorText(f'no job exists with id {job_id}', 'rouge'))
#             raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Job not found")

#         job_data_for_db = job_data.copy() # Create a mutable copy

#         if 'company' not in job_data_for_db:
#             job_data_for_db['company'] = ""

#         if isinstance(job_data.get('dateCreation'), str):
#             try:
#                 job_data['dateCreation'] = datetime.strptime(job_data['dateCreation'], "%d/%m/%Y").date()
#             except ValueError:
#                 try:
#                     job_data['dateCreation'] = datetime.fromisoformat(job_data['dateCreation'].replace('Z', '+00:00')).date()
#                 except ValueError:
#                     job_data['dateCreation'] = date.today()

#         job_in_db = Job(**job_data_for_db)
#         db.add(job_in_db)
#         db.commit()
#         db.refresh(job_in_db)

#     # 4. check if the job is already in favorites
#     favorite_job = db.query(FavoriteJob).filter(
#         FavoriteJob.user_id == user_id,
#         FavoriteJob.job_id == job_id
#     ).first()

#     # If the job is already in favorites: remove it
#     if favorite_job:
#         job_in_db.liked = False
#         db.delete(favorite_job)
#         db.commit()
#         print(colorText(f'Job {job_id} removed from favorites', 'jaune'))
#         return get_user_by_id(user_id, db)

#     # 5. Add the job to favorites
#     new_favorite = FavoriteJob(user_id=user_id, job_id=job_id)
#     job_in_db.liked = True
#     db.add(new_favorite)
#     db.commit()
#     db.refresh(new_favorite)

#     print(colorText(f'Job {job_id} successfully added to favorites', 'vert_fonce'))
#     return get_user_by_id(user_id, db)

# @router.get("/favorite-jobs/{user_id}", response_model=List[JobResponse])
# async def get_favorite_jobs(user_id: int, db: Session = Depends(get_db)):
#     jobs_to_return: List[JobResponse] = []

#     favorite_jobs_entries = db.query(FavoriteJob).filter(FavoriteJob.user_id == user_id).all()
#     for favorite_entry in favorite_jobs_entries:
#         db_job_instance = db.query(Job).filter(Job.id == favorite_entry.job_id).first()
#         if db_job_instance:
#             try:
#                 jobs_to_return.append(JobResponse.model_validate(db_job_instance))
#             except ValidationErr as e:
#                 print(colorText(f"Validation Error for favorite job {db_job_instance.id}: {e}", 'rouge'))
#                 continue

#     if not jobs_to_return and favorite_jobs_entries:
#             print(colorText(f'No favorite job(s) found for this user or linked jobs missing.', 'orange'))
#     print(f"User to return: {jobs_to_return}")

#     for job in jobs_to_return:
#         print(f"{type(job)=}")

#     return [JobResponse.model_validate(job) for job in jobs_to_return]

@router.post("/liked-jobs", response_model=UserResponse)
async def like_job(payload: FavoriteJobRequest, db: Session = Depends(get_db)):
    # import inside the fonction to avoir circular import / dependancy error
    # on top of file importing
    from routers.auth import get_user_by_id

    # check before if the job is already liked by the user
    job_in_db = db.query(LikedJob).filter_by(
        user_id=payload.user_id,
        job_id=payload.job_id
        ).first()
    # if not, get the job from the API
    if not job_in_db:
        # check if the job exists in the table Job
        existing_job = db.query(Job).filter_by(id=payload.job_id).first()

        if not existing_job:
            jobs_data_from_aggregator = await JobAggregator.aggregate_jobs(offset=0, limit=1000, db=db)
            job_data: Dict[str, Any] | None = None
            for job_obj in jobs_data_from_aggregator:
                if str(job_obj.id) == str(payload.job_id):
                    job_data = JobResponse.model_validate(job_obj).model_dump()
                    break

            if not job_data:
                print(colorText(f'no job exists with id {payload.job_id}', 'rouge'))
                raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Job not found")
        
            job_data_for_db = job_data.copy()
            job_in_db = Job(**job_data_for_db)
            db.add(job_in_db)
            db.commit()
            db.refresh(job_in_db)
        else:
            job_in_db = existing_job

        # 4. check if the job is already liked
        liked_job = db.query(LikedJob).filter(
            LikedJob.user_id == payload.user_id,
            LikedJob.job_id == payload.job_id
        ).first()
        if liked_job:
            raise HTTPException(status_code=409, detail=f"{liked_job}Job already liked")

    # 5. Add the job to favorites
    new_liked = LikedJob(user_id=payload.user_id, job_id=payload.job_id)
    job_in_db.liked = True
    db.add(new_liked)
    db.commit()
    db.refresh(new_liked)
    return get_user_by_id(payload.user_id, db)


@router.delete("/liked-jobs/{job_id}", response_model=UserResponse)
async def unlike_job(job_id: str, user_id: int = Query(...), db: Session = Depends(get_db)):
    from routers.auth import get_user_by_id
    
    liked = db.query(LikedJob).filter_by(user_id=user_id, job_id=job_id).first()
    if not liked:
        raise HTTPException(status_code=404, detail="Like not found")

    db.delete(liked)
    db.commit()
    return get_user_by_id(user_id, db)

@router.get("/liked-jobs/{user_id}", response_model=List[JobResponse])
async def get_liked_jobs(user_id: int, db: Session = Depends(get_db)):
    liked_jobs = (
        # joins LikedJob table with Job table based on job_id
        # filters results to only include jobs liked by the user
        db.query(Job).join(LikedJob, LikedJob.job_id == Job.id)
        .filter(LikedJob.user_id == user_id)
        .all()
    )
    return liked_jobs
