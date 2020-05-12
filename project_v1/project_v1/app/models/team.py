from sqlalchemy import Column, Integer, String, orm
from app.models.base import Base

class Team(Base):
    TeamName = Column(String(50), nullable=False)
    TeamNumber = Column(Integer, primary_key=True, autoincrement=True)
   