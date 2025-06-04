from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Boolean,
    create_engine,
    UniqueConstraint,
)
from sqlalchemy.orm import sessionmaker
from datetime import datetime


engine = create_engine("sqlite:///triviagame.db", echo=True)
Session = sessionmaker(bind=engine)


def get_db():
    session = Session()
    try:
        yield session
    finally:
        session.close()


Base = declarative_base()


Base = declarative_base()


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    category = Column(String(100))
    difficulty = Column(String(20))
    question_text = Column(Text, unique=True)
    correct_answer = Column(Text)
    incorrect_answers = Column(Text)
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now())


class GameSession(Base):
    __tablename__ = "game_sessions"
    id = Column(Integer, primary_key=True)
    score = Column(Integer, default=0)
    total_questions = Column(Integer)
    created_at = Column(DateTime, default=datetime.now())
