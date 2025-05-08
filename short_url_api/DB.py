from sqlalchemy import create_engine,Column,Integer,String,DateTime,ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime

engine = create_engine("mysql+pymysql://root:mysql123@localhost:3306/shorturl")
Base = declarative_base()
session = sessionmaker(bind=engine)
session = session()

class user(Base):
    __tablename__ = 'user'
    id = Column(Integer,primary_key=True)
    username = Column(String)
    password = Column(String)
    created_at = Column(DateTime,default=datetime.datetime.now())

class shorturl(Base):
    __tablename_ = 'shorturl'
    id = Column(Integer,primary_key=True)
    uid = ForeignKey("user.id")
    url = Column(String)
    shortend = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime,default='Still Not updated')

