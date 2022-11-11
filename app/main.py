import os
from typing import List

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app import model, schema, crud
from app.database import engine, SessionLocal


def get_application():
    _app = FastAPI(title=os.environ.get('PROJECT_NAME'))

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[os.environ.get('BACKEND_CORS_ORIGINS')],
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
model.Base.metadata.create_all(bind=engine)
app = get_application()


@app.get("/candidates/{id}", response_model=schema.Candidate)
def get_user(candidate_id: int, db: Session = Depends(get_db)):
    candidate = crud.get_candidate(db, candidate_id)
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate


@app.get("/candidates/", response_model=List[schema.Candidate])
def get_users(db: Session = Depends(get_db)):
    candidates = crud.get_candidates(db)
    return candidates


@app.get("/party/", response_model=List[schema.Party])
def get_parties(db: Session = Depends(get_db)):
    parties = crud.get_party(db)
    return parties


@app.get("/party/member", response_model=List[schema.Candidate])
def get_party_members(party_id: int, db: Session = Depends(get_db)):
    candidates = crud.get_party_members(db, party_id)
    return candidates


@app.get("/vote/", response_model=schema.VoteResponse)
def vote(party_id: int, candidate_id: int, db: Session = Depends(get_db)):
    ballot = crud.create_ballot(db, party_id, candidate_id)
    vote_result = schema.VoteResponse(voteForParty=ballot)
    return vote_result


@app.get("/validation")
def get_ballots(area_id: int, db: Session = Depends(get_db)):
    ballots = crud.get_ballots_by_area(db, area_id)
    return ballots


@app.get("/score/")
async def get_candidate_scores(db: Session = Depends(get_db)):
    ballots = crud.get_ballots(db)

    sorted_id_ballots = sorted(ballots, key=lambda b: b.candidate_id)

    candidates_score = dict()
    for b in sorted_id_ballots:
        if b.candidate_id not in candidates_score:
            candidates_score[b.candidate_id] = 1
        else:
            candidates_score[b.candidate_id] += 1

    return candidates_score

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
