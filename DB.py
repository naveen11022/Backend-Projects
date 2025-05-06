from sqlalchemy import Column, Integer, String,create_engine,DateTime,ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("mysql+pymysql://root:mysql123@localhost:3306/blog")
session = sessionmaker(bind=engine)
session = session()
Base = declarative_base()

class user(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True)
    name = Column(String)
    password = Column(String)
    created_at = Column(DateTime)

class Blogger(Base):
    __tablename__ = 'blog'
    b_id = Column(Integer,primary_key=True)
    u_id = Column(ForeignKey("user.id"))
    title = Column(String)
    content = Column(String)
    category = Column(String)
    tags = Column(String)

