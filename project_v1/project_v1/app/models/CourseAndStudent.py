from sqlalchemy import Column, Integer, String, orm
from app.models.base import Base


class CourseAndStudent(Base):
    id=Column(Integer, primary_key=True, nullable=False, autoincrement=True)

    CourseId = Column(Integer)
    studentId = Column(Integer)
