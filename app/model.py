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

    party_id = Column(Integer, ForeignKey("party.id"))
    party = relationship("Party", back_populates="candidates")


class Party(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    pictureUrl = Column(Text(500))

    candidates = relationship("Candidate", back_populates="party")
