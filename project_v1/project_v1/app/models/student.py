from sqlalchemy import Column, String, Integer, Float, orm
from app.models.user import User

class Student(User):
    id = Column(Integer, foreign_key=True, autoincrement=True)
    GPA = Column(Float)
    email = Column(String(24), unique=True, nullable=True)

    def __init__(self, name, GPA, email, password):
        super(Student,self).__init__(name, password)
        self.id = id
        self.GPA = GPA
        self.email = email

    def jsonstr(self):

        jsondata = {
            'name':self.name,
            'id': self.id,
            'GPA': self.GPA,
            'email': self.email

        }

        return jsondata
