from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from models import get_db, Question, GameSession
from schemas import schemas


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# External API configuration
TRIVIA_API_URL = "https://opentdb.com/api.php"
ANIMATION_CATEGORY = 32
@app.get("/")
def index():
    return {"message": "Welcome to my first backend app"} 


# end points 
# GET/questions - Fetches a set of questions (e.g., 10) from the API and returns them to the frontend
# 1. Frontend requests to start a new game -> Backend creates a game session and fetches questions from the API, stores them in the database (if not already present) and associates them with the game session.

# 2. Backend returns the questions (without the correct answer) and a session ID.

# 3. For each question, the frontend sends the user's answer and the session ID to the backend. The backend then checks the answer and updates the score.

# 4. After answering, the frontend can send a like/dislike for that question.

# - `POST /start_game`:
# - Creates a new game session.
# - Fetches 10 questions from the API (category=32, amount=10).
# - For each question, check if it exists in our database (by the question text? or by an API id if available). If not, create it.
# - Then create `GameQuestion` entries for this session, linking to the questions.
# - Return the session ID and the list of questions (without the correct answer) in the order they will be presented.

# - `POST /submit_answer`:
#  Expects: session_id, question_id, and the answer text (or index? but the frontend will have the text of the answer).
# - Check if the provided answer matches the correct answer for that question (in our Question table).
# - Update the GameQuestion entry: set `user_answer` and `is_correct`.
# - Update the GameSession's score: if correct, increment by 1.
# - Return whether the answer was correct and the correct answer.

# - `POST /feedback`:
# - Expects: session_id, question_id, and a boolean (like=true, dislike=false).
# - Update the Question's like or dislike count.
# - `GET /score/{session_id}`:
# - Get the current score for the session.

@app.get("/geturl")
def get_url():
    return {"message": "This is a placeholder for GET /geturl"}

@app.post("/posturl")
def post_url():
    return {"message": "This is a placeholder for POST /posturl"}