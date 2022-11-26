import asyncio
import json
import os
from typing import List

import httpx
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app import model, schema, crud, http_client
from app.database import engine, SessionLocal


def get_application():
    _app = FastAPI(title=os.environ.get('PROJECT_NAME'))

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=json.loads(os.environ.get('BACKEND_CORS_ORIGINS')),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


load_dotenv()
app = get_application()


@app.get("/", tags=["Hello Welcome"])
def hello():
    return "Hello from Somtum"


@app.get("/candidates/{candidate_id}", response_model=schema.Candidate, tags=["Voter"])
def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = crud.get_candidate(db, candidate_id)
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate


@app.get("/candidates", response_model=List[schema.Candidate], tags=["Voter"])
def get_candidates(db: Session = Depends(get_db)):
    candidates = crud.get_candidates(db)
    return candidates


@app.get("/candidates/area/{area_id}", response_model=List[schema.Candidate], tags=["Voter"])
def get_candidates_area(area_id: int, db: Session = Depends(get_db)):
    candidates = crud.get_candidates_by_area(db, area_id)
    return candidates


@app.get("/party", response_model=List[schema.Party], tags=["Voter"])
def get_parties(db: Session = Depends(get_db)):
    parties = crud.get_parties(db)
    return parties


@app.get("/party/{party_id}", response_model=schema.Party, tags=["Voter"])
def get_party(party_id: int, db: Session = Depends(get_db)):
    party = crud.get_party(db, party_id)
    return party


@app.get("/party/member/{party_id}", response_model=List[schema.Candidate], tags=["Voter"])
def get_party_members(party_id: int, db: Session = Depends(get_db)):
    candidates = crud.get_party_members(db, party_id)
    return candidates


@app.get("/vote/party", response_model=schema.PartyVoteResponse, tags=["Voter"])
def vote_party(party_id: int, area_id: int, db: Session = Depends(get_db)):
    ballot = crud.create_ballot_party(db, party_id, area_id)
    vote_result = schema.PartyVoteResponse(voteForParty=ballot)
    return vote_result


@app.get("/vote/mp", response_model=schema.MPVoteResponse, tags=["Voter"])
def vote_mp(candidate_id: int, area_id: int, db: Session = Depends(get_db)):
    ballot = crud.create_ballot_mp(db, candidate_id, area_id)
    vote_result = schema.MPVoteResponse(voteForParty=ballot)
    return vote_result


VOTE_TOPIC_ID = {
    "MP": 1,
    "Party": 2
}

"""
vote_topic_id: Either candidate_id or party_id
"""


@app.get("/vote", tags=["Voter"])
def vote(vote_topic_id: int, area_id: int, vote_target_id: int, db: Session = Depends(get_db)):
    VOTE_TOPIC_ID = {
        1: {
            "method": crud.create_ballot_mp,
            "response_model": schema.MPVoteResponse
        },
        2: {
            "method": crud.create_ballot_party,
            "response_model": schema.PartyVoteResponse
        }
    }

    vote_topic = VOTE_TOPIC_ID.get(vote_topic_id)
    voting = vote_topic.get("method")
    vote_response_model = vote_topic.get("response_model")

    ballot = voting(db, vote_target_id, area_id)
    vote_result = vote_response_model(voteForParty=ballot)
    return vote_result


@app.get("/validation", tags=["Voter"])
def get_ballots(vote_topic_id: int, area_id: int, db: Session = Depends(get_db)):
    ballots = crud.get_ballots_by_area(db, vote_topic_id, area_id)
    return ballots


@app.get("/score/mp", tags=["EC"])
def get_candidate_scores(db: Session = Depends(get_db)):
    ballots = crud.get_ballots(db, VOTE_TOPIC_ID.get("MP"))

    sorted_id_ballots = sorted(ballots, key=lambda b: b.candidate_id)

    candidates_score = dict()
    for b in sorted_id_ballots:
        if b.candidate_id not in candidates_score:
            candidates_score[b.candidate_id] = 1
        else:
            candidates_score[b.candidate_id] += 1

    return candidates_score


@app.get("/score/party", tags=["EC"])
def get_candidate_scores(db: Session = Depends(get_db)):
    ballots = crud.get_ballots(db, VOTE_TOPIC_ID.get("Party"))

    sorted_id_ballots = sorted(ballots, key=lambda b: b.party_id)

    party_scores = dict()
    for b in sorted_id_ballots:
        if b.party_id not in party_scores:
            party_scores[b.party_id] = 1
        else:
            party_scores[b.party_id] += 1

    return party_scores


@app.get("/score/area/candidate", tags=["EC"])
def get_candidate_scores_area(area_id: int, db: Session = Depends(get_db)):
    ballots = crud.get_ballots_by_area(db, VOTE_TOPIC_ID.get("MP"), area_id)

    sorted_id_ballots = sorted(ballots, key=lambda b: b.candidate_id)

    candidates_scores = dict()
    for b in sorted_id_ballots:
        if b.candidate_id not in candidates_scores:
            candidates_scores[b.candidate_id] = 1
        else:
            candidates_scores[b.candidate_id] += 1

    return candidates_scores


@app.get("/score/area/party", tags=["EC"])
def get_party_scores_area(area_id: int, db: Session = Depends(get_db)):
    ballots = crud.get_ballots_by_area(db, VOTE_TOPIC_ID.get("Party"), area_id)

    sorted_id_ballots = sorted(ballots, key=lambda b: b.party_id)

    party_scores = dict()
    for b in sorted_id_ballots:
        if b.party_id not in party_scores:
            party_scores[b.party_id] = 1
        else:
            party_scores[b.party_id] += 1

    return party_scores


@app.get("/score/party/areas", tags=["EC"])
def get_party_score_areas(db: Session = Depends(get_db)):
    try:
        population_statistics = asyncio.run(http_client.get_population_statistics())
        area_scores = []

        for location in population_statistics:
            ballots = crud.get_ballots_by_area(db, VOTE_TOPIC_ID.get("Party"), location.get("LocationID"))

            sorted_id_ballots = sorted(ballots, key=lambda b: b.party_id)

            party_scores = dict()
            scores = dict()
            for b in sorted_id_ballots:
                if b.party_id not in scores:
                    scores[b.party_id] = 1
                else:
                    scores[b.party_id] += 1

            party_scores["score"] = scores

            try:
                party_scores["most_voted"] = max(scores, key=scores.get)
            except ValueError:
                party_scores["most_voted"] = 0

            party_scores["area_id"] = location.get("LocationID")
            party_scores["area_name"] = location.get("Location")

            area_scores.append(party_scores)

        return area_scores

    except httpx.HTTPError:
        return []


@app.get("/score/candidate/areas", tags=["EC"])
def get_party_score_areas(db: Session = Depends(get_db)):
    try:
        population_statistics = asyncio.run(http_client.get_population_statistics())
        area_scores = []

        for location in population_statistics:
            ballots = crud.get_ballots_by_area(db, VOTE_TOPIC_ID.get("MP"), location.get("LocationID"))

            sorted_id_ballots = sorted(ballots, key=lambda b: b.candidate_id)

            candidate_scores = dict()
            scores = dict()
            for b in sorted_id_ballots:
                if b.candidate_id not in scores:
                    scores[b.candidate_id] = 1
                else:
                    scores[b.candidate_id] += 1

            candidate_scores["score"] = scores

            try:
                candidate_scores["most_voted"] = max(scores, key=scores.get)
            except ValueError:
                candidate_scores["most_voted"] = 0

            candidate_scores["area_id"] = location.get("LocationID")
            candidate_scores["area_name"] = location.get("Location")

            area_scores.append(candidate_scores)

        return area_scores

    except httpx.HTTPError:
        return []


@app.get("/gov/candidates", response_model=List[schema.GovCandidate], tags=["EC"])
def get_candidate_and_save_to_db(db: Session = Depends(get_db)):
    try:
        candidates = asyncio.run(http_client.get_candidate_from_gov())

        for c in candidates:
            citizen_id = c.get("CitizenID")
            name = " ".join([c.get("Name"), c.get("Lastname")])
            area_id = c.get("DistrictID")
            crud.create_candidate(db, citizen_id, name, area_id)

        return candidates
    except httpx.HTTPError:
        return []


@app.get("/population", response_model=List[schema.PopulationStatistic], tags=["EC"])
def get_population_statistics():
    try:
        population_statistics = asyncio.run(http_client.get_population_statistics())

        return population_statistics
    except httpx.HTTPError:
        return []


@app.post("/submit", tags=["EC"])
def submit_mp(db: Session = Depends(get_db)):
    try:
        population_statistics = asyncio.run(http_client.get_population_statistics())
        area_scores = []

        for location in population_statistics:
            ballots = crud.get_ballots_by_area(db, VOTE_TOPIC_ID.get("MP"), location.get("LocationID"))

            sorted_id_ballots = sorted(ballots, key=lambda b: b.candidate_id)

            candidate_scores = dict()
            scores = dict()
            for b in sorted_id_ballots:
                if b.candidate_id not in scores:
                    scores[b.candidate_id] = 1
                else:
                    scores[b.candidate_id] += 1

            candidate_scores["score"] = scores

            try:
                won_candidate_id = max(scores, key=scores.get)
                candidate_scores["won_candidate_id"] = crud.get_candidate(db, won_candidate_id).citizen_id
            except ValueError:
                candidate_scores["won_candidate_id"] = 0

            area_scores.append(candidate_scores)

            result = []
            for a in area_scores:
                to_submit_id = a.get("won_candidate_id")

                if len(to_submit_id) == 13:
                    result.append(asyncio.run(http_client.submit_mp(to_submit_id)))

        return result

    except httpx.HTTPError:
        return []


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
