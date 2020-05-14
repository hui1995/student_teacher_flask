from sqlalchemy import Column, String, Integer, orm
from app.models.user import User

class Teacher(User):
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(24), unique=True, nullable=True)
    def __init__(self, name, email, password):
        super(Teacher,self).__init__(name, password)
        

    def jsonstr(self):

        jsondata = {
            'name':self.name,
            'id': self.id

        }

        return jsondata
