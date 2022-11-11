from sqlalchemy.orm import Session

from . import model, schema


def get_candidate(db: Session, candidate_id: int):
    return db.query(model.Candidate).filter(model.Candidate.id == candidate_id).first()


def get_candidates(db: Session):
    return db.query(model.Candidate).all()


def get_party(db: Session):
    return db.query(model.Party).all()


def get_party_members(db: Session, party_id: int):
    return db.query(model.Candidate).filter(model.Candidate.party_id == party_id).all()


def create_ballot(db: Session, party_id: int, candidate_id: int):
    candidate = get_candidate(db, candidate_id)
    ballot = model.Ballot(area_id=candidate.area_id, party_id=party_id, candidate_id=candidate_id)

    db.add(ballot)
    db.commit()
    db.refresh(ballot)

    return ballot


def get_ballots_by_area(db: Session, area_id: int):
    ballots = db.query(model.Ballot).filter(model.Ballot.area_id == area_id).all()

    return ballots


def get_ballots(db: Session):
    ballots = db.query(model.Ballot).all()

    return ballots

# def get_party_ranking(db: Session):
#     rank = db.query(model.Party).group_by(accept_candidate)
