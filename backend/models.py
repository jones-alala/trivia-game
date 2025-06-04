from sqlalchemy import Column, Integer, String, Text
from .database import Base

class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    feedback = Column(String(10), nullable=False)  # like/dislike
