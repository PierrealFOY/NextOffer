import requests
import time
from datetime import datetime
from typing import List
from models.models import Job
from core.config import settings
from auth.schemas import JobBase, JobResponse
from utils.colorText import colorText

_francetravail_token_cache = {
    "access_token": None,
    "expires_at": 0
}

async def get_francetravail_access_token():
    current_time = time.time()

    if _francetravail_token_cache["access_token"] and _francetravail_token_cache["expires_at"] > current_time + 60:
        return _francetravail_token_cache["access_token"]

    if not settings.FRANCETRAVAIL_CLIENT_ID or not settings.FRANCETRAVAIL_CLIENT_SECRET:
        print("Erreur: FRANCETRAVAIL_CLIENT_ID ou FRANCETRAVAIL_CLIENT_SECRET non définis dans .env")
        return None

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = (
        f"client_id={settings.FRANCETRAVAIL_CLIENT_ID}&"
        f"client_secret={settings.FRANCETRAVAIL_CLIENT_SECRET}&"
        "grant_type=client_credentials&"
        "scope=o2dsoffre api_offresdemploiv2"
    )

    try:
        response = requests.post(settings.FRANCETRAVAIL_TOKEN_URL, headers=headers, data=payload)
        response.raise_for_status()
        token_data = response.json()

        access_token = token_data.get("access_token")
        expires_in = token_data.get("expires_in", 3600)

        if access_token:
            _francetravail_token_cache["access_token"] = access_token
            _francetravail_token_cache["expires_at"] = current_time + expires_in
            print(f"Token France Travail obtenu/rafraîchi. Expiration dans {expires_in} secondes.")
            return access_token
        else:
            print(f"Erreur: 'access_token' non trouvé dans la réponse du token France Travail: {token_data}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'obtention du token France Travail: {e}")
        if e.response is not None:
            print(f"Réponse d'erreur: {e.response.status_code} - {e.response.text}")
        return None

class FranceTravailService:
    @staticmethod
    async def fetch_jobs() -> List[JobBase]:
        access_token = await get_francetravail_access_token()
        if not access_token:
            print("Impossible d'obtenir le token France Travail, étape suivante.")
            return []

        try:
            params = {
                "accesTravailleurHandicape": "false",
                "motsCles":"" if settings.ENV == "prod" else "développeur",
            }
            print(settings.ENV)
            print(colorText(f"France Travail env actuel (pour motsClés): {settings.ENV}.", "bleu"))
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json"
            }
            url = settings.FRANCETRAVAIL_API_URL
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()

            data = response.json()
            jobs: List[JobBase] = []

            for offre in data.get("resultats", []):
                date_creation_str = offre.get("dateCreation")
                date_creation = datetime.strptime(date_creation_str, "%Y-%m-%dT%H:%M:%S.%fZ").date() if date_creation_str else None
                job = JobBase(
                    external_id=str(offre.get("id", "")),
                    title=offre.get("intitule", ""),
                    company=offre.get("entreprise", {}).get("nom", ""),
                    url=offre.get("contact", {}).get("urlPostulation", "") or "",
                    source="France Travail",
                    location=offre.get("lieuTravail", {}).get("libelle", ""),
                    salary=offre.get("salaire", {}).get("libelle", ""),
                    description=offre.get("description", {}),
                    typeContrat=offre.get("typeContrat", {}),
                    dateCreation=date_creation,
                )
                jobs.append(job)
            print(colorText(f"France Travail: {len(jobs)} jobs fetched.", "bleu"))
        except requests.exceptions.RequestException as e:
            print(f"Error fetching from France Travail: {e}")
            if e.response is not None:
                print(f"Response error: {e.response.status_code} - {e.response.text}")
            return []
        except Exception as e:
            print(f"Unexpected error fetching from France Travail: {e}")
            return []
        return jobs