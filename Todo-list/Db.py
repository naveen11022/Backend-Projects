from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer,create_engine,DATETIME
engine = create_engine(engine = create_engine("mysql+pymysql://root:mysql123@localhost:3306/todo_list"))
import datetime
session = sessionmaker(bind=engine)
session = session()
base = declarative_base()


class user(base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True)
    name = Column(String)
    password = Column(String)
    created_at = Column(DATETIME)

class todo(base):
    __tablename__ = 'todo_list'
    t_id = Column(Integer,primary_key=True)
    uid = Column(Integer)
    title = Column(String)
    description = Column(String)
    created_at = Column(DATETIME,default=datetime.datetime.now())

