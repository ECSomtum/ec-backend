from sqlalchemy.orm import Session

from . import model, schema

VOTE_TOPIC_ID = {
    1: model.MPBallot,
    2: model.PartyBallot
}


def get_candidate(db: Session, candidate_id: int):
    return db.query(model.Candidate).filter(model.Candidate.id == candidate_id).first()


def get_candidates(db: Session):
    return db.query(model.Candidate).all()


def get_candidates_by_area(db: Session, area_id: int):
    return db.query(model.Candidate).filter(model.Candidate.area_id == area_id).all()


def get_party(db: Session, party_id: int):
    return db.query(model.Party).filter(model.Party.id == party_id).first()


def get_parties(db: Session):
    return db.query(model.Party).all()


def get_party_members(db: Session, party_id: int):
    return db.query(model.Candidate).filter(model.Candidate.party_id == party_id).all()


def create_candidate(db: Session, citizen_id: int, name: str, area_id: int):
    candidate = model.Candidate(citizen_id=citizen_id, name=name, area_id=area_id)

    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    return candidate


def create_ballot_party(db: Session, party_id: int, area_id: int):
    if party_id == 0:
        return schema.PartyBallot(id=0, area_id=0, party_id=0)
    ballot = model.PartyBallot(area_id=area_id, party_id=party_id)

    db.add(ballot)
    db.commit()
    db.refresh(ballot)

    return ballot


def create_ballot_mp(db: Session, candidate_id: int, area_id: int):
    if candidate_id == 0:
        return schema.MPBallot(id=0, area_id=0, candidate_id=0)
    ballot = model.MPBallot(area_id=area_id, candidate_id=candidate_id)

    db.add(ballot)
    db.commit()
    db.refresh(ballot)

    return ballot


def get_ballots_by_area(db: Session, vote_topic_id: int, area_id: int):
    topic = VOTE_TOPIC_ID.get(vote_topic_id)
    ballots = db.query(topic).filter(topic.area_id == area_id).all()

    return ballots


def get_ballots(db: Session, vote_topic_id: int):
    topic = VOTE_TOPIC_ID.get(vote_topic_id)
    ballots = db.query(topic).all()

    return ballots
