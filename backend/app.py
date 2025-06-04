from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import json
from models import get_db, Question, GameSession
from schemas import (
    QuestionOut,
    GameSessionOut,
    AnswerSubmission,
    StartGameResponse,
    Feedback,
)
from typing import List
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# External API configuration
TRIVIA_API_URL = "https://opentdb.com/api.php"
ANIMATION_CATEGORY = 32


def decode_html_entities(text: str) -> str:
    """Simple HTML entity decoding"""
    return text.replace("&quot;", '"').replace("&#039;", "'").replace("&amp;", "&")


@app.post("/start-game", response_model=StartGameResponse) # Changed response_model
def start_game(db: Session = Depends(get_db)):
    # Fetch questions from Open Trivia API
    params = {"amount": 10, "category": ANIMATION_CATEGORY, "type": "multiple"}

    try:
        response = requests.get(TRIVIA_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if data["response_code"] != 0:
            raise HTTPException(status_code=500, detail="Failed to fetch questions")

        # Create game session
        session = GameSession(score=0, total_questions=len(data["results"]))
        db.add(session)
        db.commit()
        db.refresh(session)

        # Store question texts for later ordering
        question_texts = []
        # Process and store questions
        for q in data["results"]:
            # Decode HTML entities
            question_text = decode_html_entities(q["question"])
            correct_answer = decode_html_entities(q["correct_answer"])
            incorrect_answers = [
                decode_html_entities(a) for a in q["incorrect_answers"]
            ]

            question_texts.append(question_text)  # Store text for ordering

            # Check if question exists using question text
            existing = db.query(Question).filter_by(question_text=question_text).first()

            if not existing:
                new_question = Question(
                    category=q["category"],
                    difficulty=q["difficulty"],
                    question_text=question_text,
                    correct_answer=correct_answer,
                    incorrect_answers=json.dumps(incorrect_answers),
                )
                db.add(new_question)

        db.commit()

        # Get stored questions in the same order as API response
        stored_questions = (
        db.query(Question).filter(Question.question_text.in_(question_texts)).all()
        )

        # Create mapping for ordering

        for question in stored_questions:
            question.incorrect_answers = json.loads(question.incorrect_answers)

        question_map = {q.question_text: q for q in stored_questions}
        ordered_questions = [question_map[text] for text in question_texts]

        # Return both session and questions
        return {
            "session": session,
            "questions": ordered_questions,  # Added questions to response
        }

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Trivia API error: {str(e)}")
    except IntegrityError:
        db.rollback()
        # Handle potential unique constraint violation
        return session


@app.get("/questions", response_model=List[QuestionOut])
def get_questions(db: Session = Depends(get_db)):
    questions = db.query(Question).limit(10).all()
    return questions


@app.post("/submit-answer")
def submit_answer(answer: AnswerSubmission, db: Session = Depends(get_db)):
    # Get question from database
    question = db.query(Question).filter_by(id=answer.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Get game session
    session = db.query(GameSession).filter_by(id=answer.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Game session not found")

    # Check answer
    is_correct = answer.answer == question.correct_answer
    if is_correct:
        session.score += 1
        db.commit()

    return {
        "is_correct": is_correct,
        "correct_answer": question.correct_answer,
        "current_score": session.score,
    }


@app.post("/feedback")
def submit_feedback(feedback: Feedback, db: Session = Depends(get_db)):
    question = db.query(Question).filter_by(id=feedback.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    if feedback.like:
        question.likes += 1
    else:
        question.dislikes += 1

    db.commit()
    return {"status": "success", "likes": question.likes, "dislikes": question.dislikes}


@app.get("/session/{session_id}", response_model=GameSessionOut)
def get_session(session_id: int, db: Session = Depends(get_db)):
    session = db.query(GameSession).filter_by(id=session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


# Game Flow:
# Frontend gets questions via /questions
# Submits answers via /submit-answer
# Provides feedback via /feedback
# Checks session status via /session/{id}
