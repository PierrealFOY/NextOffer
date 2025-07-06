import requests
from typing import List
from models.models import Job
from core.config import settings
from auth.schemas import JobResponse

class RemotiveService:
    @staticmethod
    def fetch_jobs() -> List[JobResponse]:
        try:
            response = requests.get(settings.JOBBOARD_URL)
            response.raise_for_status()
            data = response.json()
            jobs = [
                Job(
                    id=str(idx),
                    title=job.get("title", ""),
                    company=job.get("company_name", ""),
                    url=job.get("url", ""),
                    source="Remotive",
                    location=job.get("candidate_required_location", ""),
                    salary=job.get("salary", ""),
                    description=job.get("description", ""),
                    typeContrat=job.get("job_type", ""),
                    dateCreation=job.get("publication_date", ""),
                )
                for idx, job in enumerate(data.get("jobs", [])[:20])
            ]
            return [JobResponse.from_orm(job) for job in jobs]
        except requests.exceptions.RequestException as e:
            print(f"Error fetching from Remotive: {e}")
        return []
