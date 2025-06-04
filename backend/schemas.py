from pydantic import BaseModel
from typing import List


class QuestionBase(BaseModel):
    category: str
    difficulty: str
    question_text: str
    correct_answer: str
    incorrect_answers: List[str]


class QuestionCreate(QuestionBase):
    pass


class QuestionOut(BaseModel):
    id: int
    category: str
    difficulty: str
    question_text: str
    correct_answer: str
    incorrect_answers: List[str]  # List here, NOT JSON string
    likes: int
    dislikes: int

    class Config:
        orm_mode = True


class GameSessionCreate(BaseModel):
    total_questions: int


class AnswerSubmission(BaseModel):
    session_id: int
    question_id: int
    answer: str


class Feedback(BaseModel):
    question_id: int
    like: bool


class GameSessionOut(BaseModel):
    id: int
    score: int
    total_questions: int

    class Config:
        orm_mode = True


class StartGameResponse(BaseModel):
    session: GameSessionOut
    questions: List[QuestionOut]
