from sqlalchemy import Column, String, Integer, orm
from app.models.student import Student

class Member(Student):

    contribution = Column(String(50), nullable=True)

    def __init__(self, name, id, GPA, email, contribution, password):
        super(Member,self).__init__(name, GPA, email, password)
        self.contribution = contribution
        

    def jsonstr(self):

        jsondata = {
            'name':self.name,
            'age': self.age,
            'email':self.email,
            'contribution':self.contribution

        }

        return jsondata