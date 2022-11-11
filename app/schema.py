from typing import List

from pydantic import BaseModel


class Candidate(BaseModel):
    id: int
    name: str
    pictureUrl: str
    area_id: int
    party_id: int

    class Config:
        orm_mode = True


class Party(BaseModel):
    id: int
    name: str
    pictureUrl: str
    # accept_candidate: int

    class Config:
        orm_mode = True


class Ballot(BaseModel):
    id: int
    area_id: int
    party_id: int
    candidate_id: int

    class Config:
        orm_mode = True


class VoteResponse(BaseModel):
    voteForParty: Ballot
