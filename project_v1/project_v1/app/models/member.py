from sqlalchemy import Column, String, Integer, orm
from app.models.base import Base


class Member(Base):
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)


    contribution = Column(String(50), nullable=True)
    teamId=Column(Integer)
    studentId=Column(Integer)
    votenum = Column(Integer)
    isVote=Column(Integer,default=0)
    leaderEvate=Column(String(50),nullable=True)


