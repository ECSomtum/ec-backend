import asyncio
import httpx
import os
from dotenv import load_dotenv


load_dotenv()

ROUTES = {
    "CandidateInfo": "candidate/",
    "SubmitMP": "mp/submit/",
    "PopulationStatistics": "population/statistic/"
}


def get_authorization_headers():
    return {'Authorization': f"Bearer {os.environ.get('API_KEY')}"}


def get_url_path(endpoint: str):
    return os.environ.get('GOV_ENDPOINT') + ROUTES.get(endpoint)


async def get_candidate_from_gov():
    async with httpx.AsyncClient() as client:
        response = await client.get(get_url_path("CandidateInfo"), headers=get_authorization_headers())

    response.raise_for_status()

    return response.json()


async def get_population_statistics():
    async with httpx.AsyncClient() as client:
        response = await client.get(get_url_path('PopulationStatistics'), headers=get_authorization_headers())

    response.raise_for_status()

    return response.json()


async def submit_mp(candidate_id: int):
    mp = {
        "CitizenID": candidate_id
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(get_url_path('SubmitMP'), headers=get_authorization_headers(), json=mp)

    response.raise_for_status()

    return response.json()
