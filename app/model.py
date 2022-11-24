from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import relationship


@as_declarative()
class Base:

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class Candidate(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    pictureUrl = Column(Text(500))
    area_id = Column(Integer)

    party_id = Column(Integer, ForeignKey("party.id"))
    party = relationship("Party", back_populates="candidates")

    mp_ballots = relationship("MPBallot", back_populates="candidate")


class Party(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    pictureUrl = Column(Text(500))

    candidates = relationship("Candidate", back_populates="party")
    party_ballots = relationship("PartyBallot", back_populates="party")


class PartyBallot(Base):
    id = Column(Integer, primary_key=True)
    area_id = Column(Integer)

    party_id = Column(Integer, ForeignKey("party.id"))
    party = relationship("Party", back_populates="party_ballots")


class MPBallot(Base):
    id = Column(Integer, primary_key=True)
    area_id = Column(Integer)

    candidate_id = Column(Integer, ForeignKey("candidate.id"))
    candidate = relationship("Candidate", back_populates="mp_ballots")
