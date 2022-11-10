from typing import List

from pydantic import BaseModel


class Candidate(BaseModel):
    id: int
    name: str
    pictureUrl: str
    party_id: int

    class Config:
        orm_mode = True


class Party(BaseModel):
    id: int
    name: str
    pictureUrl: str
    candidates: List[Candidate]

    class Config:
        orm_mode = True
