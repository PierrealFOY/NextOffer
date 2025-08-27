from datetime import datetime
import requests
from typing import List
from utils.colorText import colorText
from models.models import Job
from core.config import settings
from auth.schemas import JobBase, JobResponse

class RemotiveService:
    @staticmethod
    def fetch_jobs() -> List[JobBase]:
        jobs: List[JobBase] = []
        try:
            response = requests.get(settings.JOBBOARD_URL)
            response.raise_for_status()
            data = response.json()
            jobs = [
                JobBase(
                    external_id=str(job['id']),
                    title=job.get("title", ""),
                    company=job.get("company_name", ""),
                    url=job.get("url", ""),
                    source="Remotive",
                    location=job.get("candidate_required_location", ""),
                    salary=job.get("salary", ""),
                    description=job.get("description", ""),
                    typeContrat=job.get("job_type", ""),
                    dateCreation=datetime.strptime(job.get("publication_date", ""), "%Y-%m-%dT%H:%M:%S.%fZ").date(),
                )
                for job in data.get("jobs", [])[:settings.JOB_LIMIT]
            ]
            print(colorText(f"Remotive: {len(jobs)} jobs fetched.", 'vert_fonce'))
        except requests.exceptions.RequestException as e:
            print(colorText(f"Error fetching from Remotive: {e}", 'rouge'))
        except ValueError as e:
            print(colorText(f"Date parsing error from Remotive: {e}", 'rouge'))
        return jobs
