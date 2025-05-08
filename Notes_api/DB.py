from sqlalchemy import create_engine,Column,Integer,String,DateTime,ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()
engine = create_engine("mysql+pymysql://root:mysql123@localhost:3306/blog")
session = sessionmaker(bind=engine)
session = session()
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True)
    username = Column(String)
    password = Column(String)
    created_at = Column(DateTime,default=datetime.datetime.now())

class Notes(Base):
    n_id = Column(Integer,primary_key=True)
    uid = ForeignKey("user.id")
    title = Column(String)
    description = Column(String)
    created_at = Column(DateTime,default=datetime.datetime.now())
    

