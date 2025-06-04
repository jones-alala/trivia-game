import React, { useState, useEffect } from "react";
import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000"; //

function TriviaGame() {
  const [session, setSession] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [score, setScore] = useState(0);
  const [feedback, setFeedback] = useState("");
  const [answered, setAnswered] = useState(false);

  useEffect(() => {
    startGame();
  }, []);

  const startGame = async () => {
    const res = await axios.post(`${BASE_URL}/start-game`);
    const { session, questions } = res.data;
    setSession(session);
    setQuestions(questions);
    setCurrentIndex(0);
    setScore(0);
    setFeedback("");
    setAnswered(false);
  };

  const handleAnswer = async (answer) => {
    const currentQuestion = questions[currentIndex];

    const res = await axios.post(`${BASE_URL}/submit-answer`, {
      session_id: session.id,
      question_id: currentQuestion.id,
      answer,
    });

    const isCorrect = res.data.is_correct;
    if (isCorrect) setScore(res.data.current_score);

    setFeedback(
      isCorrect
        ? "✅ Correct!"
        : `❌ Wrong! Correct: ${res.data.correct_answer}`
    );
    setAnswered(true);
  };

  const handleFeedback = async (type) => {
    const currentQuestion = questions[currentIndex];
    await axios.post(`${BASE_URL}/feedback`, {
      question_id: currentQuestion.id,
      like: type === "like",
    });
    alert(`You ${type}d the question!`);
  };

  const nextQuestion = () => {
    setCurrentIndex((prev) => prev + 1);
    setFeedback("");
    setAnswered(false);
  };

  if (!session || questions.length === 0) return <p>Loading...</p>;

  if (currentIndex >= questions.length) {
    return (
      <div>
        <h2>Game Over!</h2>
        <p>
          Your score: {score} / {questions.length}
        </p>
        <button onClick={startGame}>Play Again</button>
      </div>
    );
  }

  const currentQuestion = questions[currentIndex];
  const allAnswers = [
    ...currentQuestion.incorrect_answers,
    currentQuestion.correct_answer,
  ].sort();

  return (
    <div>
      <h2 dangerouslySetInnerHTML={{ __html: currentQuestion.question_text }} />
      {allAnswers.map((ans, i) => (
        <button
          key={i}
          onClick={() => handleAnswer(ans)}
          disabled={answered}
          dangerouslySetInnerHTML={{ __html: ans }}
        />
      ))}

      {feedback && (
        <>
          <p>{feedback}</p>
          <button onClick={() => handleFeedback("like")}>👍 Like</button>
          <button onClick={() => handleFeedback("dislike")}>👎 Dislike</button>
          <br />
          <button onClick={nextQuestion}>Next Question</button>
        </>
      )}

      <p>
        <strong>Score:</strong> {score}
      </p>
    </div>
  );
}

export default TriviaGame;
