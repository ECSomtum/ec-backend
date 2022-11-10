from sqlalchemy.orm import Session

from . import model, schema


def get_candidate(db: Session, candidate_id: int):
    return db.query(model.Candidate).filter(model.Candidate.id == candidate_id).first()


def get_candidates(db: Session):
    return db.query(model.Candidate).all()


def get_party(db: Session):
    return db.query(model.Party).all()