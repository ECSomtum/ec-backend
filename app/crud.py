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


def get_party(db: Session):
    return db.query(model.Party).all()


def get_party_members(db: Session, party_id: int):
    return db.query(model.Candidate).filter(model.Candidate.party_id == party_id).all()


def create_ballot_party(db: Session, party_id: int, area_id: int):
    ballot = model.PartyBallot(area_id=area_id, party_id=party_id)

    db.add(ballot)
    db.commit()
    db.refresh(ballot)

    return ballot


def create_ballot_mp(db: Session, candidate_id: int, area_id: int):
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
