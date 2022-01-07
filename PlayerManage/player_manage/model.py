import os,sys

from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer,Text, String, DateTime,Boolean,MetaData,create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Player(Base):
    __tablename__ = 'player'
    id = Column(Integer(), primary_key=True)
    uuid = Column(Text(length=128), unique=True)
    name = Column(String(64), unique=True)
    lastjoin = Column(DateTime(), index=True)
    firstjoin = Column(DateTime(), index=True)
    is_bot = Column(Boolean(), default=0)

prefix = 'sqlite:///' if sys.platform.startswith('win') else 'sqlite:////'
engine = create_engine(prefix + './PlayerManage.db' + '?check_same_thread=False&timeout=20')
metaData = MetaData(engine)
session = Session(engine)

def creat_database():
    Base.metadata.create_all(engine)
