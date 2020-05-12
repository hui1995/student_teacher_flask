from sqlalchemy import Column, String, Float, orm
from app.models.base import Base


class SubItem(Base):
    title = Column(String(50), primary_key=True, nullable=False)
    percentage = Column(Float)

    def __init__(self, title, percentage):
        self.title = title
        self.percentage = percentage

