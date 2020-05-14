#!/usr/bin/env python

from sqlalchemy import Column, String, Integer, orm
from app.models.base import Base

class Invite(Base):
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)


    teamId=Column(Integer)
    inviteId=Column(Integer)
    inviteeId=Column(Integer)



