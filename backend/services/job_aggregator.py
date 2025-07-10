import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List

from requests import Session
from auth.schemas import JobResponse
from services.external_apis.remotive import RemotiveService
# from services.external_apis.serpapi import SerpAPIService
from services.external_apis.francetravail import FranceTravailService
from core.config import settings

class JobAggregator:
    @staticmethod
    async def aggregate_jobs(offset: int = 0, limit: int = settings.JOB_LIMIT, db: Session = None) -> List[JobResponse]:
        loop = asyncio.get_running_loop()
        remotive_future = loop.run_in_executor(None, RemotiveService.fetch_jobs)
        # serpapi_future = loop.run_in_executor(None, SerpAPIService.fetch_jobs)

        france_travail_jobs = await FranceTravailService.fetch_jobs()

        remotive_jobs = await asyncio.gather(remotive_future)

        all_jobs = remotive_jobs[0] + france_travail_jobs

        # remove duplicates based on URL
        unique_jobs = []
        seen_urls = set()
        for job in all_jobs:
            if job.url and job.url not in seen_urls: # Ensure URL exists for de-duplication
                seen_urls.add(job.url)
                unique_jobs.append(job)
            elif not job.url: # If job has no URL, append it anyway, or handle as desired
                unique_jobs.append(job)

        paginated_jobs = unique_jobs[offset : offset + limit]

        return paginated_jobs