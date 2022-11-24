from typing import List

from pydantic import BaseModel


class GovCandidate(BaseModel):
    CitizenID: int
    LazerID: str
    Name: str
    Lastname: str
    Birthday: str
    Nationality: str
    DistrictID: str


class PopulationStatistic(BaseModel):
    LocationID: int
    Location: str
    PeopleWithRightToVote: int
    PeopleCommitTheVote: int
    TotalPeople: int


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

    class Config:
        orm_mode = True


class Ballot(BaseModel):
    id: int
    area_id: int

    class Config:
        orm_mode = True


class MPBallot(Ballot):
    candidate_id: int


class PartyBallot(Ballot):
    party_id: int


class MPVoteResponse(BaseModel):
    voteForParty: MPBallot


class PartyVoteResponse(BaseModel):
    voteForParty: PartyBallot
