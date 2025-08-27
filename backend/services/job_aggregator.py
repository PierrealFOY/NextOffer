import asyncio
from concurrent.futures import ThreadPoolExecutor
from sqlite3 import IntegrityError
from typing import List

from utils.colorText import colorText
from sqlalchemy.orm import Session

from auth.schemas import JobBase, JobResponse
from database import get_db
from models.models import Job
from services.external_apis.remotive import RemotiveService
from services.external_apis.francetravail import FranceTravailService
from core.config import settings

class JobAggregator:
    @staticmethod
    async def aggregate_jobs(db: Session) -> None:
        """
        Agrège les offres d'emploi des différentes sources et les enregistre dans la base de données.
        """
        loop = asyncio.get_running_loop()
        remotive_future = loop.run_in_executor(None, RemotiveService.fetch_jobs)

        # retrieve jobs in parallel from Remotive and FranceTravail
        remotive_jobs, france_travail_jobs = await asyncio.gather(remotive_future, FranceTravailService.fetch_jobs())

        all_jobs: List[JobBase] = remotive_jobs + france_travail_jobs
        print(colorText(f"{len(all_jobs)} jobs found.", 'vert_fonce'))

        jobs_to_add = []
        for job_base in all_jobs:
            # Check if url already exists in DB
            existing_job = db.query(Job).filter(Job.url == job_base.url).first()
            if not existing_job:
                # Create new instance of Job from JobBase
                new_job = Job(
                    external_id=job_base.external_id,
                    title=job_base.title,
                    company=job_base.company,
                    url=job_base.url,
                    source=job_base.source,
                    location=job_base.location,
                    salary=job_base.salary,
                    description=job_base.description,
                    typeContrat=job_base.typeContrat,
                    dateCreation=job_base.dateCreation,
                    liked=False
                )
                jobs_to_add.append(new_job)
                
        if jobs_to_add:
            try:
                db.bulk_save_objects(jobs_to_add)
                db.commit()
                print(colorText(f"{len(jobs_to_add)} new jobs saved to DB.", 'vert_fonce'))
            except IntegrityError as e:
                db.rollback()
                print(colorText(f"Error saving jobs to DB: {e}", 'rouge'))

    @staticmethod
    def get_jobs_from_db(offset: int, limit: int, db: Session) -> List[Job]:
        """
        Récupère les offres d'emploi directement depuis la base de données.
        """
        print(colorText(f"Retrieving {limit} jobs from DB.", 'vert_fonce'))
        return db.query(Job).offset(offset).limit(limit).all()