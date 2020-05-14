from sqlalchemy import Column, String, orm
from app.models.base import Base

class User(Base):
    __abstract__ = True # 抽象类 不会生成表
    name = Column(String(50), primary_key=True, nullable=False)
    password = Column(String(50))
    programme = Column(String(50),nullable=False)


    def __init__(self, name, password, programme):
        super(User,self).__init__()
        self.name = name
        self.password = password
        self.programme = programme
