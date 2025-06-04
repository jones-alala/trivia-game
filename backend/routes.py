from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas, database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/feedback", status_code=201)
def submit_feedback(feedback: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    if feedback.feedback not in ["like", "dislike"]:
        raise HTTPException(status_code=400, detail="Invalid feedback type.")
    return crud.create_feedback(db, feedback)