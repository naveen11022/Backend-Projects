from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from fastapi.responses import Response
from datetime import datetime
import uvicorn

app = FastAPI()

DATABASE_URL = "sqlite:///./tasks.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True, index=True)
    uid = Column(Integer, ForeignKey('users.id'))
    amount = Column(Integer)
    description = Column(String, nullable=False)
    createdAt = Column(DateTime, default=datetime.utcnow)

@app.post("/add", tags=["Expense"])
def add_expense(amount: int, description: str, db: Session = Depends(SessionLocal)):
    new_expense = Expense(amount=amount, description=description)
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return Response(content=f"Expense added successfully with ID {new_expense.id}", status_code=201)

@app.get("/get_expense", tags=["Expense"])
def get_expense(db: Session = Depends(SessionLocal)):
    expenses = db.query(Expense).all()
    if not expenses:
        raise HTTPException(status_code=404, detail="No expenses found.")
    return expenses

@app.delete("delete_expense")
def delete_expense(id:int):
    details = Session.query(Expense).filter(id=id)
    if details:
        details.delete
        return Response({"messages":"Expense deleted succesfully"})
    else:
        return Response({"message":"No data found"})
    
if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000)
