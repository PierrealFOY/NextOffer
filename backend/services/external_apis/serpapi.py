# import requests
# from typing import List
# from models.models import Job
# from core.config import settings

# class SerpAPIService:
#     @staticmethod
#     def fetch_jobs() -> List[Job]:
#         try:
#             if not settings.SERP_API_KEY:
#                 print("SERP_API_KEY not set, skipping SerpAPI job fetch.")
#                 return []

#             params = {
#                 "engine": "google_jobs",
#                 "q": "remote developer",
#                 "api_key": settings.SERP_API_KEY,
#                 "location": ""
#             }
#             response = requests.get(settings.JOBBOARD_URL_SERP, params=params)
#             response.raise_for_status()
#             data = response.json()
#             return [
#                 Job(
#                     id=job.get("job_id", ""),
#                     title=job.get("title", ""),
#                     company=job.get("company_name", ""),
#                     url=job.get("related_links", [{}])[0].get("link", "") or job.get("url", ""), # Fallback for URL
#                     source="SerpAPI",
#                     location=job.get("location", ""),
#                 )
#                 for job in data.get("jobs_results", [])[:10] # Limiting for example
#             ]
#         except requests.exceptions.RequestException as e:
#             print(f"Error fetching from SerpAPI: {e}")
#         return []