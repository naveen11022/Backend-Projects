from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session
from datetime import datetime
from pydantic import BaseModel
from typing import List
from fastapi.responses import JSONResponse,Response

from Auth import get_current_user 

router = APIRouter()

DATABASE_URL = "sqlite:///./tasks.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    articles = relationship("Articles", back_populates="user")


class Articles(Base):
    __tablename__ = 'articles'

    A_id = Column(Integer, primary_key=True, index=True)
    uid = Column(Integer, ForeignKey('users.id'))
    article_name = Column(String, nullable=False)
    article_description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="articles")


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Update_article(BaseModel):
    article_name: str
    article_description: str


class ArticleOut(BaseModel):
    A_id: int
    article_name: str
    article_description: str
    created_at: datetime

    class Config:
        orm_mode = True



@router.post("/add_article",tags=["Articles"], response_model=ArticleOut)
def add_article(
    article: ArticleOut,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_article = Articles(
        uid=current_user.id,
        article_name=article.article_name,
        article_description=article.article_description
    )
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article


@router.get("/get_article",tags=["Articles"], response_model=List[ArticleOut])
def get_article(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    articles = db.query(Articles).filter(Articles.uid == current_user.id).all()
    return JSONResponse(articles)

@router.delete("/delete_articles/{id}")
def delete_article(id:int,current_user:User=Depends(get_current_user),db:Session=Depends(SessionLocal)):
    delete_ar = db.query(Articles).filter(id=id,uid=current_user)
    if delete_ar:
        delete_ar.delete
        return Response({"messages":"deleted successfully"}) 
    return Response({"messages":"No Data Found"})


@router.patch("/update_article",tags=["Artilces"])
def update_article(id:int,current_user:User=Depends(get_current_user),db:Session=Depends(SessionLocal)):
    article_details = db.query(Articles).filter(id=id,uid=current_user)
    if article_details:
        article_details.update(article_name=Update_article.article_name,description=Update_article.article_description)
        article_details.save()
        return Response({"messages":"updated successfully"})
    return Response({"No Data Found!!!"})

