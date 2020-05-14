from sqlalchemy import Column, String, orm
from app.models.base import Base


class SubCon(Base):
    contribution = Column(String(50), primary_key=True, nullable=False)

