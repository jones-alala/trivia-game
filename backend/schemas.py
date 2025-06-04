from pydantic import BaseModel

class FeedbackCreate(BaseModel):
    question: str
    feedback: str
