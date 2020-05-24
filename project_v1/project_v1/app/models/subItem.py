from sqlalchemy import Column, String, Float, orm,Integer
from app.models.base import Base


class SubItem(Base):
    title = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(50),nullable=False)
    percentage = Column(Float)
    courseId=Column(Integer)

    def __init__(self, title, percentage):
        self.title = title
        self.percentage = percentage

