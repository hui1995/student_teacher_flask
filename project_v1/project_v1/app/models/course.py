from sqlalchemy import Column, Integer, String, orm
from app.models.base import Base


class Course(Base):
    CourseId = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    courseName = Column(String(50), nullable=False)
    totalNum = Column(Integer)
    teacherId=Column(Integer)
    teamType=Column(Integer,nullable=True)